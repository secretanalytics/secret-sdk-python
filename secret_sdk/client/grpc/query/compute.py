import json
import base64
from grpclib.client import Channel

from ..grpc_utils import EmptyRequest
from ..encryption import EncryptionUtils
from ..protobuf.secret.compute.v1beta1 import QueryStub as computeQueryStub
from ..protobuf.secret.compute.v1beta1 import QueryByContractAddressRequest, QueryByCodeIdRequest, \
    QuerySecretContractRequest
from ..protobuf.secret.compute.v1beta1 import QueryContractInfoResponse, QueryContractsByCodeIdResponse, \
    QueryCodeResponse, QueryCodesResponse, QuerySecretContractResponse


class ComputeQuerier:
    def __init__(
        self,
        channel: Channel,
    ):
        self.client = computeQueryStub(channel)
        self.encryption = EncryptionUtils(channel)
        self.code_hash_cache = {}

    async def contract_code_hash(self, address: str) -> str:
        """Get codeHash of a Secret Contract"""
        code_hash = self.code_hash_cache.get(address)
        if not code_hash:
            contract_info_response = await self.contract_info(address)
            contract_info = contract_info_response.contract_info
            code_hash = await self.code_hash(contract_info.code_id)

        return code_hash

    async def code_hash(self, code_id: int) -> str:
        """Get codeHash from code id"""
        code_hash = self.code_hash_cache.get(code_id)

        if not code_hash:
            code_info_response = await self.code(code_id)
            code_hash = code_info_response.code_info.code_hash.replace("0x", "").lower()
            code_hash = self.code_hash_cache[code_id] = code_hash

        return code_hash

    async def contract_info(self, address: str) -> QueryContractInfoResponse:
        query_contract_info_response = await self.client.contract_info(
            QueryByContractAddressRequest(contract_address=address)
        )
        return query_contract_info_response

    async def contracts_by_code(self, code_id: int = 1) -> QueryContractsByCodeIdResponse:
        raise NotImplementedError
        query_contracts_by_code_response = await self.client.contracts_by_code_id(
            QueryByCodeIdRequest(code_id=code_id)
        )

        return query_contracts_by_code_response

    async def query_contract(self, contract_address: str, query: json, code_hash: str = None) -> QuerySecretContractResponse:
        if code_hash is None:
            code_hash = await self.contract_code_hash(contract_address)

        encrypted_query = await self.encryption.encrypt(code_hash, query)
        nonce = encrypted_query[0:32]

        query_secret_contract_response_encrypted = await self.client.query_secret_contract(
            QuerySecretContractRequest(
                contract_address=contract_address,
                query=bytes(encrypted_query)
            )
        )
        decrypted_b64_result = await self.encryption.decrypt(
            query_secret_contract_response_encrypted.data,
            nonce
        )
        query_secret_contract_response = QuerySecretContractResponse(json.loads(base64.b64decode(decrypted_b64_result)))
        return query_secret_contract_response

    async def code(self, code_id: int) -> QueryCodeResponse:
        query_code_response = await self.client.code(
            QueryByCodeIdRequest(code_id=code_id)
        )
        return query_code_response

    async def codes(self) -> QueryCodesResponse:
        query_codes_response = await self.client.codes(EmptyRequest())
        return query_codes_response
