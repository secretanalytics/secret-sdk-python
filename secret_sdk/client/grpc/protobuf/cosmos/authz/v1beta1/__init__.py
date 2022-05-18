# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: cosmos/authz/v1beta1/authz.proto, cosmos/authz/v1beta1/event.proto, cosmos/authz/v1beta1/genesis.proto, cosmos/authz/v1beta1/query.proto, cosmos/authz/v1beta1/tx.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase
import grpclib


@dataclass(eq=False, repr=False)
class GenericAuthorization(betterproto.Message):
    """
    GenericAuthorization gives the grantee unrestricted permissions to execute
    the provided method on behalf of the granter's account.
    """

    # Msg, identified by it's type URL, to grant unrestricted permissions to
    # execute
    msg: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class Grant(betterproto.Message):
    """
    Grant gives permissions to execute the provide method with expiration time.
    """

    authorization: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(1)
    expiration: datetime = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class GrantAuthorization(betterproto.Message):
    """
    GrantAuthorization extends a grant with both the addresses of the grantee
    and granter. It is used in genesis.proto and query.proto Since: cosmos-sdk
    0.45.2
    """

    granter: str = betterproto.string_field(1)
    grantee: str = betterproto.string_field(2)
    authorization: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(3)
    expiration: datetime = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class MsgGrant(betterproto.Message):
    """
    MsgGrant is a request type for Grant method. It declares authorization to
    the grantee on behalf of the granter with the provided expiration time.
    """

    granter: str = betterproto.string_field(1)
    grantee: str = betterproto.string_field(2)
    grant: "Grant" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class MsgExecResponse(betterproto.Message):
    """MsgExecResponse defines the Msg/MsgExecResponse response type."""

    results: List[bytes] = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class MsgExec(betterproto.Message):
    """
    MsgExec attempts to execute the provided messages using authorizations
    granted to the grantee. Each message should have only one signer
    corresponding to the granter of the authorization.
    """

    grantee: str = betterproto.string_field(1)
    # Authorization Msg requests to execute. Each msg must implement
    # Authorization interface The x/authz will try to find a grant matching
    # (msg.signers[0], grantee, MsgTypeURL(msg)) triple and validate it.
    msgs: List["betterproto_lib_google_protobuf.Any"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class MsgGrantResponse(betterproto.Message):
    """MsgGrantResponse defines the Msg/MsgGrant response type."""

    pass


@dataclass(eq=False, repr=False)
class MsgRevoke(betterproto.Message):
    """
    MsgRevoke revokes any authorization with the provided sdk.Msg type on the
    granter's account with that has been granted to the grantee.
    """

    granter: str = betterproto.string_field(1)
    grantee: str = betterproto.string_field(2)
    msg_type_url: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class MsgRevokeResponse(betterproto.Message):
    """MsgRevokeResponse defines the Msg/MsgRevokeResponse response type."""

    pass


@dataclass(eq=False, repr=False)
class QueryGrantsRequest(betterproto.Message):
    """
    QueryGrantsRequest is the request type for the Query/Grants RPC method.
    """

    granter: str = betterproto.string_field(1)
    grantee: str = betterproto.string_field(2)
    # Optional, msg_type_url, when set, will query only grants matching given msg
    # type.
    msg_type_url: str = betterproto.string_field(3)
    # pagination defines an pagination for the request.
    pagination: "__base_query_v1_beta1__.PageRequest" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class QueryGrantsResponse(betterproto.Message):
    """
    QueryGrantsResponse is the response type for the Query/Authorizations RPC
    method.
    """

    # authorizations is a list of grants granted for grantee by granter.
    grants: List["Grant"] = betterproto.message_field(1)
    # pagination defines an pagination for the response.
    pagination: "__base_query_v1_beta1__.PageResponse" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class QueryGranterGrantsRequest(betterproto.Message):
    """
    QueryGranterGrantsRequest is the request type for the Query/GranterGrants
    RPC method.
    """

    granter: str = betterproto.string_field(1)
    # pagination defines an pagination for the request.
    pagination: "__base_query_v1_beta1__.PageRequest" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class QueryGranterGrantsResponse(betterproto.Message):
    """
    QueryGranterGrantsResponse is the response type for the Query/GranterGrants
    RPC method.
    """

    # grants is a list of grants granted by the granter.
    grants: List["GrantAuthorization"] = betterproto.message_field(1)
    # pagination defines an pagination for the response.
    pagination: "__base_query_v1_beta1__.PageResponse" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class QueryGranteeGrantsRequest(betterproto.Message):
    """
    QueryGranteeGrantsRequest is the request type for the Query/IssuedGrants
    RPC method.
    """

    grantee: str = betterproto.string_field(1)
    # pagination defines an pagination for the request.
    pagination: "__base_query_v1_beta1__.PageRequest" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class QueryGranteeGrantsResponse(betterproto.Message):
    """
    QueryGranteeGrantsResponse is the response type for the Query/GranteeGrants
    RPC method.
    """

    # grants is a list of grants granted to the grantee.
    grants: List["GrantAuthorization"] = betterproto.message_field(1)
    # pagination defines an pagination for the response.
    pagination: "__base_query_v1_beta1__.PageResponse" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class EventGrant(betterproto.Message):
    """EventGrant is emitted on Msg/Grant"""

    # Msg type URL for which an autorization is granted
    msg_type_url: str = betterproto.string_field(2)
    # Granter account address
    granter: str = betterproto.string_field(3)
    # Grantee account address
    grantee: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class EventRevoke(betterproto.Message):
    """EventRevoke is emitted on Msg/Revoke"""

    # Msg type URL for which an autorization is revoked
    msg_type_url: str = betterproto.string_field(2)
    # Granter account address
    granter: str = betterproto.string_field(3)
    # Grantee account address
    grantee: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class GenesisState(betterproto.Message):
    """GenesisState defines the authz module's genesis state."""

    authorization: List["GrantAuthorization"] = betterproto.message_field(1)


class MsgStub(betterproto.ServiceStub):
    async def grant(
        self, *, granter: str = "", grantee: str = "", grant: "Grant" = None
    ) -> "MsgGrantResponse":

        request = MsgGrant()
        request.granter = granter
        request.grantee = grantee
        if grant is not None:
            request.grant = grant

        return await self._unary_unary(
            "/cosmos.authz.v1beta1.Msg/Grant", request, MsgGrantResponse
        )

    async def exec(
        self,
        *,
        grantee: str = "",
        msgs: Optional[List["betterproto_lib_google_protobuf.Any"]] = None
    ) -> "MsgExecResponse":
        msgs = msgs or []

        request = MsgExec()
        request.grantee = grantee
        if msgs is not None:
            request.msgs = msgs

        return await self._unary_unary(
            "/cosmos.authz.v1beta1.Msg/Exec", request, MsgExecResponse
        )

    async def revoke(
        self, *, granter: str = "", grantee: str = "", msg_type_url: str = ""
    ) -> "MsgRevokeResponse":

        request = MsgRevoke()
        request.granter = granter
        request.grantee = grantee
        request.msg_type_url = msg_type_url

        return await self._unary_unary(
            "/cosmos.authz.v1beta1.Msg/Revoke", request, MsgRevokeResponse
        )


class QueryStub(betterproto.ServiceStub):
    async def grants(
        self,
        *,
        granter: str = "",
        grantee: str = "",
        msg_type_url: str = "",
        pagination: "__base_query_v1_beta1__.PageRequest" = None
    ) -> "QueryGrantsResponse":

        request = QueryGrantsRequest()
        request.granter = granter
        request.grantee = grantee
        request.msg_type_url = msg_type_url
        if pagination is not None:
            request.pagination = pagination

        return await self._unary_unary(
            "/cosmos.authz.v1beta1.Query/Grants", request, QueryGrantsResponse
        )

    async def granter_grants(
        self,
        *,
        granter: str = "",
        pagination: "__base_query_v1_beta1__.PageRequest" = None
    ) -> "QueryGranterGrantsResponse":

        request = QueryGranterGrantsRequest()
        request.granter = granter
        if pagination is not None:
            request.pagination = pagination

        return await self._unary_unary(
            "/cosmos.authz.v1beta1.Query/GranterGrants",
            request,
            QueryGranterGrantsResponse,
        )

    async def grantee_grants(
        self,
        *,
        grantee: str = "",
        pagination: "__base_query_v1_beta1__.PageRequest" = None
    ) -> "QueryGranteeGrantsResponse":

        request = QueryGranteeGrantsRequest()
        request.grantee = grantee
        if pagination is not None:
            request.pagination = pagination

        return await self._unary_unary(
            "/cosmos.authz.v1beta1.Query/GranteeGrants",
            request,
            QueryGranteeGrantsResponse,
        )


class MsgBase(ServiceBase):
    async def grant(
        self, granter: str, grantee: str, grant: "Grant"
    ) -> "MsgGrantResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def exec(
        self, grantee: str, msgs: Optional[List["betterproto_lib_google_protobuf.Any"]]
    ) -> "MsgExecResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def revoke(
        self, granter: str, grantee: str, msg_type_url: str
    ) -> "MsgRevokeResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_grant(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "granter": request.granter,
            "grantee": request.grantee,
            "grant": request.grant,
        }

        response = await self.grant(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_exec(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "grantee": request.grantee,
            "msgs": request.msgs,
        }

        response = await self.exec(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_revoke(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "granter": request.granter,
            "grantee": request.grantee,
            "msg_type_url": request.msg_type_url,
        }

        response = await self.revoke(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/cosmos.authz.v1beta1.Msg/Grant": grpclib.const.Handler(
                self.__rpc_grant,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgGrant,
                MsgGrantResponse,
            ),
            "/cosmos.authz.v1beta1.Msg/Exec": grpclib.const.Handler(
                self.__rpc_exec,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgExec,
                MsgExecResponse,
            ),
            "/cosmos.authz.v1beta1.Msg/Revoke": grpclib.const.Handler(
                self.__rpc_revoke,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgRevoke,
                MsgRevokeResponse,
            ),
        }


class QueryBase(ServiceBase):
    async def grants(
        self,
        granter: str,
        grantee: str,
        msg_type_url: str,
        pagination: "__base_query_v1_beta1__.PageRequest",
    ) -> "QueryGrantsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def granter_grants(
        self, granter: str, pagination: "__base_query_v1_beta1__.PageRequest"
    ) -> "QueryGranterGrantsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def grantee_grants(
        self, grantee: str, pagination: "__base_query_v1_beta1__.PageRequest"
    ) -> "QueryGranteeGrantsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_grants(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "granter": request.granter,
            "grantee": request.grantee,
            "msg_type_url": request.msg_type_url,
            "pagination": request.pagination,
        }

        response = await self.grants(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_granter_grants(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "granter": request.granter,
            "pagination": request.pagination,
        }

        response = await self.granter_grants(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_grantee_grants(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "grantee": request.grantee,
            "pagination": request.pagination,
        }

        response = await self.grantee_grants(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/cosmos.authz.v1beta1.Query/Grants": grpclib.const.Handler(
                self.__rpc_grants,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryGrantsRequest,
                QueryGrantsResponse,
            ),
            "/cosmos.authz.v1beta1.Query/GranterGrants": grpclib.const.Handler(
                self.__rpc_granter_grants,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryGranterGrantsRequest,
                QueryGranterGrantsResponse,
            ),
            "/cosmos.authz.v1beta1.Query/GranteeGrants": grpclib.const.Handler(
                self.__rpc_grantee_grants,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryGranteeGrantsRequest,
                QueryGranteeGrantsResponse,
            ),
        }


from ...base.query import v1beta1 as __base_query_v1_beta1__
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
