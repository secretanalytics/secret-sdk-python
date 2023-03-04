from __future__ import annotations

from asyncio import AbstractEventLoop, get_event_loop, TimeoutError
from threading import Lock
from typing import Optional, Union

import nest_asyncio
from aiohttp import ClientSession
from multidict import CIMultiDict

from secret_sdk.core import Coins, Dec, Numeric
from secret_sdk.exceptions import LCDResponseError
from secret_sdk.key.key import Key
from secret_sdk.util.json import dict_to_data
from secret_sdk.util.url import urljoin

from .api.auth import AsyncAuthAPI, AuthAPI
from .api.authz import AsyncAuthzAPI, AuthzAPI
from .api.bank import AsyncBankAPI, BankAPI
from .api.distribution import AsyncDistributionAPI, DistributionAPI
from .api.feegrant import AsyncFeeGrantAPI, FeeGrantAPI
from .api.gov import AsyncGovAPI, GovAPI
from .api.ibc import AsyncIbcAPI, IbcAPI
from .api.ibc_transfer import AsyncIbcTransferAPI, IbcTransferAPI
from .api.mint import AsyncMintAPI, MintAPI
from .api.slashing import AsyncSlashingAPI, SlashingAPI
from .api.staking import AsyncStakingAPI, StakingAPI
from .api.tendermint import AsyncTendermintAPI, TendermintAPI
from .api.tx import AsyncTxAPI, TxAPI
from .api.wasm import AsyncWasmAPI, WasmAPI
from .api.registration import AsyncRegistrationAPI, RegistrationAPI
from .params import APIParams
from secret_sdk.util.encrypt_utils import EncryptionUtils
from .wallet import AsyncWallet, Wallet
from secret_sdk.core.fee import Fee


# default gas_price is 0.25, amount = gas * gas_price
default_fees = {
    "upload": Fee(
        gas_limit=1_000_000, amount=Coins.from_data([{"amount": 250_000, "denom": "uscrt"}])
    ),
    "init": Fee(
        gas_limit=500_000, amount=Coins.from_data([{"amount": 125_000, "denom": "uscrt"}])
    ),
    "exec": Fee(
        gas_limit=200_000, amount=Coins.from_data([{"amount": 50_000, "denom": "uscrt"}])
    ),
    "send": Fee(
        gas_limit=80_000, amount=Coins.from_data([{"amount": 20_000, "denom": "uscrt"}])
    ),
    "default": Fee(
        gas_limit=200_000, amount=Coins.from_data([{"amount": 50_000, "denom": "uscrt"}])
    ),
}
default_gas_prices = Coins.from_data([{"amount": 0.25, "denom": "uscrt"}])
default_gas_adjustment = 1

mainnet_chain_ids = {"secret-2", "secret-3", "secret-4"}

# mainnetConsensusIoPubKey = bytes.fromhex(
#   "083b1a03661211d5a4cc8d39a77795795862f7730645573b2bcc2c1920c53c04"
# )
mainnetConsensusIoPubKey = bytes.fromhex(
    "efdfbee583877e6d12c219695030a5bfb72e0a3abdc416655aa4a30c95a4446f"
)  # == base64.b64decode("79++5YOHfm0SwhlpUDClv7cuCjq9xBZlWqSjDJWkRG8=")

REQUEST_CONFIG = {
    "GET_TIMEOUT": 30,
    "POST_TIMEOUT": 30,
    "GET_RETRY": 1
}


