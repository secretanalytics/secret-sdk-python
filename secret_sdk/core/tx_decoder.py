from secret_sdk.protobuf.cosmos.base.v1beta1 import Coin
from secret_sdk.protobuf.cosmos.authz.v1beta1 import MsgGrant, MsgExec, MsgRevoke

from secret_sdk.protobuf.cosmos.bank.v1beta1 import MsgSend, MsgMultiSend

from secret_sdk.protobuf.cosmos.crisis.v1beta1 import MsgVerifyInvariant

from secret_sdk.protobuf.cosmos.distribution.v1beta1 import (
    MsgWithdrawDelegatorReward,
    MsgFundCommunityPool,
    MsgWithdrawValidatorCommission,
    MsgSetWithdrawAddress,
)

from secret_sdk.protobuf.cosmos.evidence.v1beta1 import MsgSubmitEvidence

from secret_sdk.protobuf.cosmos.feegrant.v1beta1 import MsgGrantAllowance, MsgRevokeAllowance
from secret_sdk.protobuf.cosmos.gov.v1beta1 import (
    MsgSubmitProposal,
    MsgVote,
    MsgVoteWeighted,
    MsgDeposit,
)

from secret_sdk.protobuf.cosmos.slashing.v1beta1 import MsgUnjail

from secret_sdk.protobuf.cosmos.staking.v1beta1 import (
    MsgCreateValidator,
    MsgEditValidator,
    MsgDelegate,
    MsgBeginRedelegate,
    MsgUndelegate,
)

from secret_sdk.protobuf.ibc.applications.transfer.v1 import MsgTransfer

from secret_sdk.protobuf.ibc.core.channel.v1 import (
    MsgChannelOpenInit,
    MsgChannelOpenTry,
    MsgChannelOpenAck,
    MsgChannelOpenConfirm,
    MsgChannelCloseInit,
    MsgChannelCloseConfirm,
    MsgRecvPacket,
    MsgTimeout,
    MsgTimeoutOnClose,
    MsgAcknowledgement,
)

from secret_sdk.protobuf.ibc.core.client.v1 import (
    MsgCreateClient,
    MsgUpdateClient,
    MsgUpgradeClient,
    MsgSubmitMisbehaviour,
)

from secret_sdk.protobuf.ibc.core.connection.v1 import (
    MsgConnectionOpenInit,
    MsgConnectionOpenTry,
    MsgConnectionOpenAck,
    MsgConnectionOpenConfirm,
)

from secret_sdk.protobuf.secret.compute.v1beta1 import (
    MsgStoreCode,
    MsgInstantiateContract,
    MsgExecuteContract,
)
from secret_sdk.protobuf.secret.registration.v1beta1 import RaAuthenticate


msg_decoder_mapper = {
    "/cosmos.authz.v1beta1.MsgGrant": MsgGrant,
    "/cosmos.authz.v1beta1.MsgExec": MsgExec,
    "/cosmos.authz.v1beta1.MsgRevoke": MsgRevoke,
    "/cosmos.bank.v1beta1.MsgSend": MsgSend,
    "/cosmos.bank.v1beta1.MsgMultiSend": MsgMultiSend,
    "/cosmos.crisis.v1beta1.MsgVerifyInvariant": MsgVerifyInvariant,
    "/cosmos.distribution.v1beta1.MsgSetWithdrawAddress": MsgSetWithdrawAddress,
    "/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward": MsgWithdrawDelegatorReward,
    "/cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission": MsgWithdrawValidatorCommission,
    "/cosmos.distribution.v1beta1.MsgFundCommunityPool": MsgFundCommunityPool,
    "/cosmos.evidence.v1beta1.MsgSubmitEvidence": MsgSubmitEvidence,
    "/cosmos.feegrant.v1beta1.MsgGrantAllowance": MsgGrantAllowance,
    "/cosmos.feegrant.v1beta1.MsgRevokeAllowance": MsgRevokeAllowance,
    "/cosmos.gov.v1beta1.MsgSubmitProposal": MsgSubmitProposal,
    "/cosmos.gov.v1beta1.MsgVote": MsgVote,
    "/cosmos.gov.v1beta1.MsgVoteWeighted": MsgVoteWeighted,
    "/cosmos.gov.v1beta1.MsgDeposit": MsgDeposit,
    "/cosmos.slashing.v1beta1.MsgUnjail": MsgUnjail,
    "/cosmos.staking.v1beta1.MsgCreateValidator": MsgCreateValidator,
    "/cosmos.staking.v1beta1.MsgEditValidator": MsgEditValidator,
    "/cosmos.staking.v1beta1.MsgDelegate": MsgDelegate,
    "/cosmos.staking.v1beta1.MsgBeginRedelegate": MsgBeginRedelegate,
    "/cosmos.staking.v1beta1.MsgUndelegate": MsgUndelegate,
    "/ibc.applications.transfer.v1.MsgTransfer": MsgTransfer,
    "/ibc.core.channel.v1.MsgChannelOpenInit": MsgChannelOpenInit,
    "/ibc.core.channel.v1.MsgChannelOpenTry": MsgChannelOpenTry,
    "/ibc.core.channel.v1.MsgChannelOpenAck": MsgChannelOpenAck,
    "/ibc.core.channel.v1.MsgChannelOpenConfirm": MsgChannelOpenConfirm,
    "/ibc.core.channel.v1.MsgChannelCloseInit": MsgChannelCloseInit,
    "/ibc.core.channel.v1.MsgChannelCloseConfirm": MsgChannelCloseConfirm,
    "/ibc.core.channel.v1.MsgRecvPacket": MsgRecvPacket,
    "/ibc.core.channel.v1.MsgTimeout": MsgTimeout,
    "/ibc.core.channel.v1.MsgTimeoutOnClose": MsgTimeoutOnClose,
    "/ibc.core.channel.v1.MsgAcknowledgement": MsgAcknowledgement,
    "/ibc.core.client.v1.MsgCreateClient": MsgCreateClient,
    "/ibc.core.client.v1.MsgUpdateClient": MsgUpdateClient,
    "/ibc.core.client.v1.MsgUpgradeClient": MsgUpgradeClient,
    "/ibc.core.client.v1.MsgSubmitMisbehaviour": MsgSubmitMisbehaviour,
    "/ibc.core.connection.v1.MsgConnectionOpenInit": MsgConnectionOpenInit,
    "/ibc.core.connection.v1.MsgConnectionOpenTry": MsgConnectionOpenTry,
    "/ibc.core.connection.v1.MsgConnectionOpenAck": MsgConnectionOpenAck,
    "/ibc.core.connection.v1.MsgConnectionOpenConfirm": MsgConnectionOpenConfirm,
    "/secret.compute.v1beta1.MsgStoreCode": MsgStoreCode,
    "/secret.compute.v1beta1.MsgInstantiateContract": MsgInstantiateContract,
    "/secret.compute.v1beta1.MsgExecuteContract": MsgExecuteContract,
    "/secret.registration.v1beta1.RaAuthenticate": RaAuthenticate,
}