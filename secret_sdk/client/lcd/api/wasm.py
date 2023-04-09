import base64
import json
import re
from typing import Any, Optional
from secret_sdk.exceptions import LCDResponseError

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
        return await self._c._get("/compute/v1beta1/codes") or []

    async def code_info(self, code_id: int) -> dict:
        """Fetches information about an uploaded code.

        Args:
            code_id (int): code ID

        Returns:
            dict: code information
        """
        return await self._c._get(f"/compute/v1beta1/code/{code_id}")

    async def list_contracts_by_code_id(self, code_id: int) -> list:
        """Fetches information about an uploaded code.

        Args:
            code_id (int): code ID

        Returns:
            dict: code information
        """
        return await self._c._get(f"/compute/v1beta1/code/{code_id}") or []

    async def contract_info(self, contract_address: str) -> dict:
        """Fetches information about an instantiated contract.

        Args:
            contract_address (str): contract address

        Returns:
            dict: contract information
        """
        res = await self._c._get(f"/compute/v1beta1/info/{contract_address}")
        return res

    async def code_hash_by_code_id(self, code_id: int) -> dict:
        """ Query code hash by code id
        :param code_id: int
        :return: query code hash response
        """
        res = await self._c._get(f"/compute/v1beta1/code_hash/by_code_id/{code_id}")
        return res

    async def contract_hash(self, contract_address: str) -> str:
        """Fetches information about an instantiated contract.

        Args:
            contract_address (str): contract address

        Returns:
            dict: contract hash
        """

        if contract_address not in _contract_code_hash:
            contract_code_hash = await self._c._get(
                f"/compute/v1beta1/code_hash/by_contract_address/{contract_address}"
            )
            _contract_code_hash[contract_address] = contract_code_hash['code_hash']
        return _contract_code_hash[contract_address]

    async def contract_query(
            self, contract_address: str, query: dict, contract_code_hash: Optional[str] = None,
            height: Optional[int] = 0, timeout: Optional[int] = 15, retry_attempts: Optional[int] = 1
    ) -> Any:
        """Runs a QueryMsg on a contract.

        Args:
            contract_address (str): contract address
            query_msg (dict): QueryMsg to run

        Returns:
            Any: results of query
        """
        query_str = json.dumps(query, separators=(",", ":"))
        if not contract_code_hash:
            if contract_address not in _contract_code_hash:
                contract_code_hash = await BaseAsyncAPI._try_await(
                    self.contract_hash(contract_address)
                )
                _contract_code_hash[contract_address] = contract_code_hash
            else:
                contract_code_hash = _contract_code_hash[contract_address]
        encrypted = self._c.encrypt_utils.encrypt(contract_code_hash, query_str)
        # first 32 bytes are the nonce
        nonce = encrypted[0:32]
        # base64 over the wire
        params = {
            'contract_address': contract_address,
            'query': base64.b64encode(bytes(encrypted)).decode('utf-8')
        }
        if height:
            params['block_height'] = str(height)

        query_path = f"/compute/v1beta1/query/{contract_address}"
        try:
            query_result = await BaseAsyncAPI._try_await(
                self._c._get(query_path, params=params, timeout=timeout, retry_attempts=retry_attempts)
            )
        except LCDResponseError as lcd_error:
            # trying to decrypt error
            error_json = json.loads(lcd_error.message.replace("'", '"'))
            error_msg = error_json.get('message','')
            encrypted_error = re.findall('encrypted: (.+?):', error_msg)
            if encrypted_error:
                decrypted_error = self._c.encrypt_utils.decrypt(base64.b64decode(bytes(encrypted_error[0], 'utf-8')), nonce)
                lcd_error.message = decrypted_error.decode('utf-8')
            raise lcd_error
        except:
            raise

        encoded_result = base64.b64decode(bytes(query_result["data"], "utf-8"))
        decrypted = self._c.encrypt_utils.decrypt(encoded_result, nonce)
        return json.loads(base64.b64decode(decrypted))

    async def contract_execute_msg(
            self,
            sender_address: AccAddress,
            contract_address: AccAddress,
            handle_msg: dict,
            transfer_amount: Optional[Coins] = None,
            contract_code_hash: Optional[str] = None
    ) -> MsgExecuteContract:
        if not contract_code_hash:
            if contract_address not in _contract_code_hash:
                contract_code_hash = await BaseAsyncAPI._try_await(
                    self.contract_hash(contract_address)
                )
                _contract_code_hash[contract_address] = contract_code_hash
            else:
                contract_code_hash = _contract_code_hash[contract_address]
        return MsgExecuteContract(
            sender_address, contract_address, msg=handle_msg, sent_funds=transfer_amount, code_hash=contract_code_hash,
            encryption_utils=self._c.encrypt_utils
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

    @sync_bind(AsyncWasmAPI.contract_hash)
    def contract_hash(self, contract_address: str) -> dict:
        pass

    contract_hash.__doc__ = AsyncWasmAPI.contract_hash.__doc__

    @sync_bind(AsyncWasmAPI.code_hash_by_code_id)
    def code_hash_by_code_id(self, code_info: int) -> dict:
        pass

    code_hash_by_code_id.__doc__ = AsyncWasmAPI.code_hash_by_code_id.__doc__

    @sync_bind(AsyncWasmAPI.contract_query)
    def contract_query(
            self, contract_address: str, query_msg: dict, contract_code_hash: Optional[str] = None,
            height: Optional[int] = 0, timeout: Optional[int] = 15, retry_attempts: Optional[int] = 1
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
            contract_code_hash: str
    ) -> MsgExecuteContract:
        pass

    contract_execute_msg.__doc__ = AsyncWasmAPI.contract_execute_msg.__doc__
