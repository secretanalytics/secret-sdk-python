import base64
import re
from typing import List, Optional

import attr

from secret_sdk.core import AccAddress, Coins, Numeric
from secret_sdk.core.auth import SearchTxsResponse, StdFee, StdSignMsg, StdTx, TxInfo
from secret_sdk.core.broadcast import (
    AsyncTxBroadcastResult,
    BlockTxBroadcastResult,
    SyncTxBroadcastResult,
)
from secret_sdk.core.msg import Msg
from secret_sdk.util.hash import hash_amino

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncTxAPI", "TxAPI", "BroadcastOptions"]


@attr.s
class BroadcastOptions:
    sequences: Optional[List[int]] = attr.ib()
    fee_granter: Optional[AccAddress] = attr.ib(default=None)


class AsyncTxAPI(BaseAsyncAPI):
    async def tx_info(self, tx_hash: str) -> TxInfo:
        """Fetches information for an included transaction given a tx hash.

        Args:
            tx_hash (str): hash of transaction to lookup

        Returns:
            TxInfo: transaction info
        """
        return TxInfo.from_data(await self._c._get(f"/txs/{tx_hash}", raw=True))

    async def tx_by_id(self, id: str) -> TxInfo:
        """Fetches information for an included transaction given a tx hash.

        Args:
            tx_hash (str): hash of transaction to lookup

        Returns:
            TxInfo: transaction info
        """
        response_data = await self._c._get(f"/txs/{id}", raw=True)
        if "tx" not in response_data:
            raise Exception("Unexpected response data format")
        # TODO: update TxInfo interface
        return await self.decrypt_txs_response(response_data)

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
        data_field = None
        data = []

        if txs_response.get("data"):
            data_field = txs_response[
                "data"
            ]  # await self.decode_tx_data(txs_response['data'])

        logs = txs_response.get("logs")
        if logs:
            logs[0]["msg_index"] = 0

        for i, msg in enumerate(txs_response["tx"]["value"].get("msg")):

            if msg["type"] == "wasm/MsgExecuteContract":
                input_msg_encrypted = base64.b64decode(msg["value"]["msg"])
            elif msg["type"] == "wasm/MsgInstantiateContract":
                input_msg_encrypted = base64.b64decode(msg["value"]["init_msg"])
            else:
                continue

            input_msg_pubkey = input_msg_encrypted[32:64]
            pub_key = await self._c.utils.get_pub_key()
            if base64.b64encode(pub_key) == base64.b64encode(input_msg_pubkey):
                # my pubkey, can decrypt
                nonce = input_msg_pubkey[0:32]

                # decrypt input
                input_msg = await self._c.utils.decrypt(input_msg_encrypted[:64], nonce)

                if msg["type"] == "wasm/MsgExecuteContract":
                    # decrypt input
                    txs_response["tx"]["value"]["msg"][i]["value"]["msg"] = input_msg

                    # decrypt output data
                    # hack since only 1st message data is returned
                    if data_field and i == 0 and data_field[0]["data"]:
                        data = await self.decrypt_data_field(
                            bytearray.fromhex(base64.b64decode(data_field[0]["data"])),
                            [nonce],
                        )
                elif msg.type == "wasm/MsgInstantiateContract":
                    # decrypt input
                    txs_response["tx"]["value"]["msg"][0]["value"][
                        "init_msg"
                    ] = input_msg

                # decrypt output logs
                if txs_response.get("logs") and logs:
                    if "log" not in txs_response["logs"][i]:
                        logs[i]["log"] = ""
                    logs[i] = await self.decrypt_logs(
                        [txs_response["logs"][i]], [nonce]
                    )[0]

                # failed to execute message; message index: 0: encrypted: (.+?): (?:instantiate | execute | query) contract failed
                # decrypt error const
                error_message_rgx = re.compile(
                    rf"failed to execute message; message index: {i}: encrypted: (.+?): (?:instantiate|execute|query) contract failed"
                )
                rgx_matches = error_message_rgx.findall(txs_response["raw_log"])
                if rgx_matches and len(rgx_matches) == 2:
                    error_cipher_b64 = rgx_matches[1]
                    error_cipher_bz = base64.b64decode(error_cipher_b64)
                    error_plain_bz = await self._c.utils.decrypt(error_cipher_bz, nonce)
                    txs_response["raw_log"] = txs_response["raw_log"].replace(
                        error_cipher_b64, error_plain_bz
                    )

        txs_response = {k: v for k, v in txs_response.items()}
        txs_response["logs"] = logs
        txs_response["data"] = data

        return txs_response

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
        return await self._c._post("/txs", data, raw=True)

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

    async def search(self, options: dict = {}) -> SearchTxsResponse:
        """Searches for transactions given criteria.

        Args:
            options (dict, optional): dictionary containing options. Defaults to {}.

        Returns:
            dict: transaction search results
        """
        res = await self._c._get("/txs", options, raw=True)
        return SearchTxsResponse.from_data(res)


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
    def search(self, options: dict = {}) -> SearchTxsResponse:
        pass

    search.__doc__ = AsyncTxAPI.search.__doc__
