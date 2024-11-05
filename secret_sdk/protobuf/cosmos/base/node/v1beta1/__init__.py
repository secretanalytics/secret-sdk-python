# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: cosmos/base/node/v1beta1/query.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Dict,
    Optional,
)

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


@dataclass(eq=False, repr=False)
class ConfigRequest(betterproto.Message):
    """
    ConfigRequest defines the request structure for the Config gRPC query.
    """

    pass


@dataclass(eq=False, repr=False)
class ConfigResponse(betterproto.Message):
    """
    ConfigResponse defines the response structure for the Config gRPC query.
    """

    minimum_gas_price: str = betterproto.string_field(1)
    pruning_keep_recent: str = betterproto.string_field(2)
    pruning_interval: str = betterproto.string_field(3)
    halt_height: int = betterproto.uint64_field(4)


@dataclass(eq=False, repr=False)
class StatusRequest(betterproto.Message):
    """StateRequest defines the request structure for the status of a node."""

    pass


@dataclass(eq=False, repr=False)
class StatusResponse(betterproto.Message):
    """
    StateResponse defines the response structure for the status of a node.
    """

    earliest_store_height: int = betterproto.uint64_field(1)
    height: int = betterproto.uint64_field(2)
    timestamp: datetime = betterproto.message_field(3)
    app_hash: bytes = betterproto.bytes_field(4)
    validator_hash: bytes = betterproto.bytes_field(5)


class ServiceStub(betterproto.ServiceStub):
    async def config(
        self,
        config_request: "ConfigRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ConfigResponse":
        return await self._unary_unary(
            "/cosmos.base.node.v1beta1.Service/Config",
            config_request,
            ConfigResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def status(
        self,
        status_request: "StatusRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "StatusResponse":
        return await self._unary_unary(
            "/cosmos.base.node.v1beta1.Service/Status",
            status_request,
            StatusResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class ServiceBase(ServiceBase):

    async def config(self, config_request: "ConfigRequest") -> "ConfigResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def status(self, status_request: "StatusRequest") -> "StatusResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_config(
        self, stream: "grpclib.server.Stream[ConfigRequest, ConfigResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.config(request)
        await stream.send_message(response)

    async def __rpc_status(
        self, stream: "grpclib.server.Stream[StatusRequest, StatusResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.status(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/cosmos.base.node.v1beta1.Service/Config": grpclib.const.Handler(
                self.__rpc_config,
                grpclib.const.Cardinality.UNARY_UNARY,
                ConfigRequest,
                ConfigResponse,
            ),
            "/cosmos.base.node.v1beta1.Service/Status": grpclib.const.Handler(
                self.__rpc_status,
                grpclib.const.Cardinality.UNARY_UNARY,
                StatusRequest,
                StatusResponse,
            ),
        }
