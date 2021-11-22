import base64
import json
from typing import Any, Optional
from terra_sdk.core.coins import Coins
from terra_sdk.client.lcd.api._base import BaseAsyncAPI, sync_bind
from terra_sdk.core.wasm.msgs import MsgExecuteContract, AccAddress
__all__ = ["AsyncWasmAPI", "WasmAPI"]

_contract_code_hash = {}
class AsyncWasmAPI(BaseAsyncAPI):
    async def code_info(self, code_id: int) -> dict:
        """Fetches information about an uploaded code.

        Args:
            code_id (int): code ID

        Returns:
            dict: code information
        """
        return await self._c._get(f"/wasm/codes/{code_id}")

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

        # if contract_address in _contract_code_hash: return _contract_code_hash.get(contract_address)
        contract_code_hash = await self._c._get(f"/wasm/contract/{contract_address}/code-hash")
        # _contract_code_hash[contract_address] = contract_code_hash
        # if not contract_code_hash:
        #     raise ValueError(f'contract hash not found for {contract_address}')
        return contract_code_hash

    async def contract_query(self, contract_address: str, query: dict, height: Optional[int] = 0) -> Any:
        """Runs a QueryMsg on a contract.

        Args:
            contract_address (str): contract address
            query_msg (dict): QueryMsg to run

        Returns:
            Any: results of query
        """
        query_str = json.dumps(query, separators=(",", ":"))
        contract_code_hash = await BaseAsyncAPI._try_await(self.contract_hash(contract_address))
        encrypted = await BaseAsyncAPI._try_await( self._c.utils.encrypt(contract_code_hash, query_str))
        nonce = encrypted[0:32]
        encoded = base64.b64encode(bytes(encrypted)).hex()
        query_path = f'/wasm/contract/{contract_address}/query/{encoded}?encoding=hex&height={height}'
        query_result = await BaseAsyncAPI._try_await(self._c._get(query_path))
        encoded_result = base64.b64decode(bytes(query_result['smart'], 'utf-8'))
        decrypted = await BaseAsyncAPI._try_await(self._c.utils.decrypt(encoded_result, nonce))
        return json.loads(base64.b64decode(decrypted))

    async def contract_execute_msg(self, sender_address: AccAddress, contract_address: AccAddress, handle_msg: dict,
                                   transfer_amount: Optional[Coins] = None) -> MsgExecuteContract :
        contract_code_hash = await BaseAsyncAPI._try_await(self.contract_hash(contract_address))
        msg_str = json.dumps(handle_msg, separators=(",", ":"))
        encrypted_msg = await BaseAsyncAPI._try_await( self._c.utils.encrypt(contract_code_hash, msg_str))
        encrypted_msg = base64.b64encode(bytes(encrypted_msg)).decode()
        return MsgExecuteContract(sender_address, contract_address, encrypted_msg, transfer_amount)

    async def parameters(self) -> dict:
        """Fetches the Wasm module parameters.

        Returns:
            dict: Wasm module parameters
        """
        return await self._c._get("/wasm/parameters")


class WasmAPI(AsyncWasmAPI):
    @sync_bind(AsyncWasmAPI.code_info)
    def code_info(self, code_id: int) -> dict:
        pass

    code_info.__doc__ = AsyncWasmAPI.code_info.__doc__

    @sync_bind(AsyncWasmAPI.contract_info)
    def contract_info(self, contract_address: str) -> dict:
        pass

    contract_info.__doc__ = AsyncWasmAPI.contrat_info.__doc__

    @sync_bind(AsyncWasmAPI.contract_hash_by_code_id)
    def contract_hash_by_code_id(self, code_id: int) -> dict:
        pass

    contract_hash_by_code_id.__doc__ = AsyncWasmAPI.contract_hash_by_code_id.__doc__

    @sync_bind(AsyncWasmAPI.contract_hash)
    def contract_hash(self, contract_address: str) -> dict:
        pass

    contract_hash.__doc__ = AsyncWasmAPI.contract_hash.__doc__

    @sync_bind(AsyncWasmAPI.contract_query)
    def contract_query(self, contract_address: str, query_msg: dict, height: Optional[int] = 0) -> Any:
        pass

    contract_query.__doc__ = AsyncWasmAPI.contract_query.__doc__

    @sync_bind(AsyncWasmAPI.parameters)
    def parameters(self) -> dict:
        pass

    parameters.__doc__ = AsyncWasmAPI.parameters.__doc__

    @sync_bind(AsyncWasmAPI.contract_execute_msg)
    def contract_execute_msg(self, sender_address: AccAddress, contract_address: AccAddress, handle_msg: dict,
                             transfer_amount: Coins) -> MsgExecuteContract:
        pass
    contract_execute_msg.__doc__ = AsyncWasmAPI.contract_execute_msg.__doc__
