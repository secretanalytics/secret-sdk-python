import base64
import re
import json
from typing import List, Optional

import attr
from multidict import CIMultiDict

from secret_sdk.core import AccAddress, Coins, Dec, Numeric, PublicKey
from secret_sdk.core import SearchTxsResponse, StdFee, StdSignMsg, StdTx, TxInfo
from secret_sdk.core.broadcast import (
    AsyncTxBroadcastResult,
    BlockTxBroadcastResult,
    SyncTxBroadcastResult,
)
from secret_sdk.core.tx_decoder import msg_decoder_mapper
from secret_sdk.core.fee import Fee
from secret_sdk.core.msg import Msg
from secret_sdk.core.tx import AuthInfo, SignerData, SignMode, Tx, TxBody, TxInfo
from secret_sdk.util.hash import hash_amino
from secret_sdk.util.json import JSONSerializable

from secret_sdk.protobuf.secret.compute.v1beta1 import MsgInstantiateContractResponse, MsgExecuteContractResponse
from ..params import APIParams
from ._base import BaseAsyncAPI, sync_bind

__all__ = [
    "AsyncTxAPI",
    "TxAPI",
    "BroadcastOptions",
    "CreateTxOptions",
    "SignerOptions",
]


@attr.s
class SignerOptions:
    """SignerOptions specifies infomations about signers
    Args:
        address (AccAddress): address of the signer
        sequence (int, optional): nonce of the messages from the signer
        public_key (PublicKey, optional): signer's PublicKey
    """

    address: AccAddress = attr.ib()
    sequence: Optional[int] = attr.ib(default=None)
    public_key: Optional[PublicKey] = attr.ib(default=None)


@attr.s
class CreateTxOptions:
    """

    Args:
        msgs (List[Msg]): list of messages to include
        fee (Optional[Fee], optional): transaction fee. If ``None``, will be estimated.
            See more on `fee estimation`_.
        memo (str, optional): optional short string to include with transaction.
        gas (str, optional): gas limit to set per-transaction; set to "auto" to calculate sufficient gas automatically
        gas_prices (Coins.Input, optional): gas prices for fee estimation.
        gas_adjustment (Numeric.Input, optional): gas adjustment for fee estimation.
        fee_denoms (List[str], optional): list of denoms to use for fee after estimation.
        account_number (int, optional): account number (overrides blockchain query if
            provided)
        sequence (int, optional): sequence (overrides blockchain qu ery if provided)
        timeout_height (int, optional):  specifies a block timeout height to prevent the tx from being committed past a certain height.
        sign_mode: (SignMode, optional): SignMode.SIGN_MODE_DIRECT by default. multisig needs SignMode.SIGN_MODE_LEGACY_AMINO_JSON.
    """

    msgs: List[Msg] = attr.ib()
    fee: Optional[Fee] = attr.ib(default=None)
    memo: Optional[str] = attr.ib(default=None)
    gas: Optional[str] = attr.ib(default=None)
    gas_prices: Optional[Coins.Input] = attr.ib(default=None)
    gas_adjustment: Optional[Numeric.Output] = attr.ib(
        default=0, converter=Numeric.parse
    )
    fee_denoms: Optional[List[str]] = attr.ib(default=None)
    account_number: Optional[int] = attr.ib(default=None)
    sequence: Optional[int] = attr.ib(default=None)
    timeout_height: Optional[int] = attr.ib(default=None)
    sign_mode: Optional[SignMode] = attr.ib(default=None)


@attr.s
class BroadcastOptions:
    sequences: Optional[List[int]] = attr.ib()
    fee_granter: Optional[AccAddress] = attr.ib(default=None)


@attr.s
class GasInfo:
    gas_wanted: int = attr.ib(converter=int)
    gas_used: int = attr.ib(converter=int)


@attr.s
class EventAttribute:
    key: str = attr.ib()
    value: str = attr.ib()


@attr.s
class Event:
    type: str = attr.ib()
    attributes: List[EventAttribute] = attr.ib(converter=list)


@attr.s
class SimulateResult:
    data: str = attr.ib()
    log: str = attr.ib()
    events: List[Event] = attr.ib(converter=list)


