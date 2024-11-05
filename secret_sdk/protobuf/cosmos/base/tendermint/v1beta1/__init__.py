# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: cosmos/base/tendermint/v1beta1/query.proto, cosmos/base/tendermint/v1beta1/types.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
)

import betterproto
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase

from .....tendermint import (
    p2p as ____tendermint_p2_p__,
    types as ____tendermint_types__,
    version as ____tendermint_version__,
)
from ...query import v1beta1 as __query_v1_beta1__


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


@dataclass(eq=False, repr=False)
class Block(betterproto.Message):
    """
    Block is tendermint type Block, with the Header proposer address field
    converted to bech32 string.
    """

    header: "Header" = betterproto.message_field(1)
    data: "____tendermint_types__.Data" = betterproto.message_field(2)
    evidence: "____tendermint_types__.EvidenceList" = betterproto.message_field(3)
    last_commit: "____tendermint_types__.Commit" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class Header(betterproto.Message):
    """Header defines the structure of a Tendermint block header."""

    version: "____tendermint_version__.Consensus" = betterproto.message_field(1)
    """basic block info"""

    chain_id: str = betterproto.string_field(2)
    height: int = betterproto.int64_field(3)
    time: datetime = betterproto.message_field(4)
    last_block_id: "____tendermint_types__.BlockId" = betterproto.message_field(5)
    """prev block info"""

    last_commit_hash: bytes = betterproto.bytes_field(6)
    """hashes of block data"""

    data_hash: bytes = betterproto.bytes_field(7)
    validators_hash: bytes = betterproto.bytes_field(8)
    """hashes from the app output from the prev block"""

    next_validators_hash: bytes = betterproto.bytes_field(9)
    consensus_hash: bytes = betterproto.bytes_field(10)
    app_hash: bytes = betterproto.bytes_field(11)
    last_results_hash: bytes = betterproto.bytes_field(12)
    evidence_hash: bytes = betterproto.bytes_field(13)
    """consensus info"""

    proposer_address: str = betterproto.string_field(14)
    """
    proposer_address is the original block proposer address, formatted as a
    Bech32 string. In Tendermint, this type is `bytes`, but in the SDK, we
    convert it to a Bech32 string for better UX.
    """


@dataclass(eq=False, repr=False)
class GetValidatorSetByHeightRequest(betterproto.Message):
    """
    GetValidatorSetByHeightRequest is the request type for the
    Query/GetValidatorSetByHeight RPC method.
    """

    height: int = betterproto.int64_field(1)
    pagination: "__query_v1_beta1__.PageRequest" = betterproto.message_field(2)
    """pagination defines an pagination for the request."""


@dataclass(eq=False, repr=False)
class GetValidatorSetByHeightResponse(betterproto.Message):
    """
    GetValidatorSetByHeightResponse is the response type for the
    Query/GetValidatorSetByHeight RPC method.
    """

    block_height: int = betterproto.int64_field(1)
    validators: List["Validator"] = betterproto.message_field(2)
    pagination: "__query_v1_beta1__.PageResponse" = betterproto.message_field(3)
    """pagination defines an pagination for the response."""


@dataclass(eq=False, repr=False)
class GetLatestValidatorSetRequest(betterproto.Message):
    """
    GetLatestValidatorSetRequest is the request type for the
    Query/GetValidatorSetByHeight RPC method.
    """

    pagination: "__query_v1_beta1__.PageRequest" = betterproto.message_field(1)
    """pagination defines an pagination for the request."""


@dataclass(eq=False, repr=False)
class GetLatestValidatorSetResponse(betterproto.Message):
    """
    GetLatestValidatorSetResponse is the response type for the
    Query/GetValidatorSetByHeight RPC method.
    """

    block_height: int = betterproto.int64_field(1)
    validators: List["Validator"] = betterproto.message_field(2)
    pagination: "__query_v1_beta1__.PageResponse" = betterproto.message_field(3)
    """pagination defines an pagination for the response."""


