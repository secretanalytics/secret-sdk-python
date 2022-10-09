# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: tendermint/abci/types.proto
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
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase

from .. import (
    crypto as _crypto__,
    types as _types__,
)


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


class CheckTxType(betterproto.Enum):
    NEW = 0
    RECHECK = 1


class EvidenceType(betterproto.Enum):
    UNKNOWN = 0
    DUPLICATE_VOTE = 1
    LIGHT_CLIENT_ATTACK = 2


class ResponseOfferSnapshotResult(betterproto.Enum):
    UNKNOWN = 0
    ACCEPT = 1
    ABORT = 2
    REJECT = 3
    REJECT_FORMAT = 4
    REJECT_SENDER = 5


class ResponseApplySnapshotChunkResult(betterproto.Enum):
    UNKNOWN = 0
    ACCEPT = 1
    ABORT = 2
    RETRY = 3
    RETRY_SNAPSHOT = 4
    REJECT_SNAPSHOT = 5


@dataclass(eq=False, repr=False)
class Request(betterproto.Message):
    echo: "RequestEcho" = betterproto.message_field(1, group="value")
    flush: "RequestFlush" = betterproto.message_field(2, group="value")
    info: "RequestInfo" = betterproto.message_field(3, group="value")
    set_option: "RequestSetOption" = betterproto.message_field(4, group="value")
    init_chain: "RequestInitChain" = betterproto.message_field(5, group="value")
    query: "RequestQuery" = betterproto.message_field(6, group="value")
    begin_block: "RequestBeginBlock" = betterproto.message_field(7, group="value")
    check_tx: "RequestCheckTx" = betterproto.message_field(8, group="value")
    deliver_tx: "RequestDeliverTx" = betterproto.message_field(9, group="value")
    end_block: "RequestEndBlock" = betterproto.message_field(10, group="value")
    commit: "RequestCommit" = betterproto.message_field(11, group="value")
    list_snapshots: "RequestListSnapshots" = betterproto.message_field(
        12, group="value"
    )
    offer_snapshot: "RequestOfferSnapshot" = betterproto.message_field(
        13, group="value"
    )
    load_snapshot_chunk: "RequestLoadSnapshotChunk" = betterproto.message_field(
        14, group="value"
    )
    apply_snapshot_chunk: "RequestApplySnapshotChunk" = betterproto.message_field(
        15, group="value"
    )


