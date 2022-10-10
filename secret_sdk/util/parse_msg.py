# core msgs
from secret_sdk.core.auth import(
    MsgCreateVestingAccount
)
from secret_sdk.core.authz import (
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
)
from secret_sdk.core.bank import MsgMultiSend, MsgSend
from secret_sdk.core.crisis import MsgVerifyInvariant
from secret_sdk.core.distribution import (
    MsgFundCommunityPool,
    MsgSetWithdrawAddress,
    MsgWithdrawDelegatorReward,
    MsgWithdrawValidatorCommission,
)
from secret_sdk.core.feegrant import MsgGrantAllowance, MsgRevokeAllowance
from secret_sdk.core.gov.msgs import MsgDeposit, MsgSubmitProposal, MsgVote
from secret_sdk.core.ibc.msgs import (
    MsgAcknowledgement,
    MsgChannelCloseConfirm,
    MsgChannelCloseInit,
    MsgChannelOpenAck,
    MsgChannelOpenConfirm,
    MsgChannelOpenInit,
    MsgChannelOpenTry,
    MsgConnectionOpenAck,
    MsgConnectionOpenConfirm,
    MsgConnectionOpenInit,
    MsgConnectionOpenTry,
    MsgCreateClient,
    MsgRecvPacket,
    MsgSubmitMisbehaviour,
    MsgTimeout,
    MsgUpdateClient,
    MsgUpgradeClient,
)
from secret_sdk.core.ibc_transfer import MsgTransfer
from secret_sdk.core.slashing import MsgUnjail
from secret_sdk.core.staking import (
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
)
from secret_sdk.core.wasm import (
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgStoreCode,
)

from .base import create_demux, create_demux_proto, create_demux_unpack_any
auth_msgs = [
    MsgCreateVestingAccount,
]
bank_msgs = [MsgSend, MsgMultiSend]
distribution_msgs = [
    MsgFundCommunityPool,
    MsgSetWithdrawAddress,
    MsgWithdrawDelegatorReward,
    MsgWithdrawValidatorCommission,
]
gov_msgs = [MsgDeposit, MsgSubmitProposal, MsgVote]
authz_msgs = [
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
]
slashing_msgs = [MsgUnjail]
staking_msgs = [
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
]
wasm_msgs = [
    MsgStoreCode,
    MsgInstantiateContract,
    MsgExecuteContract,
]
feegrant_msgs = [MsgGrantAllowance, MsgRevokeAllowance]

ibc_transfer_msgs = [MsgTransfer]
ibc_msgs = [
    MsgCreateClient,
    MsgUpdateClient,
    MsgUpgradeClient,
    MsgSubmitMisbehaviour,
    MsgConnectionOpenInit,
    MsgConnectionOpenTry,
    MsgConnectionOpenAck,
    MsgConnectionOpenConfirm,
    MsgChannelOpenInit,
    MsgChannelOpenTry,
    MsgChannelOpenAck,
    MsgChannelOpenConfirm,
    MsgChannelCloseInit,
    MsgChannelCloseConfirm,
    MsgRecvPacket,
    MsgTimeout,
    MsgAcknowledgement,
]
crisis_msgs = [MsgVerifyInvariant]

parse_msg = create_demux(
    [
        *auth_msgs,
        *authz_msgs,
        *bank_msgs,
        *distribution_msgs,
        *feegrant_msgs,
        *gov_msgs,
        *slashing_msgs,
        *staking_msgs,
        *wasm_msgs,
        *ibc_msgs,
        *ibc_transfer_msgs,
        *crisis_msgs,
    ]
)

parse_proto = create_demux_proto(
    [
        *auth_msgs,
        *authz_msgs,
        *bank_msgs,
        *distribution_msgs,
        *feegrant_msgs,
        *gov_msgs,
        *slashing_msgs,
        *staking_msgs,
        *wasm_msgs,
        *ibc_msgs,
        *ibc_transfer_msgs,
        *crisis_msgs,
    ]
)


parse_unpack_any = create_demux_unpack_any(
    [
        *auth_msgs,
        *authz_msgs,
        *bank_msgs,
        *distribution_msgs,
        *feegrant_msgs,
        *gov_msgs,
        *slashing_msgs,
        *staking_msgs,
        *wasm_msgs,
        *ibc_msgs,
        *ibc_transfer_msgs,
        *crisis_msgs,
    ]
)