@dataclass(eq=False, repr=False)
class Validator(betterproto.Message):
    """Validator is the type for the validator-set."""

    address: str = betterproto.string_field(1)
    pub_key: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(2)
    voting_power: int = betterproto.int64_field(3)
    proposer_priority: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class GetBlockByHeightRequest(betterproto.Message):
    """
    GetBlockByHeightRequest is the request type for the Query/GetBlockByHeight
    RPC method.
    """

    height: int = betterproto.int64_field(1)


@dataclass(eq=False, repr=False)
class GetBlockByHeightResponse(betterproto.Message):
    """
    GetBlockByHeightResponse is the response type for the
    Query/GetBlockByHeight RPC method.
    """

    block_id: "____tendermint_types__.BlockId" = betterproto.message_field(1)
    block: "____tendermint_types__.Block" = betterproto.message_field(2)
    """Deprecated: please use `sdk_block` instead"""

    sdk_block: "Block" = betterproto.message_field(3)
    """Since: cosmos-sdk 0.47"""


@dataclass(eq=False, repr=False)
class GetLatestBlockRequest(betterproto.Message):
    """
    GetLatestBlockRequest is the request type for the Query/GetLatestBlock RPC
    method.
    """

    pass


@dataclass(eq=False, repr=False)
class GetLatestBlockResponse(betterproto.Message):
    """
    GetLatestBlockResponse is the response type for the Query/GetLatestBlock
    RPC method.
    """

    block_id: "____tendermint_types__.BlockId" = betterproto.message_field(1)
    block: "____tendermint_types__.Block" = betterproto.message_field(2)
    """Deprecated: please use `sdk_block` instead"""

    sdk_block: "Block" = betterproto.message_field(3)
    """Since: cosmos-sdk 0.47"""


@dataclass(eq=False, repr=False)
class GetSyncingRequest(betterproto.Message):
    """
    GetSyncingRequest is the request type for the Query/GetSyncing RPC method.
    """

    pass


@dataclass(eq=False, repr=False)
class GetSyncingResponse(betterproto.Message):
    """
    GetSyncingResponse is the response type for the Query/GetSyncing RPC
    method.
    """

    syncing: bool = betterproto.bool_field(1)


@dataclass(eq=False, repr=False)
class GetNodeInfoRequest(betterproto.Message):
    """
    GetNodeInfoRequest is the request type for the Query/GetNodeInfo RPC
    method.
    """

    pass


@dataclass(eq=False, repr=False)
class GetNodeInfoResponse(betterproto.Message):
    """
    GetNodeInfoResponse is the response type for the Query/GetNodeInfo RPC
    method.
    """

    default_node_info: "____tendermint_p2_p__.DefaultNodeInfo" = (
        betterproto.message_field(1)
    )
    application_version: "VersionInfo" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class VersionInfo(betterproto.Message):
    """VersionInfo is the type for the GetNodeInfoResponse message."""

    name: str = betterproto.string_field(1)
    app_name: str = betterproto.string_field(2)
    version: str = betterproto.string_field(3)
    git_commit: str = betterproto.string_field(4)
    build_tags: str = betterproto.string_field(5)
    go_version: str = betterproto.string_field(6)
    build_deps: List["Module"] = betterproto.message_field(7)
    cosmos_sdk_version: str = betterproto.string_field(8)
    """Since: cosmos-sdk 0.43"""


@dataclass(eq=False, repr=False)
class Module(betterproto.Message):
    """Module is the type for VersionInfo"""

    path: str = betterproto.string_field(1)
    """module path"""

    version: str = betterproto.string_field(2)
    """module version"""

    sum: str = betterproto.string_field(3)
    """checksum"""