class AsyncLCDClient:
    def __init__(
        self,
        url: str,
        chain_id: Optional[str] = None,
        gas_prices: Optional[Coins.Input] = default_gas_prices,
        gas_adjustment: Optional[Numeric.Input] = default_gas_adjustment,
        custom_fees: Optional[dict] = default_fees,
        loop: Optional[AbstractEventLoop] = None,
        _create_session: bool = True,  # don't create a session (used for sync LCDClient)
        _request_config: Optional[dict] = REQUEST_CONFIG
    ):
        self._request_config = _request_config
        if loop is None:
            loop = get_event_loop()
        self.loop = loop
        if _create_session:
            self.session = ClientSession(
                headers={"Accept": "application/json"}, loop=self.loop
            )

        self.chain_id = chain_id
        self.url = url
        self.last_request_height = None

        self.gas_prices = Coins(gas_prices)
        self.gas_adjustment = gas_adjustment
        self.custom_fees = custom_fees

        self.auth = AsyncAuthAPI(self)
        self.bank = AsyncBankAPI(self)
        self.distribution = AsyncDistributionAPI(self)
        self.feegrant = AsyncFeeGrantAPI(self)
        self.gov = AsyncGovAPI(self)
        self.mint = AsyncMintAPI(self)
        self.authz = AsyncAuthzAPI(self)
        self.slashing = AsyncSlashingAPI(self)
        self.staking = AsyncStakingAPI(self)
        self.tendermint = AsyncTendermintAPI(self)
        self.wasm = AsyncWasmAPI(self)
        self.ibc = AsyncIbcAPI(self)
        self.ibc_transfer = AsyncIbcTransferAPI(self)
        self.tx = AsyncTxAPI(self)
        self.registration = AsyncRegistrationAPI(self)

        if self.chain_id in mainnet_chain_ids:
            consensus_io_pub_key = mainnetConsensusIoPubKey
        else:
            consensus_io_pub_key = RegistrationAPI(self).consensus_io_pub_key()
        self.encrypt_utils = EncryptionUtils(consensus_io_pub_key)

    def wallet(self, key: Key) -> AsyncWallet:
        """Creates a :class:`AsyncWallet` object from a key.

        Args:
            key (Key): key implementation
        """
        return AsyncWallet(self, key)

    async def _get(
        self,
        endpoint: str,
        params: Optional[Union[APIParams, CIMultiDict, list, dict]] = None,
        timeout: Optional[int] = None,
        retry_attempts: Optional[int] = None
    ):
        params = params or {}
        if (
            params
            and hasattr(params, "to_dict")
            and callable(getattr(params, "to_dict"))
        ):
            params = params.to_dict()

        block_height = 0
        if 'block_height' in params:
            block_height = params.pop('block_height')
            self.session.headers['x-cosmos-block-height'] = str(block_height)
        current_attempt = 0

        timeout, retry_attempts = timeout or self._request_config['GET_TIMEOUT'], retry_attempts or self._request_config['GET_RETRY']
        while True:
            current_attempt += 1
            async with self.session.get(
                urljoin(self.url, endpoint), params=params, timeout=timeout
            ) as response:
                try:
                    result = await response.json(content_type=None)
                except TimeoutError:
                    if current_attempt < retry_attempts:
                        continue
                    raise TimeoutError(f'{urljoin(self.url, endpoint)}, time out after {str(current_attempt)} attempts')
                except Exception as e:
                    if current_attempt < retry_attempts:
                        continue
                    raise e
                if not 200 <= response.status < 299:
                    raise LCDResponseError(message=str(result), response=response)

                request_height = response.headers.get('grpc-metadata-x-cosmos-block-height')
                self.last_request_height = (
                    request_height if result else self.last_request_height
                )
                if block_height:
                    self.session.headers.pop('x-cosmos-block-height')
                return result

    async def _post(
        self,
        endpoint: str,
        data: Optional[dict] = None
    ):

        async with self.session.post(
            urljoin(self.url, endpoint), json=data and dict_to_data(data), timeout=self._request_config["POST_TIMEOUT"]
        ) as response:
            try:
                result = await response.json(content_type=None)
            except Exception as e:
                raise LCDResponseError(message=str(e), response=str(e))
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=result.get("error"), response=response)
        self.last_request_height = (
            result.get("height") if result else self.last_request_height
        )
        return result

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