@attr.s
class SimulateResponse(JSONSerializable):
    gas_info: GasInfo = attr.ib()
    result: SimulateResult = attr.ib()

    @classmethod
    def from_data(cls, data: dict):
        return cls(gas_info=data["gas_info"], result=data["result"])


class AsyncTxAPI(BaseAsyncAPI):
    async def tx_info(self, tx_hash: str) -> TxInfo:
        """Fetches information for an included transaction given a tx hash.

        Args:
            tx_hash (str): hash of transaction to lookup

        Returns:
            TxInfo: transaction info
        """
        res = await self._c._get(f"/cosmos/tx/v1beta1/txs/{tx_hash}")
        return TxInfo.from_data(res["tx_response"])

    async def tx_by_id(self, id: str) -> TxInfo:
        """Fetches information for an included transaction given a tx hash.

        Args:
            tx_hash (str): hash of transaction to lookup

        Returns:
            TxInfo: transaction info
        """
        res = await self._c._get(f"/cosmos/tx/v1beta1/txs/{id}")
        if "tx" not in res:
            raise Exception("Unexpected response data format")
        # TODO: update TxInfo interface
        return await self.decrypt_txs_response(res)

    async def decrypt_data_field(self, data_field: str, nonces):
        wasm_output_data_cipher_bz = bytearray.fromhex(data_field)

        for nonce in nonces:
            try:
                return base64.b64decode(
                    await self._c.utils.decrypt(wasm_output_data_cipher_bz, nonce)
                )
            except Exception as e:
                error = e
        raise error

    async def decrypt_logs(self, logs, nonces):
        for log in logs:
            for e in log["events"]:
                if e["type"] == "wasm":
                    for nonce in nonces:
                        nonce_ok = False
                        for a in e["attributes"]:
                            try:
                                a["key"] = await self._c.utils.decrypt(
                                    base64.b64decode(a["key"]), nonce
                                )
                                nonce_ok = True
                            except Exception:
                                pass
                            try:
                                a["value"] = await self._c.utils.decrypt(
                                    base64.b64decode(a["value"], nonce)
                                )
                                nonce_ok = True
                            except Exception:
                                pass

                        if nonce_ok:
                            continue

        return logs

    async def decrypt_txs_response(self, txs_response):
        nonces = {}

        decoded_tx = Tx.from_data(txs_response['tx'])
        for i, message in enumerate(decoded_tx.body.messages):
            msg_type = message.type_url
            msg_decoder = msg_decoder_mapper.get(msg_type)

            if not msg_decoder:
                continue

            msg = {
                'type_url': msg_type,
                'value': msg_decoder(message)
            }

            # Check if the message needs decryption
            contract_input_msg_field_name = ''
            if msg_type == "/secret.compute.v1beta1.MsgInstantiateContract":
                contract_input_msg_field_name = "initMsg";
            elif msg_type == "/secret.compute.v1beta1.MsgExecuteContract":
                contract_input_msg_field_name = "msg";

            if contract_input_msg_field_name != '':
                # Encrypted, try to decrypt
                try:
                    contract_input_msg_bytes = base64.b64decode(msg["value"][contract_input_msg_field_name])
                    nonce = contract_input_msg_bytes[0:32]
                    account_pub_key = contract_input_msg_bytes[32:64]
                    ciphertext = contract_input_msg_bytes[64:]

                    plaintext = await self._c.utils.decrypt(
                        ciphertext,
                        nonce
                    )
                    # first 64 chars is the code hash as hex string
                    msg["value"][contract_input_msg_field_name] = plaintext[64:]

                    # Fill nonces array to later use it in output decryption
                    nonces[i] = nonce
                except:
                    pass
                    # Not encrypted or can't decrypt because not original sender

            decoded_tx.body.messages[i] = msg

        raw_log = txs_response['tx_response']['raw_log']
        json_log = None
        array_log = None

        code = txs_response['tx_response']['code']
        if code == 0 and raw_log != '':
            json_log = json.loads(raw_log)

            for i, _ in enumerate(json_log):
                if 'msg_index' not in json_log[i] or not json_log[i]['msg_index']:
                    # See https://github.com/cosmos/cosmos-sdk/pull/11147
                    json_log[i]['msg_index'] = i

            array_log = await self.decrypt_logs(json_log, nonces)
        elif code != 0 and raw_log != '':
            try:
                error_message_rgx = re.compile(
                    rf'; message index: (\d+):(?: dispatch: submessages:)* encrypted: (.+?): (?:instantiate|execute|query|reply to) contract failed'
                )
                rgx_matches = error_message_rgx.findall(raw_log)
                if rgx_matches and len(rgx_matches) == 3:
                    msg_index = int(rgx_matches[1])
                    error_cipher_b64 = rgx_matches[2]
                    error_cipher_bz = base64.b64decode(error_cipher_b64)
                    error_plain_bz = await self._c.utils.decrypt(error_cipher_bz, nonces[msg_index])
                    raw_log = raw_log.replace(
                        f'encrypted: {rgx_matches[2]}', error_plain_bz
                    )

                    try:
                        json_log = json.loads(error_plain_bz)
                    except:
                        pass
            except:
                pass

        tx_msg_data = [bytearray.fromhex(txs_response['tx_response']['data'])]
        for i, data in enumerate(tx_msg_data):
            nonce = nonces.get(i)
            if nonce and len(nonces) == 32:
                # Check if the message needs decryption
                try:
                    msg_type = decoded_tx.body.messages[i].type_url
                    if msg_type == '/secret.compute.v1beta1.MsgInstantiateContract':
                        decoded = MsgInstantiateContractResponse(data['data'])
                        decrypted = await self.decrypt_data_field(data['data'], [nonce])
                        data[i] = MsgInstantiateContractResponse(
                            address=decoded.address,
                            data=decrypted
                        )
                    elif msg_type == '/secret.compute.v1beta1.MsgExecuteContract':
                        decoded = MsgExecuteContractResponse(data['data'])
                        decrypted = await self.decrypt_data_field(data['data'], [nonce])
                        data[i] = MsgExecuteContractResponse(
                            data=decrypted
                        )
                except:
                    pass

        tx_resp = txs_response['tx_response']
        return {
          'height': int(tx_resp['height']),
          'timestamp': tx_resp['timestamp'],
          'transactionHash': tx_resp['txhash'],
          'code': tx_resp['code'],
          'tx': decoded_tx,
          'txBytes': tx_resp['tx'].get('value'),
          'rawLog': raw_log,
          'jsonLog': json_log,
          'arrayLog': array_log,
          'events': tx_resp['events'],
          'data': data,
          'gasUsed': int(tx_resp['gas_used']),
          'gasWanted': int(tx_resp['gas_wanted']),
        }

    async def create(
        self,
        sender: AccAddress,
        msgs: List[Msg],
        fee: Optional[StdFee] = None,
        memo: str = "",
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        account_number: Optional[int] = None,
        sequence: Optional[int] = None,
    ) -> StdSignMsg:
        """Create a new unsigned transaction, with helpful utilities such as lookup of
        chain ID, account number, sequence and fee estimation.

        Args:
            sender (AccAddress): transaction sender's account address
            msgs (List[Msg]): list of messages to include
            fee (Optional[StdFee], optional): fee to use (estimates if empty).
            memo (str, optional): memo to use. Defaults to "".
            gas (Optional[int]): gas
            gas_prices (Optional[Coins.Input], optional): gas prices for fee estimation.
            gas_adjustment (Optional[Numeric.Input], optional): gas adjustment for fee estimation.
            fee_denoms (Optional[List[str]], optional): list of denoms to use for gas fee when estimating.
            account_number (Optional[int], optional): account number to use.
            sequence (Optional[int], optional): sequence number to use.

        Returns:
            StdSignMsg: unsigned tx
        """

        # create the fake fee
        if fee is None:
            fee = await BaseAsyncAPI._try_await(
                self.estimate_fee(gas, gas_prices, gas_adjustment, fee_denoms)
            )

        if account_number is None or sequence is None:
            account = await BaseAsyncAPI._try_await(self._c.auth.account_info(sender))
            if account_number is None:
                account_number = account.account_number
            if sequence is None:
                sequence = account.sequence

        return StdSignMsg(
            self._c.chain_id, account_number or 0, sequence or 0, fee, msgs, memo  # type: ignore
        )

    async def estimate_fee(
        self,
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
    ) -> StdFee:
        """Estimates the proper fee to apply by simulating it within the node.

        Args:
            gas (Optional[int]): gas
            gas_prices (Optional[Coins.Input], optional): gas prices to use.
            gas_adjustment (Optional[Numeric.Input], optional): gas adjustment to use.
            fee_denoms (Optional[List[str]], optional): list of denoms to use to pay for gas.

        Returns:
            StdFee: estimated fee
        """
        if gas is None or gas_prices is None:
            return self._c.custom_fees["default"]

        gas_prices = gas_prices or self._c.gas_prices
        gas_adjustment = gas_adjustment or self._c.gas_adjustment

        gas_prices_coins = None
        if gas_prices:
            gas_prices_coins = Coins(gas_prices)
            if fee_denoms:
                _fee_denoms: List[str] = fee_denoms  # satisfy mypy type checking :(
                gas_prices_coins = gas_prices_coins.filter(
                    lambda c: c.denom in _fee_denoms
                )
        fee_amount = gas_prices_coins.mul(gas * gas_adjustment)
        return StdFee(gas, fee_amount)

    async def encode(self, tx: StdTx, options: BroadcastOptions = None) -> str:
        """Fetches a transaction's amino encoding.

        Args:
            tx (StdTx): transaction to encode

        Returns:
            str: base64 string containing amino-encoded tx
        """
        data = tx.to_data()
        if options is not None:
            if options.sequences is not None and len(options.sequences) > 0:
                data["sequences"] = [str(i) for i in options.sequences]
            if options.fee_granter is not None and len(options.fee_granter) > 0:
                data["fee_granter"] = options.fee_granter

        res = await self._c._post("/txs/encode", data)
        return res["tx"]

    async def hash(self, tx: StdTx) -> str:
        """Compute hash for a transaction.

        Args:
            tx (StdTx): transaction to hash

        Returns:
            str: transaction hash
        """
        amino = await self.encode(tx)
        return hash_amino(amino)

    async def _broadcast(
        self, tx: StdTx, mode: str, options: BroadcastOptions = None
    ) -> dict:
        data = {"tx": tx.to_data()["value"], "mode": mode}
        if options is not None:
            if options.sequences is not None and len(options.sequences) > 0:
                data["sequences"] = [str(i) for i in options.sequences]
            if options.fee_granter is not None and len(options.fee_granter) > 0:
                data["fee_granter"] = options.fee_granter
        return await self._c._post("/txs", data)

    async def broadcast_sync(
        self, tx: StdTx, options: BroadcastOptions = None
    ) -> SyncTxBroadcastResult:
        """Broadcasts a transaction using the ``sync`` broadcast mode.

        Args:
            tx (StdTx): transaction to broadcast

        Returns:
            SyncTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "sync", options)
        return SyncTxBroadcastResult(
            txhash=res["txhash"],
            raw_log=res.get("raw_log"),
            code=res.get("code"),
            codespace=res.get("codespace"),
        )

    async def broadcast_async(
        self, tx: StdTx, options: BroadcastOptions = None
    ) -> AsyncTxBroadcastResult:
        """Broadcasts a transaction using the ``async`` broadcast mode.

        Args:
            tx (StdTx): transaction to broadcast

        Returns:
            AsyncTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "async", options)
        return AsyncTxBroadcastResult(
            txhash=res["txhash"],
        )

    async def broadcast(
        self, tx: StdTx, options: BroadcastOptions = None
    ) -> BlockTxBroadcastResult:
        """Broadcasts a transaction using the ``block`` broadcast mode.

        Args:
            tx (StdTx): transaction to broadcast

        Returns:
            BlockTxBroadcastResult: result
        """
        res = await self._broadcast(tx, "block", options)
        return BlockTxBroadcastResult(
            height=res.get("height") or 0,
            txhash=res["txhash"],
            raw_log=res.get("raw_log"),
            gas_wanted=res.get("gas_wanted") or 0,
            gas_used=res.get("gas_used") or 0,
            logs=res.get("logs"),
            code=res.get("code"),
            codespace=res.get("codespace"),
        )

    async def search(
        self, events: List[list], params: Optional[APIParams] = None
    ) -> dict:
        """Searches for transactions given criteria.

        Args:
            events (dict): dictionary containing options
            params (APIParams): optional parameters

        Returns:
            dict: transaction search results
        """

        actual_params = CIMultiDict()

        for event in events:
            if event == "tx.height":
                actual_params.add("events", f"{event}={events[event]}")
            else:
                actual_params.add("events", f"{event}='{events[event]}'")
        if params:
            for p in params:
                actual_params.add(p, params[p])

        res = await self._c._get("/cosmos/tx/v1beta1/txs", actual_params)
        return {
            "txs": [TxInfo.from_data(tx) for tx in res.get("tx_responses")],
            "pagination": res.get("pagination"),
        }

    async def tx_infos_by_height(self, height: Optional[int] = None) -> List[TxInfo]:
        """Fetches information for an included transaction given block height or latest

        Args:
            height (int, optional): height to lookup. latest if height is None.

        Returns:
            List[TxInfo]: transaction info
        """
        if height is None:
            x = "latest"
        else:
            x = height

        res = await self._c._get(f"/cosmos/base/tendermint/v1beta1/blocks/{x}")

        txs = res.get("block").get("data").get("txs")
        hashes = [hash_amino(tx) for tx in txs]
        return [
            await BaseAsyncAPI._try_await(self.tx_info(tx_hash)) for tx_hash in hashes
        ]


