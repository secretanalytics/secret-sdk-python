import asyncio
import base64
import json
import re
from dataclasses import dataclass
from typing import List

import bech32
from grpclib.client import Channel

from ..encryption import EncryptionUtils
from ..protobuf.secret.compute.v1beta1 import CodeInfoResponse as baseCodeInfoResponse
from ..protobuf.secret.compute.v1beta1 import ContractInfo as baseContractInfo
from ..protobuf.secret.compute.v1beta1 import QueryStub as computeQueryStub

"""
most of the code below is copied from secret.js impl: https://github.com/scrtlabs/secret.js/blob/master/src/query/compute.ts
notes from them: 
For future wanderers:
This file is written manually with a few goals in mind:
1. Proxy the auto-generated QueryClientImpl from "src/protobuf_stuff/secret/compute/v1beta1/query.tx" (See the "scripts/generate_protobuf.sh" script)
2. Abstract "address: Uint8Array" in the underlying types as "address: string".
3. Add Secret Network encryption
"""


@dataclass(eq=False, repr=False)
class AbsoluteTxPosition:
    """AbsoluteTxPosition can be used to sort contracts"""

    # BlockHeight is the block the contract was created at
    block_height: str

    # TxIndex is a monotonic counter within the block (actual transaction index,
    tx_index: str


@dataclass(eq=False, repr=False)
class ContractInfo:
    """ContractInfo stores a WASM contract instance"""

    code_id: int
    creator: str
    label: str
    created: AbsoluteTxPosition


@dataclass(eq=False, repr=False)
class QueryContractInfoResponse:
    """QueryContractInfoResponse is the response type for the Query/ContractInfo RPC method"""

    # address is the address of the contract
    address: str
    ContractInfo: ContractInfo


@dataclass(eq=False, repr=False)
class CodeInfoResponse:
    code_id: str
    creator: str
    code_hash: str
    source: str
    builder: str


@dataclass(eq=False, repr=False)
class ContractInfoWithAddress:
    """ContractInfoWithAddress adds the address (key) to the ContractInfo representation"""

    address: str
    ContractInfo: ContractInfo


@dataclass(eq=False, repr=False)
class QueryContractsByCodeResponse:
    contract_infos: List[ContractInfoWithAddress]


@dataclass(eq=False, repr=False)
class QueryCodeResponse:
    code_info: CodeInfoResponse
    daa: bytes


class ComputeQuerier:
    def __init__(self, channel: Channel):
        self.client = computeQueryStub(channel)
        self.encryption = EncryptionUtils(channel._host, channel._port)
        self.code_hash_cache = {}

    async def contract_code_hash(self, address: str) -> str:
        """Get codeHash of a Secret Contract"""
        code_hash = self.code_hash_cache.get(address)
        if not code_hash:
            contract_info = await self.contract_info(address)
            code_hash = (
                (await self.code_hash(contract_info.code_id)).replace("0x", "").lower()
            )
            self.code_hash_cache[address] = code_hash

        return code_hash

    async def code_hash(self, code_id: int) -> str:
        """Get codeHash from code id"""
        code_hash = self.code_hash_cache.get(code_id)

        if not code_hash:
            code_info = await self.code(code_id)

    async def contract_info(self, address: str) -> QueryContractInfoResponse:
        response = await self.client.contract_info(
            address=ComputeQuerier.address_to_bytes(address)
        )
        print(response)

        return QueryContractInfoResponse(
            address=ComputeQuerier.bytes_to_address(response.address),
            ContractInfo=ComputeQuerier.contract_info_from_protobuf(
                response.ContractInfo
            ),
        )

    async def contracts_by_code(self, code_id: int = 1) -> QueryContractsByCodeResponse:
        response = await self.client.contracts_by_code(code_id=code_id)
        print(response)
        print("\n")
        address_bytes = list(response.contract_infos[0].address)
        print(address_bytes)
        print(ComputeQuerier.bytes_to_address(address_bytes))

        return QueryContractsByCodeResponse(
            contract_infos=[
                print(list(contract.address))
                # ContractInfo(
                #     address=ComputeQuerier.bytes_to_address(contract.address),
                #     ContractInfo=ComputeQuerier.contract_info_from_protobuf(
                #         contract.ContractInfo
                #     )
                #     if contract.ContractInfo
                #     else None,
                # )
                for contract in response.contract_infos
            ]
        )

    async def query_contract(self, contract_address: str, query: json):

        # code hash was an arugment in secret.js but I thought it was easier to just pull in manually
        code_hash = await self.contract_code_hash(contract_address)

        code_hash = code_hash.replace("0x", "").lower()

        encrypted_query = await self.encryption.encrypt(code_hash, query)
        nonce = encrypted_query[0:32]

        encrypted_result = await self.client.smart_contract_state(
            address=ComputeQuerier.address_to_bytes(contract_address),
            query_data=encrypted_query,
        )
        decrypted_b64_result = await self.encryption.decrypt(encrypted_result, nonce)

        return json.loads(base64.b64decode(decrypted_b64_result))

    async def code(self, code_id: int) -> QueryCodeResponse:
        response = await self.client.code(code_id=code_id)
        code_info = ComputeQuerier.code_info_response_from_protobuf(response.code_info)

        self.code_hash_cache[code_id] = code_info.replace("0x", "").lower()

        return QueryCodeResponse(code_info=code_info, data=response.data)

    async def codes(self) -> List[CodeInfoResponse]:
        response = await self.client.codes()
        return [
            ComputeQuerier.code_info_response_from_protobuf(codeInfo)
            for codeInfo in response.code_infos
        ]

    def address_to_bytes(address: str) -> bytes:
        hrp, bytes = bech32.bech32_decode(address)
        return bytes

    def bytes_to_address(bytes: bytes, prefix: str = "secret") -> str:
        res = bech32.bech32_encode(prefix, bytes)
        return res

    ## following functions convert from base protobuf responses to this levels formats
    def contract_info_from_protobuf(contractInfo: baseContractInfo) -> ContractInfo:
        return ContractInfo(
            code_id=contractInfo.code_id,
            creator=ComputeQuerier.bytes_to_address(contractInfo.creator),
            label=contractInfo.label,
            created=contractInfo.created,
        )

    def code_info_response_from_protobuf(
        codeInfo: baseCodeInfoResponse,
    ) -> baseCodeInfoResponse:
        # this should never be empty strings
        return CodeInfoResponse(
            code_id=codeInfo.code_id if codeInfo.code_id else "",
            creator=ComputeQuerier.bytes_to_address(codeInfo.creator)
            if codeInfo.creator
            else "",
            code_hash=codeInfo.data_hash.decode().replace("0x", "").lower()
            if codeInfo.dash_hash
            else "",
            source=codeInfo.source if codeInfo.source else "",
            builder=codeInfo.builder if codeInfo.builder else "",
        )