@dataclass(eq=False, repr=False)
class AbciQueryRequest(betterproto.Message):
    """
    ABCIQueryRequest defines the request structure for the ABCIQuery gRPC
    query.
    """

    data: bytes = betterproto.bytes_field(1)
    path: str = betterproto.string_field(2)
    height: int = betterproto.int64_field(3)
    prove: bool = betterproto.bool_field(4)


@dataclass(eq=False, repr=False)
class AbciQueryResponse(betterproto.Message):
    """
    ABCIQueryResponse defines the response structure for the ABCIQuery gRPC
    query. Note: This type is a duplicate of the ResponseQuery proto type
    defined in Tendermint.
    """

    code: int = betterproto.uint32_field(1)
    log: str = betterproto.string_field(3)
    info: str = betterproto.string_field(4)
    index: int = betterproto.int64_field(5)
    key: bytes = betterproto.bytes_field(6)
    value: bytes = betterproto.bytes_field(7)
    proof_ops: "ProofOps" = betterproto.message_field(8)
    height: int = betterproto.int64_field(9)
    codespace: str = betterproto.string_field(10)


@dataclass(eq=False, repr=False)
class ProofOp(betterproto.Message):
    """
    ProofOp defines an operation used for calculating Merkle root. The data
    could be arbitrary format, providing necessary data for example
    neighbouring node hash. Note: This type is a duplicate of the ProofOp proto
    type defined in Tendermint.
    """

    type: str = betterproto.string_field(1)
    key: bytes = betterproto.bytes_field(2)
    data: bytes = betterproto.bytes_field(3)


@dataclass(eq=False, repr=False)
class ProofOps(betterproto.Message):
    """
    ProofOps is Merkle proof defined by the list of ProofOps. Note: This type
    is a duplicate of the ProofOps proto type defined in Tendermint.
    """

    ops: List["ProofOp"] = betterproto.message_field(1)