@dataclass(eq=False, repr=False)
class RequestEcho(betterproto.Message):
    message: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class RequestFlush(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class RequestInfo(betterproto.Message):
    version: str = betterproto.string_field(1)
    block_version: int = betterproto.uint64_field(2)
    p2_p_version: int = betterproto.uint64_field(3)


@dataclass(eq=False, repr=False)
class RequestSetOption(betterproto.Message):
    """nondeterministic"""

    key: str = betterproto.string_field(1)
    value: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class RequestInitChain(betterproto.Message):
    time: datetime = betterproto.message_field(1)
    chain_id: str = betterproto.string_field(2)
    consensus_params: "ConsensusParams" = betterproto.message_field(3)
    validators: List["ValidatorUpdate"] = betterproto.message_field(4)
    app_state_bytes: bytes = betterproto.bytes_field(5)
    initial_height: int = betterproto.int64_field(6)


@dataclass(eq=False, repr=False)
class RequestQuery(betterproto.Message):
    data: bytes = betterproto.bytes_field(1)
    path: str = betterproto.string_field(2)
    height: int = betterproto.int64_field(3)
    prove: bool = betterproto.bool_field(4)


@dataclass(eq=False, repr=False)
class RequestBeginBlock(betterproto.Message):
    hash: bytes = betterproto.bytes_field(1)
    header: "_types__.Header" = betterproto.message_field(2)
    last_commit_info: "LastCommitInfo" = betterproto.message_field(3)
    byzantine_validators: List["Evidence"] = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class RequestCheckTx(betterproto.Message):
    tx: bytes = betterproto.bytes_field(1)
    type: "CheckTxType" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class RequestDeliverTx(betterproto.Message):
    tx: bytes = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class RequestEndBlock(betterproto.Message):
    height: int = betterproto.int64_field(1)


@dataclass(eq=False, repr=False)
class RequestCommit(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class RequestListSnapshots(betterproto.Message):
    """lists available snapshots"""

    pass


@dataclass(eq=False, repr=False)
class RequestOfferSnapshot(betterproto.Message):
    """offers a snapshot to the application"""

    snapshot: "Snapshot" = betterproto.message_field(1)
    app_hash: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class RequestLoadSnapshotChunk(betterproto.Message):
    """loads a snapshot chunk"""

    height: int = betterproto.uint64_field(1)
    format: int = betterproto.uint32_field(2)
    chunk: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class RequestApplySnapshotChunk(betterproto.Message):
    """Applies a snapshot chunk"""

    index: int = betterproto.uint32_field(1)
    chunk: bytes = betterproto.bytes_field(2)
    sender: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class Response(betterproto.Message):
    exception: "ResponseException" = betterproto.message_field(1, group="value")
    echo: "ResponseEcho" = betterproto.message_field(2, group="value")
    flush: "ResponseFlush" = betterproto.message_field(3, group="value")
    info: "ResponseInfo" = betterproto.message_field(4, group="value")
    set_option: "ResponseSetOption" = betterproto.message_field(5, group="value")
    init_chain: "ResponseInitChain" = betterproto.message_field(6, group="value")
    query: "ResponseQuery" = betterproto.message_field(7, group="value")
    begin_block: "ResponseBeginBlock" = betterproto.message_field(8, group="value")
    check_tx: "ResponseCheckTx" = betterproto.message_field(9, group="value")
    deliver_tx: "ResponseDeliverTx" = betterproto.message_field(10, group="value")
    end_block: "ResponseEndBlock" = betterproto.message_field(11, group="value")
    commit: "ResponseCommit" = betterproto.message_field(12, group="value")
    list_snapshots: "ResponseListSnapshots" = betterproto.message_field(
        13, group="value"
    )
    offer_snapshot: "ResponseOfferSnapshot" = betterproto.message_field(
        14, group="value"
    )
    load_snapshot_chunk: "ResponseLoadSnapshotChunk" = betterproto.message_field(
        15, group="value"
    )
    apply_snapshot_chunk: "ResponseApplySnapshotChunk" = betterproto.message_field(
        16, group="value"
    )


@dataclass(eq=False, repr=False)
class ResponseException(betterproto.Message):
    """nondeterministic"""

    error: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class ResponseEcho(betterproto.Message):
    message: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class ResponseFlush(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class ResponseInfo(betterproto.Message):
    data: str = betterproto.string_field(1)
    version: str = betterproto.string_field(2)
    app_version: int = betterproto.uint64_field(3)
    last_block_height: int = betterproto.int64_field(4)
    last_block_app_hash: bytes = betterproto.bytes_field(5)


@dataclass(eq=False, repr=False)
class ResponseSetOption(betterproto.Message):
    """nondeterministic"""

    code: int = betterproto.uint32_field(1)
    log: str = betterproto.string_field(3)
    """bytes data = 2;"""

    info: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class ResponseInitChain(betterproto.Message):
    consensus_params: "ConsensusParams" = betterproto.message_field(1)
    validators: List["ValidatorUpdate"] = betterproto.message_field(2)
    app_hash: bytes = betterproto.bytes_field(3)


@dataclass(eq=False, repr=False)
class ResponseQuery(betterproto.Message):
    code: int = betterproto.uint32_field(1)
    log: str = betterproto.string_field(3)
    """bytes data = 2; // use "value" instead."""

    info: str = betterproto.string_field(4)
    index: int = betterproto.int64_field(5)
    key: bytes = betterproto.bytes_field(6)
    value: bytes = betterproto.bytes_field(7)
    proof_ops: "_crypto__.ProofOps" = betterproto.message_field(8)
    height: int = betterproto.int64_field(9)
    codespace: str = betterproto.string_field(10)


@dataclass(eq=False, repr=False)
class ResponseBeginBlock(betterproto.Message):
    events: List["Event"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class ResponseCheckTx(betterproto.Message):
    code: int = betterproto.uint32_field(1)
    data: bytes = betterproto.bytes_field(2)
    log: str = betterproto.string_field(3)
    info: str = betterproto.string_field(4)
    gas_wanted: int = betterproto.int64_field(5)
    gas_used: int = betterproto.int64_field(6)
    events: List["Event"] = betterproto.message_field(7)
    codespace: str = betterproto.string_field(8)


@dataclass(eq=False, repr=False)
class ResponseDeliverTx(betterproto.Message):
    code: int = betterproto.uint32_field(1)
    data: bytes = betterproto.bytes_field(2)
    log: str = betterproto.string_field(3)
    info: str = betterproto.string_field(4)
    gas_wanted: int = betterproto.int64_field(5)
    gas_used: int = betterproto.int64_field(6)
    events: List["Event"] = betterproto.message_field(7)
    codespace: str = betterproto.string_field(8)


@dataclass(eq=False, repr=False)
class ResponseEndBlock(betterproto.Message):
    validator_updates: List["ValidatorUpdate"] = betterproto.message_field(1)
    consensus_param_updates: "ConsensusParams" = betterproto.message_field(2)
    events: List["Event"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class ResponseCommit(betterproto.Message):
    data: bytes = betterproto.bytes_field(2)
    """reserve 1"""

    retain_height: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class ResponseListSnapshots(betterproto.Message):
    snapshots: List["Snapshot"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class ResponseOfferSnapshot(betterproto.Message):
    result: "ResponseOfferSnapshotResult" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class ResponseLoadSnapshotChunk(betterproto.Message):
    chunk: bytes = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class ResponseApplySnapshotChunk(betterproto.Message):
    result: "ResponseApplySnapshotChunkResult" = betterproto.enum_field(1)
    refetch_chunks: List[int] = betterproto.uint32_field(2)
    reject_senders: List[str] = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class ConsensusParams(betterproto.Message):
    """
    ConsensusParams contains all consensus-relevant parameters that can be
    adjusted by the abci app
    """

    block: "BlockParams" = betterproto.message_field(1)
    evidence: "_types__.EvidenceParams" = betterproto.message_field(2)
    validator: "_types__.ValidatorParams" = betterproto.message_field(3)
    version: "_types__.VersionParams" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class BlockParams(betterproto.Message):
    """BlockParams contains limits on the block size."""

    max_bytes: int = betterproto.int64_field(1)
    """Note: must be greater than 0"""

    max_gas: int = betterproto.int64_field(2)
    """Note: must be greater or equal to -1"""


@dataclass(eq=False, repr=False)
class LastCommitInfo(betterproto.Message):
    round: int = betterproto.int32_field(1)
    votes: List["VoteInfo"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class Event(betterproto.Message):
    """
    Event allows application developers to attach additional information to
    ResponseBeginBlock, ResponseEndBlock, ResponseCheckTx and
    ResponseDeliverTx. Later, transactions may be queried using these events.
    """

    type: str = betterproto.string_field(1)
    attributes: List["EventAttribute"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class EventAttribute(betterproto.Message):
    """EventAttribute is a single key-value pair, associated with an event."""

    key: bytes = betterproto.bytes_field(1)
    value: bytes = betterproto.bytes_field(2)
    index: bool = betterproto.bool_field(3)


@dataclass(eq=False, repr=False)
class TxResult(betterproto.Message):
    """
    TxResult contains results of executing the transaction. One usage is
    indexing transaction results.
    """

    height: int = betterproto.int64_field(1)
    index: int = betterproto.uint32_field(2)
    tx: bytes = betterproto.bytes_field(3)
    result: "ResponseDeliverTx" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class Validator(betterproto.Message):
    """Validator"""

    address: bytes = betterproto.bytes_field(1)
    power: int = betterproto.int64_field(3)
    """PubKey pub_key = 2 [(gogoproto.nullable)=false];"""


@dataclass(eq=False, repr=False)
class ValidatorUpdate(betterproto.Message):
    """ValidatorUpdate"""

    pub_key: "_crypto__.PublicKey" = betterproto.message_field(1)
    power: int = betterproto.int64_field(2)


@dataclass(eq=False, repr=False)
class VoteInfo(betterproto.Message):
    """VoteInfo"""

    validator: "Validator" = betterproto.message_field(1)
    signed_last_block: bool = betterproto.bool_field(2)


@dataclass(eq=False, repr=False)
class Evidence(betterproto.Message):
    type: "EvidenceType" = betterproto.enum_field(1)
    validator: "Validator" = betterproto.message_field(2)
    """The offending validator"""

    height: int = betterproto.int64_field(3)
    """The height when the offense occurred"""

    time: datetime = betterproto.message_field(4)
    """The corresponding time where the offense occurred"""

    total_voting_power: int = betterproto.int64_field(5)
    """
    Total voting power of the validator set in case the ABCI application does
    not store historical validators.
    https://github.com/tendermint/tendermint/issues/4581
    """


@dataclass(eq=False, repr=False)
class Snapshot(betterproto.Message):
    height: int = betterproto.uint64_field(1)
    format: int = betterproto.uint32_field(2)
    chunks: int = betterproto.uint32_field(3)
    hash: bytes = betterproto.bytes_field(4)
    metadata: bytes = betterproto.bytes_field(5)


class AbciApplicationStub(betterproto.ServiceStub):
    async def echo(
        self,
        request_echo: "RequestEcho",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseEcho":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/Echo",
            request_echo,
            ResponseEcho,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def flush(
        self,
        request_flush: "RequestFlush",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseFlush":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/Flush",
            request_flush,
            ResponseFlush,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def info(
        self,
        request_info: "RequestInfo",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseInfo":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/Info",
            request_info,
            ResponseInfo,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def set_option(
        self,
        request_set_option: "RequestSetOption",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseSetOption":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/SetOption",
            request_set_option,
            ResponseSetOption,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def deliver_tx(
        self,
        request_deliver_tx: "RequestDeliverTx",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseDeliverTx":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/DeliverTx",
            request_deliver_tx,
            ResponseDeliverTx,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def check_tx(
        self,
        request_check_tx: "RequestCheckTx",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseCheckTx":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/CheckTx",
            request_check_tx,
            ResponseCheckTx,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def query(
        self,
        request_query: "RequestQuery",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseQuery":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/Query",
            request_query,
            ResponseQuery,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def commit(
        self,
        request_commit: "RequestCommit",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseCommit":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/Commit",
            request_commit,
            ResponseCommit,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def init_chain(
        self,
        request_init_chain: "RequestInitChain",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseInitChain":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/InitChain",
            request_init_chain,
            ResponseInitChain,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def begin_block(
        self,
        request_begin_block: "RequestBeginBlock",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseBeginBlock":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/BeginBlock",
            request_begin_block,
            ResponseBeginBlock,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def end_block(
        self,
        request_end_block: "RequestEndBlock",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseEndBlock":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/EndBlock",
            request_end_block,
            ResponseEndBlock,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def list_snapshots(
        self,
        request_list_snapshots: "RequestListSnapshots",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseListSnapshots":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/ListSnapshots",
            request_list_snapshots,
            ResponseListSnapshots,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def offer_snapshot(
        self,
        request_offer_snapshot: "RequestOfferSnapshot",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseOfferSnapshot":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/OfferSnapshot",
            request_offer_snapshot,
            ResponseOfferSnapshot,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def load_snapshot_chunk(
        self,
        request_load_snapshot_chunk: "RequestLoadSnapshotChunk",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseLoadSnapshotChunk":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/LoadSnapshotChunk",
            request_load_snapshot_chunk,
            ResponseLoadSnapshotChunk,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def apply_snapshot_chunk(
        self,
        request_apply_snapshot_chunk: "RequestApplySnapshotChunk",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResponseApplySnapshotChunk":
        return await self._unary_unary(
            "/tendermint.abci.ABCIApplication/ApplySnapshotChunk",
            request_apply_snapshot_chunk,
            ResponseApplySnapshotChunk,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class AbciApplicationBase(ServiceBase):
    async def echo(self, request_echo: "RequestEcho") -> "ResponseEcho":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def flush(self, request_flush: "RequestFlush") -> "ResponseFlush":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def info(self, request_info: "RequestInfo") -> "ResponseInfo":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def set_option(
        self, request_set_option: "RequestSetOption"
    ) -> "ResponseSetOption":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def deliver_tx(
        self, request_deliver_tx: "RequestDeliverTx"
    ) -> "ResponseDeliverTx":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def check_tx(self, request_check_tx: "RequestCheckTx") -> "ResponseCheckTx":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def query(self, request_query: "RequestQuery") -> "ResponseQuery":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def commit(self, request_commit: "RequestCommit") -> "ResponseCommit":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def init_chain(
        self, request_init_chain: "RequestInitChain"
    ) -> "ResponseInitChain":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def begin_block(
        self, request_begin_block: "RequestBeginBlock"
    ) -> "ResponseBeginBlock":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def end_block(
        self, request_end_block: "RequestEndBlock"
    ) -> "ResponseEndBlock":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def list_snapshots(
        self, request_list_snapshots: "RequestListSnapshots"
    ) -> "ResponseListSnapshots":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def offer_snapshot(
        self, request_offer_snapshot: "RequestOfferSnapshot"
    ) -> "ResponseOfferSnapshot":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def load_snapshot_chunk(
        self, request_load_snapshot_chunk: "RequestLoadSnapshotChunk"
    ) -> "ResponseLoadSnapshotChunk":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def apply_snapshot_chunk(
        self, request_apply_snapshot_chunk: "RequestApplySnapshotChunk"
    ) -> "ResponseApplySnapshotChunk":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_echo(
        self, stream: "grpclib.server.Stream[RequestEcho, ResponseEcho]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.echo(request)
        await stream.send_message(response)

    async def __rpc_flush(
        self, stream: "grpclib.server.Stream[RequestFlush, ResponseFlush]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.flush(request)
        await stream.send_message(response)

    async def __rpc_info(
        self, stream: "grpclib.server.Stream[RequestInfo, ResponseInfo]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.info(request)
        await stream.send_message(response)

    async def __rpc_set_option(
        self, stream: "grpclib.server.Stream[RequestSetOption, ResponseSetOption]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.set_option(request)
        await stream.send_message(response)

    async def __rpc_deliver_tx(
        self, stream: "grpclib.server.Stream[RequestDeliverTx, ResponseDeliverTx]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.deliver_tx(request)
        await stream.send_message(response)

    async def __rpc_check_tx(
        self, stream: "grpclib.server.Stream[RequestCheckTx, ResponseCheckTx]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.check_tx(request)
        await stream.send_message(response)

    async def __rpc_query(
        self, stream: "grpclib.server.Stream[RequestQuery, ResponseQuery]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.query(request)
        await stream.send_message(response)

    async def __rpc_commit(
        self, stream: "grpclib.server.Stream[RequestCommit, ResponseCommit]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.commit(request)
        await stream.send_message(response)

    async def __rpc_init_chain(
        self, stream: "grpclib.server.Stream[RequestInitChain, ResponseInitChain]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.init_chain(request)
        await stream.send_message(response)

    async def __rpc_begin_block(
        self, stream: "grpclib.server.Stream[RequestBeginBlock, ResponseBeginBlock]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.begin_block(request)
        await stream.send_message(response)

    async def __rpc_end_block(
        self, stream: "grpclib.server.Stream[RequestEndBlock, ResponseEndBlock]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.end_block(request)
        await stream.send_message(response)

    async def __rpc_list_snapshots(
        self,
        stream: "grpclib.server.Stream[RequestListSnapshots, ResponseListSnapshots]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.list_snapshots(request)
        await stream.send_message(response)

    async def __rpc_offer_snapshot(
        self,
        stream: "grpclib.server.Stream[RequestOfferSnapshot, ResponseOfferSnapshot]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.offer_snapshot(request)
        await stream.send_message(response)

    async def __rpc_load_snapshot_chunk(
        self,
        stream: "grpclib.server.Stream[RequestLoadSnapshotChunk, ResponseLoadSnapshotChunk]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.load_snapshot_chunk(request)
        await stream.send_message(response)

    async def __rpc_apply_snapshot_chunk(
        self,
        stream: "grpclib.server.Stream[RequestApplySnapshotChunk, ResponseApplySnapshotChunk]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.apply_snapshot_chunk(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/tendermint.abci.ABCIApplication/Echo": grpclib.const.Handler(
                self.__rpc_echo,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestEcho,
                ResponseEcho,
            ),
            "/tendermint.abci.ABCIApplication/Flush": grpclib.const.Handler(
                self.__rpc_flush,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestFlush,
                ResponseFlush,
            ),
            "/tendermint.abci.ABCIApplication/Info": grpclib.const.Handler(
                self.__rpc_info,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestInfo,
                ResponseInfo,
            ),
            "/tendermint.abci.ABCIApplication/SetOption": grpclib.const.Handler(
                self.__rpc_set_option,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestSetOption,
                ResponseSetOption,
            ),
            "/tendermint.abci.ABCIApplication/DeliverTx": grpclib.const.Handler(
                self.__rpc_deliver_tx,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestDeliverTx,
                ResponseDeliverTx,
            ),
            "/tendermint.abci.ABCIApplication/CheckTx": grpclib.const.Handler(
                self.__rpc_check_tx,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestCheckTx,
                ResponseCheckTx,
            ),
            "/tendermint.abci.ABCIApplication/Query": grpclib.const.Handler(
                self.__rpc_query,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestQuery,
                ResponseQuery,
            ),
            "/tendermint.abci.ABCIApplication/Commit": grpclib.const.Handler(
                self.__rpc_commit,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestCommit,
                ResponseCommit,
            ),
            "/tendermint.abci.ABCIApplication/InitChain": grpclib.const.Handler(
                self.__rpc_init_chain,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestInitChain,
                ResponseInitChain,
            ),
            "/tendermint.abci.ABCIApplication/BeginBlock": grpclib.const.Handler(
                self.__rpc_begin_block,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestBeginBlock,
                ResponseBeginBlock,
            ),
            "/tendermint.abci.ABCIApplication/EndBlock": grpclib.const.Handler(
                self.__rpc_end_block,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestEndBlock,
                ResponseEndBlock,
            ),
            "/tendermint.abci.ABCIApplication/ListSnapshots": grpclib.const.Handler(
                self.__rpc_list_snapshots,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestListSnapshots,
                ResponseListSnapshots,
            ),
            "/tendermint.abci.ABCIApplication/OfferSnapshot": grpclib.const.Handler(
                self.__rpc_offer_snapshot,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestOfferSnapshot,
                ResponseOfferSnapshot,
            ),
            "/tendermint.abci.ABCIApplication/LoadSnapshotChunk": grpclib.const.Handler(
                self.__rpc_load_snapshot_chunk,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestLoadSnapshotChunk,
                ResponseLoadSnapshotChunk,
            ),
            "/tendermint.abci.ABCIApplication/ApplySnapshotChunk": grpclib.const.Handler(
                self.__rpc_apply_snapshot_chunk,
                grpclib.const.Cardinality.UNARY_UNARY,
                RequestApplySnapshotChunk,
                ResponseApplySnapshotChunk,
            ),
        }