class TxAPI(AsyncTxAPI):
    @sync_bind(AsyncTxAPI.tx_info)
    def tx_info(self, tx_hash: str) -> TxInfo:
        pass

    tx_info.__doc__ = AsyncTxAPI.tx_info.__doc__

    @sync_bind(AsyncTxAPI.tx_by_id)
    def tx_by_id(self, tx_hash: str) -> TxInfo:
        pass

    tx_by_id.__doc__ = AsyncTxAPI.tx_by_id.__doc__

    @sync_bind(AsyncTxAPI.create)
    def create(
        self,
        sender: AccAddress,
        msgs: List[Msg],
        fee: Optional[StdFee] = None,
        memo: str = "",
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
        account_number: Optional[int] = None,
        sequence: Optional[int] = None,
    ) -> StdSignMsg:
        pass

    create.__doc__ = AsyncTxAPI.create.__doc__

    @sync_bind(AsyncTxAPI.estimate_fee)
    def estimate_fee(
        self,
        gas: Optional[int] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        fee_denoms: Optional[List[str]] = None,
    ) -> StdFee:
        pass

    estimate_fee.__doc__ = AsyncTxAPI.estimate_fee.__doc__

    @sync_bind(AsyncTxAPI.encode)
    def encode(self, tx: StdTx, options: BroadcastOptions = None) -> str:
        pass

    encode.__doc__ = AsyncTxAPI.encode.__doc__

    @sync_bind(AsyncTxAPI.hash)
    def hash(self, tx: StdTx) -> str:
        pass

    hash.__doc__ = AsyncTxAPI.hash.__doc__

    @sync_bind(AsyncTxAPI.broadcast_sync)
    def broadcast_sync(
        self, tx: StdTx, options: BroadcastOptions = None
    ) -> SyncTxBroadcastResult:
        pass

    broadcast_sync.__doc__ = AsyncTxAPI.broadcast_sync.__doc__

    @sync_bind(AsyncTxAPI.broadcast_async)
    def broadcast_async(
        self, tx: StdTx, options: BroadcastOptions = None
    ) -> AsyncTxBroadcastResult:
        pass

    broadcast_async.__doc__ = AsyncTxAPI.broadcast_async.__doc__

    @sync_bind(AsyncTxAPI.broadcast)
    def broadcast(
        self, tx: StdTx, options: BroadcastOptions = None
    ) -> BlockTxBroadcastResult:
        pass

    broadcast.__doc__ = AsyncTxAPI.broadcast.__doc__

    @sync_bind(AsyncTxAPI.search)
    def search(self, events: List[list], params: Optional[APIParams] = None) -> dict:
        pass

    search.__doc__ = AsyncTxAPI.search.__doc__

    @sync_bind(AsyncTxAPI.tx_infos_by_height)
    def tx_infos_by_height(self, height: Optional[int] = None) -> List[TxInfo]:
        pass

    tx_infos_by_height.__doc__ = AsyncTxAPI.tx_infos_by_height.__doc__