class ServiceStub(betterproto.ServiceStub):
    async def get_node_info(
        self,
        get_node_info_request: "GetNodeInfoRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetNodeInfoResponse":
        return await self._unary_unary(
            "/cosmos.base.tendermint.v1beta1.Service/GetNodeInfo",
            get_node_info_request,
            GetNodeInfoResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_syncing(
        self,
        get_syncing_request: "GetSyncingRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetSyncingResponse":
        return await self._unary_unary(
            "/cosmos.base.tendermint.v1beta1.Service/GetSyncing",
            get_syncing_request,
            GetSyncingResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_latest_block(
        self,
        get_latest_block_request: "GetLatestBlockRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetLatestBlockResponse":
        return await self._unary_unary(
            "/cosmos.base.tendermint.v1beta1.Service/GetLatestBlock",
            get_latest_block_request,
            GetLatestBlockResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_block_by_height(
        self,
        get_block_by_height_request: "GetBlockByHeightRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetBlockByHeightResponse":
        return await self._unary_unary(
            "/cosmos.base.tendermint.v1beta1.Service/GetBlockByHeight",
            get_block_by_height_request,
            GetBlockByHeightResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_latest_validator_set(
        self,
        get_latest_validator_set_request: "GetLatestValidatorSetRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetLatestValidatorSetResponse":
        return await self._unary_unary(
            "/cosmos.base.tendermint.v1beta1.Service/GetLatestValidatorSet",
            get_latest_validator_set_request,
            GetLatestValidatorSetResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_validator_set_by_height(
        self,
        get_validator_set_by_height_request: "GetValidatorSetByHeightRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetValidatorSetByHeightResponse":
        return await self._unary_unary(
            "/cosmos.base.tendermint.v1beta1.Service/GetValidatorSetByHeight",
            get_validator_set_by_height_request,
            GetValidatorSetByHeightResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def abci_query(
        self,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "AbciQueryResponse":
        return await self._unary_unary(
            "/cosmos.base.tendermint.v1beta1.Service/ABCIQuery",
            abci_query_request,
            AbciQueryResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class ServiceBase(ServiceBase):

    async def get_node_info(
        self, get_node_info_request: "GetNodeInfoRequest"
    ) -> "GetNodeInfoResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_syncing(
        self, get_syncing_request: "GetSyncingRequest"
    ) -> "GetSyncingResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_latest_block(
        self, get_latest_block_request: "GetLatestBlockRequest"
    ) -> "GetLatestBlockResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_block_by_height(
        self, get_block_by_height_request: "GetBlockByHeightRequest"
    ) -> "GetBlockByHeightResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_latest_validator_set(
        self, get_latest_validator_set_request: "GetLatestValidatorSetRequest"
    ) -> "GetLatestValidatorSetResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_validator_set_by_height(
        self, get_validator_set_by_height_request: "GetValidatorSetByHeightRequest"
    ) -> "GetValidatorSetByHeightResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def abci_query(self) -> "AbciQueryResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_get_node_info(
        self, stream: "grpclib.server.Stream[GetNodeInfoRequest, GetNodeInfoResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_node_info(request)
        await stream.send_message(response)

    async def __rpc_get_syncing(
        self, stream: "grpclib.server.Stream[GetSyncingRequest, GetSyncingResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_syncing(request)
        await stream.send_message(response)

    async def __rpc_get_latest_block(
        self,
        stream: "grpclib.server.Stream[GetLatestBlockRequest, GetLatestBlockResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_latest_block(request)
        await stream.send_message(response)

    async def __rpc_get_block_by_height(
        self,
        stream: "grpclib.server.Stream[GetBlockByHeightRequest, GetBlockByHeightResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_block_by_height(request)
        await stream.send_message(response)

    async def __rpc_get_latest_validator_set(
        self,
        stream: "grpclib.server.Stream[GetLatestValidatorSetRequest, GetLatestValidatorSetResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_latest_validator_set(request)
        await stream.send_message(response)

    async def __rpc_get_validator_set_by_height(
        self,
        stream: "grpclib.server.Stream[GetValidatorSetByHeightRequest, GetValidatorSetByHeightResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_validator_set_by_height(request)
        await stream.send_message(response)

    async def __rpc_abci_query(
        self, stream: "grpclib.server.Stream[AbciQueryRequest, AbciQueryResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.abci_query(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/cosmos.base.tendermint.v1beta1.Service/GetNodeInfo": grpclib.const.Handler(
                self.__rpc_get_node_info,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetNodeInfoRequest,
                GetNodeInfoResponse,
            ),
            "/cosmos.base.tendermint.v1beta1.Service/GetSyncing": grpclib.const.Handler(
                self.__rpc_get_syncing,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetSyncingRequest,
                GetSyncingResponse,
            ),
            "/cosmos.base.tendermint.v1beta1.Service/GetLatestBlock": grpclib.const.Handler(
                self.__rpc_get_latest_block,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetLatestBlockRequest,
                GetLatestBlockResponse,
            ),
            "/cosmos.base.tendermint.v1beta1.Service/GetBlockByHeight": grpclib.const.Handler(
                self.__rpc_get_block_by_height,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetBlockByHeightRequest,
                GetBlockByHeightResponse,
            ),
            "/cosmos.base.tendermint.v1beta1.Service/GetLatestValidatorSet": grpclib.const.Handler(
                self.__rpc_get_latest_validator_set,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetLatestValidatorSetRequest,
                GetLatestValidatorSetResponse,
            ),
            "/cosmos.base.tendermint.v1beta1.Service/GetValidatorSetByHeight": grpclib.const.Handler(
                self.__rpc_get_validator_set_by_height,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetValidatorSetByHeightRequest,
                GetValidatorSetByHeightResponse,
            ),
            "/cosmos.base.tendermint.v1beta1.Service/ABCIQuery": grpclib.const.Handler(
                self.__rpc_abci_query,
                grpclib.const.Cardinality.UNARY_UNARY,
                AbciQueryRequest,
                AbciQueryResponse,
            ),
        }
