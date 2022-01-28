from __future__ import annotations

from asyncio import AbstractEventLoop, get_event_loop
from json import JSONDecodeError
from typing import Optional, Union

import nest_asyncio
from aiohttp import ClientSession

from secret_sdk.core import Coins, Dec, Numeric
from secret_sdk.core.auth import StdFee
from secret_sdk.exceptions import LCDResponseError
from secret_sdk.key.key import Key
from secret_sdk.util.json import dict_to_data
from secret_sdk.util.url import urljoin

from .api.auth import AsyncAuthAPI, AuthAPI
from .api.bank import AsyncBankAPI, BankAPI
from .api.distribution import AsyncDistributionAPI, DistributionAPI
from .api.staking import AsyncStakingAPI, StakingAPI
from .api.tendermint import AsyncTendermintAPI, TendermintAPI
from .api.tx import AsyncTxAPI, TxAPI
from .api.wasm import AsyncWasmAPI, WasmAPI
from .lcdutils import AsyncLCDUtils, LCDUtils
from .wallet import AsyncWallet, Wallet

# default gas_price is 0.25, amount = gas * gas_price
default_fees = {
    "upload": StdFee(
        gas=1_000_000, amount=Coins.from_data([{"amount": 250_000, "denom": "uscrt"}])
    ),
    "init": StdFee(
        gas=500_000, amount=Coins.from_data([{"amount": 125_000, "denom": "uscrt"}])
    ),
    "exec": StdFee(
        gas=200_000, amount=Coins.from_data([{"amount": 50_000, "denom": "uscrt"}])
    ),
    "send": StdFee(
        gas=80_000, amount=Coins.from_data([{"amount": 20_000, "denom": "uscrt"}])
    ),
    "default": StdFee(
        gas=200_000, amount=Coins.from_data([{"amount": 50_000, "denom": "uscrt"}])
    ),
}
default_gas_prices = Coins.from_data([{"amount": 0.25, "denom": "uscrt"}])
default_gas_adjustment = 1


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
    ):
        if loop is None:
            loop = get_event_loop()
        self.loop = loop
        if _create_session:
            self.session = ClientSession(
                headers={"Accept": "application/json"}, loop=self.loop
            )

        self.chain_id = chain_id
        self.url = url
        self.gas_prices = Coins(gas_prices)
        self.gas_adjustment = gas_adjustment
        self.custom_fees = custom_fees
        self.last_request_height = None

        self.auth = AsyncAuthAPI(self)
        self.bank = AsyncBankAPI(self)
        self.distribution = AsyncDistributionAPI(self)
        self.staking = AsyncStakingAPI(self)
        self.tendermint = AsyncTendermintAPI(self)
        self.wasm = AsyncWasmAPI(self)
        self.tx = AsyncTxAPI(self)
        self.utils = AsyncLCDUtils(self)

    def wallet(self, key: Key) -> AsyncWallet:
        """Creates a :class:`AsyncWallet` object from a key.

        Args:
            key (Key): key implementation
        """
        return AsyncWallet(self, key)

    async def _get(
        self, endpoint: str, params: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.get(
            urljoin(self.url, endpoint), params=params
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise LCDResponseError(message=str(response.reason), response=response)
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=result.get("error"), response=response)
        self.last_request_height = result.get("height")
        return result if raw else result["result"]

    async def _post(
        self, endpoint: str, data: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.post(
            urljoin(self.url, endpoint), json=data and dict_to_data(data)
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise LCDResponseError(message=str(response.reason), response=response)
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=result.get("error"), response=response)
        self.last_request_height = result.get("height")
        return result if raw else result["result"]

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

    staking: StakingAPI
    """:class:`StakingAPI<secret_sdk.client.lcd.api.staking.StakingAPI>`."""

    tendermint: TendermintAPI
    """:class:`TendermintAPI<secret_sdk.client.lcd.api.tendermint.TendermintAPI>`."""

    wasm: WasmAPI
    """:class:`WasmAPI<secret_sdk.client.lcd.api.wasm.WasmAPI>`."""

    tx: TxAPI
    """:class:`TxAPI<secret_sdk.client.lcd.api.tx.TxAPI>`."""

    def __init__(
        self,
        url: str,
        chain_id: str = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        custom_fees: Optional[dict] = default_fees,
    ):
        super().__init__(
            url,
            chain_id,
            gas_prices,
            gas_adjustment,
            custom_fees,
            _create_session=False,
            loop=nest_asyncio.apply(get_event_loop()),
        )

        self.auth = AuthAPI(self)
        self.bank = BankAPI(self)
        self.distribution = DistributionAPI(self)
        self.staking = StakingAPI(self)
        self.tendermint = TendermintAPI(self)
        self.wasm = WasmAPI(self)
        self.tx = TxAPI(self)
        self.utils = LCDUtils(self)

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
        self.session = ClientSession(
            headers={"Accept": "application/json"}, loop=self.loop
        )
        try:
            result = await super()._post(*args, **kwargs)
        finally:
            await self.session.close()
        return result