class LCDClient(AsyncLCDClient):
    """An object representing a connection to a node running the Secret LCD server."""

    url: str
    """URL endpoint of LCD server."""

    chain_id: str
    """Chain ID of blockchain network connecting to."""

    gas_prices: Coins
    """Gas prices to use for automatic fee estimation."""

    gas_adjustment: Union[str, float, int, Dec]
    """Gas adjustment factor for automatic fee estimation."""

    custom_fees: Optional[dict]
    """Custom fees"""

    last_request_height: Optional[int]  # type: ignore
    """Height of response of last-made made LCD request."""

    auth: AuthAPI
    """:class:`AuthAPI<secret_sdk.client.lcd.api.auth.AuthAPI>`."""

    bank: BankAPI
    """:class:`BankAPI<secret_sdk.client.lcd.api.bank.BankAPI>`."""

    distribution: DistributionAPI
    """:class:`DistributionAPI<secret_sdk.client.lcd.api.distribution.DistributionAPI>`."""

    gov: GovAPI
    """:class:`GovAPI<secret_sdk.client.lcd.api.gov.GovAPI>`."""

    feegrant: FeeGrantAPI
    """:class:`FeeGrant<secret_sdk.client.lcd.api.feegrant.FeeGrantAPI>`."""

    mint: MintAPI
    """:class:`MintAPI<secret_sdk.client.lcd.api.mint.MintAPI>`."""

    authz: AuthzAPI
    """:class:`AuthzAPI<secret_sdk.client.lcd.api.authz.AuthzAPI>`."""

    slashing: SlashingAPI
    """:class:`SlashingAPI<secret_sdk.client.lcd.api.slashing.SlashingAPI>`."""

    staking: StakingAPI
    """:class:`StakingAPI<secret_sdk.client.lcd.api.staking.StakingAPI>`."""

    tendermint: TendermintAPI
    """:class:`TendermintAPI<secret_sdk.client.lcd.api.tendermint.TendermintAPI>`."""

    wasm: WasmAPI
    """:class:`WasmAPI<secret_sdk.client.lcd.api.wasm.WasmAPI>`."""

    tx: TxAPI
    """:class:`TxAPI<secret_sdk.client.lcd.api.tx.TxAPI>`."""

    ibc: IbcAPI
    """:class:`IbcAPI<secret_sdk.client.lcd.api.ibc.IbcAPI>`."""

    ibc_transfer: IbcTransferAPI
    """:class:`IbcTransferAPI<secret_sdk.client.lcd.api.ibc_transfer.IbcTransferAPI>`."""

    def __init__(
        self,
        url: str,
        chain_id: str = None,
        gas_prices: Optional[Coins.Input] = default_gas_prices,
        gas_adjustment: Optional[Numeric.Input] = default_gas_adjustment,
        custom_fees: Optional[dict] = default_fees,
        _request_config: Optional[dict] = REQUEST_CONFIG
    ):
        self.lock = Lock()
        super().__init__(
            url,
            chain_id,
            gas_prices,
            gas_adjustment,
            custom_fees,
            _create_session=False,
            loop=nest_asyncio.apply(get_event_loop()),
            _request_config=_request_config
        )

        self.auth = AuthAPI(self)
        self.bank = BankAPI(self)
        self.distribution = DistributionAPI(self)
        self.gov = GovAPI(self)
        self.feegrant = FeeGrantAPI(self)
        self.mint = MintAPI(self)
        self.authz = AuthzAPI(self)
        self.slashing = SlashingAPI(self)
        self.staking = StakingAPI(self)
        self.tendermint = TendermintAPI(self)
        self.wasm = WasmAPI(self)
        self.ibc = IbcAPI(self)
        self.ibc_transfer = IbcTransferAPI(self)
        self.tx = TxAPI(self)
        self.registration = RegistrationAPI(self)

        if self.chain_id in mainnet_chain_ids:
            consensus_io_pub_key = mainnetConsensusIoPubKey
        else:
            consensus_io_pub_key = self.registration.consensus_io_pub_key()
        self.encrypt_utils = EncryptionUtils(consensus_io_pub_key)

    async def __aenter__(self):
        raise NotImplementedError(
            "async context manager not implemented - you probably want AsyncLCDClient"
        )

    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplementedError(
            "async context manager not implemented - you probably want AsyncLCDClient"
        )

    def wallet(self, key: Key) -> Wallet:  # type: ignore
        """Creates a :class:`Wallet` object from a key for easy transaction creating and
        signing.

        Args:
            key (Key): key implementation
        """
        return Wallet(self, key)

    async def _get(self, *args, **kwargs):
        # session has to be manually created and torn down for each HTTP request in a
        # synchronous client
        with self.lock:
            self.session = ClientSession(
                headers={"Accept": "application/json"}, loop=self.loop
            )
            try:
                result = await super()._get(*args, **kwargs)
            finally:
                await self.session.close()
        return result

    async def _post(self, *args, **kwargs):
        # session has to be manually created and torn down for each HTTP request in a
        # synchronous client
        with self.lock:
            self.session = ClientSession(
                headers={"Accept": "application/json"}, loop=self.loop
            )
            try:
                result = await super()._post(*args, **kwargs)
            finally:
                await self.session.close()
        return result

