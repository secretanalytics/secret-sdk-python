import base64
import json
from typing import Any, Optional

from secret_sdk.client.lcd.api._base import BaseAsyncAPI, sync_bind
from secret_sdk.core.coins import Coins
from secret_sdk.core.wasm.msgs import AccAddress, MsgExecuteContract

__all__ = ["AsyncWasmAPI", "WasmAPI"]

_contract_code_hash = {}


class AsyncWasmAPI(BaseAsyncAPI):
    async def list_code_info(self) -> list:
        """Fetches information about uploaded codes.

        Returns:
            list: codes information
        """
        return await self._c._get("/wasm/code") or []

    async def code_info(self, code_id: int) -> dict:
        """Fetches information about an uploaded code.

        Args:
            code_id (int): code ID

        Returns:
            dict: code information
        """
        return await self._c._get(f"/wasm/code/{code_id}")

    async def list_contracts_by_code_id(self, code_id: int) -> list:
        """Fetches information about an uploaded code.

        Args:
            code_id (int): code ID

        Returns:
            dict: code information
        """
        return await self._c._get(f"/wasm/code/{code_id}/contracts") or []

    async def contract_info(self, contract_address: str) -> dict:
        """Fetches information about an instantiated contract.

        Args:
            contract_address (str): contract address

        Returns:
            dict: contract information
        """
        res = await self._c._get(f"/wasm/contract/{contract_address}")
        return res

    async def contract_hash_by_code_id(self, code_id: int) -> str:
        """Fetches contract hash from an instantiated contract using its code id

        Args:
            code_id (int): contract code id

        Returns:
            dict: contract hash
        """
        contract_code_hash = await self._c._get(f"/wasm/code/{code_id}/hash")
        return contract_code_hash

    async def contract_hash(self, contract_address: str) -> str:
        """Fetches information about an instantiated contract.

        Args:
            contract_address (str): contract address

        Returns:
            dict: contract hash
        """

        if contract_address not in _contract_code_hash:
            contract_code_hash = await self._c._get(
                f"/wasm/contract/{contract_address}/code-hash"
            )
            _contract_code_hash[contract_address] = contract_code_hash
        return _contract_code_hash[contract_address]

    async def contract_query(
        self, contract_address: str, query: dict, height: Optional[int] = 0
    ) -> Any:
        """Runs a QueryMsg on a contract.

        Args:
            contract_address (str): contract address
            query_msg (dict): QueryMsg to run

        Returns:
            Any: results of query
        """
        query_str = json.dumps(query, separators=(",", ":"))
        contract_code_hash = await BaseAsyncAPI._try_await(
            self.contract_hash(contract_address)
        )
        encrypted = await BaseAsyncAPI._try_await(
            self._c.utils.encrypt(contract_code_hash, query_str)
        )

        nonce = encrypted[0:32]
        encoded = base64.b64encode(bytes(encrypted)).hex()
        query_path = f"/wasm/contract/{contract_address}/query/{encoded}?encoding=hex&height={height}"

        query_result = await BaseAsyncAPI._try_await(self._c._get(query_path))
        encoded_result = base64.b64decode(bytes(query_result["smart"], "utf-8"))
        decrypted = await BaseAsyncAPI._try_await(
            self._c.utils.decrypt(encoded_result, nonce)
        )
        return json.loads(base64.b64decode(decrypted))

    async def contract_execute_msg(
        self,
        sender_address: AccAddress,
        contract_address: AccAddress,
        handle_msg: dict,
        transfer_amount: Optional[Coins] = None,
    ) -> MsgExecuteContract:
        msg_str = json.dumps(handle_msg, separators=(",", ":"))
        contract_code_hash = await BaseAsyncAPI._try_await(
            self.contract_hash(contract_address)
        )

        encrypted_msg = await BaseAsyncAPI._try_await(
            self._c.utils.encrypt(contract_code_hash, msg_str)
        )
        encrypted_msg = base64.b64encode(bytes(encrypted_msg)).decode()
        return MsgExecuteContract(
            sender_address, contract_address, encrypted_msg, transfer_amount
        )


class WasmAPI(AsyncWasmAPI):
    @sync_bind(AsyncWasmAPI.list_code_info)
    def list_code_info(self) -> list:
        pass

    list_code_info.__doc__ = AsyncWasmAPI.list_code_info.__doc__

    @sync_bind(AsyncWasmAPI.code_info)
    def code_info(self, code_id: int) -> dict:
        pass

    code_info.__doc__ = AsyncWasmAPI.code_info.__doc__

    @sync_bind(AsyncWasmAPI.list_contracts_by_code_id)
    def list_contracts_by_code_id(self, code_id: int) -> list:
        pass

    list_contracts_by_code_id.__doc__ = AsyncWasmAPI.list_contracts_by_code_id.__doc__

    @sync_bind(AsyncWasmAPI.contract_info)
    def contract_info(self, contract_address: str) -> dict:
        pass

    contract_info.__doc__ = AsyncWasmAPI.contract_info.__doc__

    @sync_bind(AsyncWasmAPI.contract_hash_by_code_id)
    def contract_hash_by_code_id(self, code_id: int) -> dict:
        pass

    contract_hash_by_code_id.__doc__ = AsyncWasmAPI.contract_hash_by_code_id.__doc__

    @sync_bind(AsyncWasmAPI.contract_hash)
    def contract_hash(self, contract_address: str) -> dict:
        pass

    contract_hash.__doc__ = AsyncWasmAPI.contract_hash.__doc__

    @sync_bind(AsyncWasmAPI.contract_query)
    def contract_query(
        self, contract_address: str, query_msg: dict, height: Optional[int] = 0
    ) -> Any:
        pass

    contract_query.__doc__ = AsyncWasmAPI.contract_query.__doc__

    @sync_bind(AsyncWasmAPI.contract_execute_msg)
    def contract_execute_msg(
        self,
        sender_address: AccAddress,
        contract_address: AccAddress,
        handle_msg: dict,
        transfer_amount: Coins,
    ) -> MsgExecuteContract:
        pass

    contract_execute_msg.__doc__ = AsyncWasmAPI.contract_execute_msg.__doc__
