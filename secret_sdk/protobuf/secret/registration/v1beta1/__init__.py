# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: secret/registration/v1beta1/genesis.proto, secret/registration/v1beta1/msg.proto, secret/registration/v1beta1/query.proto, secret/registration/v1beta1/types.proto
# plugin: python-betterproto
import builtins
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
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
class SeedConfig(betterproto.Message):
    master_cert: str = betterproto.string_field(1)
    encrypted_key: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class RegistrationNodeInfo(betterproto.Message):
    certificate: bytes = betterproto.bytes_field(1)
    encrypted_seed: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class RaAuthenticate(betterproto.Message):
    sender: bytes = betterproto.bytes_field(1)
    certificate: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class MasterCertificate(betterproto.Message):
    bytes: builtins.bytes = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class Key(betterproto.Message):
    key: bytes = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class GenesisState(betterproto.Message):
    registration: List["RegistrationNodeInfo"] = betterproto.message_field(1)
    node_exch_master_certificate: "MasterCertificate" = betterproto.message_field(2)
    io_master_certificate: "MasterCertificate" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class QueryEncryptedSeedRequest(betterproto.Message):
    pub_key: bytes = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class QueryEncryptedSeedResponse(betterproto.Message):
    encrypted_seed: bytes = betterproto.bytes_field(1)


class QueryStub(betterproto.ServiceStub):
    async def tx_key(
        self,
        betterproto_lib_google_protobuf_empty: "betterproto_lib_google_protobuf.Empty",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "Key":
        return await self._unary_unary(
            "/secret.registration.v1beta1.Query/TxKey",
            betterproto_lib_google_protobuf_empty,
            Key,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def registration_key(
        self,
        betterproto_lib_google_protobuf_empty: "betterproto_lib_google_protobuf.Empty",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "Key":
        return await self._unary_unary(
            "/secret.registration.v1beta1.Query/RegistrationKey",
            betterproto_lib_google_protobuf_empty,
            Key,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def encrypted_seed(
        self,
        query_encrypted_seed_request: "QueryEncryptedSeedRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryEncryptedSeedResponse":
        return await self._unary_unary(
            "/secret.registration.v1beta1.Query/EncryptedSeed",
            query_encrypted_seed_request,
            QueryEncryptedSeedResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class QueryBase(ServiceBase):
    async def tx_key(
        self,
        betterproto_lib_google_protobuf_empty: "betterproto_lib_google_protobuf.Empty",
    ) -> "Key":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def registration_key(
        self,
        betterproto_lib_google_protobuf_empty: "betterproto_lib_google_protobuf.Empty",
    ) -> "Key":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def encrypted_seed(
        self, query_encrypted_seed_request: "QueryEncryptedSeedRequest"
    ) -> "QueryEncryptedSeedResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_tx_key(
        self,
        stream: "grpclib.server.Stream[betterproto_lib_google_protobuf.Empty, Key]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.tx_key(request)
        await stream.send_message(response)

    async def __rpc_registration_key(
        self,
        stream: "grpclib.server.Stream[betterproto_lib_google_protobuf.Empty, Key]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.registration_key(request)
        await stream.send_message(response)

    async def __rpc_encrypted_seed(
        self,
        stream: "grpclib.server.Stream[QueryEncryptedSeedRequest, QueryEncryptedSeedResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.encrypted_seed(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/secret.registration.v1beta1.Query/TxKey": grpclib.const.Handler(
                self.__rpc_tx_key,
                grpclib.const.Cardinality.UNARY_UNARY,
                betterproto_lib_google_protobuf.Empty,
                Key,
            ),
            "/secret.registration.v1beta1.Query/RegistrationKey": grpclib.const.Handler(
                self.__rpc_registration_key,
                grpclib.const.Cardinality.UNARY_UNARY,
                betterproto_lib_google_protobuf.Empty,
                Key,
            ),
            "/secret.registration.v1beta1.Query/EncryptedSeed": grpclib.const.Handler(
                self.__rpc_encrypted_seed,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryEncryptedSeedRequest,
                QueryEncryptedSeedResponse,
            ),
        }
