from secret_sdk.client.grpc.encryption import EncryptionUtils
from .protobuf.cosmos.auth.v1beta1 import QueryStub as authQueryStub
from .protobuf.cosmos.authz.v1beta1 import (
    QueryStub as authzQueryStub,
    MsgStub as authzMsgStub,
)
from .protobuf.cosmos.bank.v1beta1 import (
    QueryStub as bankQueryStub,
    MsgStub as bankMsgStub,
)
from .protobuf.cosmos.crisis.v1beta1 import MsgStub as crisisMsgStub
from .protobuf.cosmos.distribution.v1beta1 import (
    QueryStub as distributionQueryStub,
    MsgStub as distributionMsgStub,
)
from .protobuf.cosmos.evidence.v1beta1 import (
    QueryStub as evidenceQueryStub,
    MsgStub as evidenceMsgStub,
)
from .protobuf.cosmos.feegrant.v1beta1 import (
    QueryStub as feegrantQueryStub,
    MsgStub as feegrantMsgStub,
)
from .protobuf.cosmos.gov.v1beta1 import (
    QueryStub as govQueryStub,
    MsgStub as govMsgStub,
)
from .protobuf.cosmos.mint.v1beta1 import QueryStub as mintQueryStub
from .protobuf.cosmos.params.v1beta1 import QueryStub as paramsQueryStub
from .protobuf.cosmos.slashing.v1beta1 import (
    QueryStub as slashingQueryStub,
    MsgStub as slashingMsgStub,
)
from .protobuf.cosmos.staking.v1beta1 import (
    QueryStub as stakingQueryStub,
    MsgStub as stakingMsgStub,
)
from .protobuf.cosmos.upgrade.v1beta1 import QueryStub as upgradeQueryStub

from .protobuf.cosmos.tx.v1beta1 import ServiceStub as txServiceStub

from .protobuf.ibc.core.channel.v1 import (
    QueryStub as channelQueryStub,
    MsgStub as channelMsgStub,
)
from .protobuf.ibc.core.client.v1 import (
    QueryStub as clientQueryStub,
    MsgStub as clientMsgStub,
)
from .protobuf.ibc.core.connection.v1 import (
    QueryStub as connQueryStub,
    MsgStub as connMsgStub,
)
from .protobuf.ibc.applications.transfer.v1 import (
    QueryStub as transferQueryStub,
    MsgStub as transferMsgStub,
)

from .protobuf.secret.registration.v1beta1 import QueryStub as registrationQueryStub

from .protobuf.cosmos.base.tendermint.v1beta1 import (
    ServiceStub as tendermintServiceStub,
)
from .protobuf.cosmos.base.reflection.v1beta1 import (
    ReflectionServiceStub as reflectionServiceStub,
)

from .protobuf.tendermint.abci import AbciApplicationStub

from grpclib.client import Channel
import asyncio

from .query.compute import ComputeQuerier


class AsyncGRPCClient:
    def __init__(self, *, host, port) -> None:
        self.channel = Channel(host=host, port=port)
        # apis

        # query
        self.query = self.Query(self.channel)

        # serviceStub
        self.tendermint = tendermintServiceStub(self.channel)
        self.reflection = reflectionServiceStub(self.channel)

        # msg
        # self.msg = self.Msg(self.channel)

        # txs
        self.tx = txServiceStub(self.channel)

    def __del__(self) -> None:
        self.channel.close()

    class Query:
        def __init__(self, channel) -> None:
            self.auth = authQueryStub(channel)
            self.authz = authzQueryStub(channel)
            self.bank = bankQueryStub(channel)
            self.distribution = distributionQueryStub(channel)
            self.gov = govQueryStub(channel)
            self.evidence = evidenceQueryStub(channel)
            self.feegrant = feegrantQueryStub(channel)
            self.mint = mintQueryStub(channel)
            self.params = paramsQueryStub(channel)
            self.slashing = slashingQueryStub(channel)
            self.staking = stakingQueryStub(channel)
            self.upgrade = upgradeQueryStub(channel)
            self.ibc = self.IBCQuery(channel)
            self.secret = self.Secret(channel)

        class IBCQuery:
            def __init__(self, channel) -> None:
                self.core = self.Core(channel)
                self.applications = self.Applications(channel)

            class Core:
                def __init__(self, channel) -> None:
                    self.channel = channelQueryStub(channel)
                    self.client = clientQueryStub(channel)
                    self.connection = connQueryStub(channel)

            class Applications:
                def __init__(self, channel) -> None:
                    self.transfer = transferQueryStub(channel)

        class Secret:
            def __init__(self, channel) -> None:
                self.compute = ComputeQuerier(channel)

    # class Msg:
    #     def __init__(self, channel) -> None:
    #         self.authz = authzMsgStub(channel)
    #         self.distribution = distributionMsgStub(channel)
    #         self.bank = bankMsgStub(channel)
    #         self.crisis = crisisMsgStub(channel)
    #         self.evidence = evidenceMsgStub(channel)
    #         self.feegrant = feegrantMsgStub(channel)
    #         self.gov = govMsgStub(channel)
    #         self.slashing = slashingMsgStub(channel)
    #         self.staking = stakingMsgStub(channel)
    #         self.ibc = self.IBCMsg(channel)

    #     class IBCMsg:
    #         def __init__(self, channel) -> None:
    #             self.core = self.Core(channel)
    #             self.applications = self.Applications(channel)

    #         class Core:
    #             def __init__(self, channel) -> None:
    #                 self.channel = channelMsgStub(channel)
    #                 self.client = clientMsgStub(channel)
    #                 self.connection = connMsgStub(channel)

    #         class Applications:
    #             def __init__(self, channel) -> None:
    #                 self.transfer = transferMsgStub(channel)
