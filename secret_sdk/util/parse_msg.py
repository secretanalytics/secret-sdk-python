from secret_sdk.core.bank import MsgMultiSend, MsgSend
from secret_sdk.core.distribution import (
    MsgFundCommunityPool,
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
)

from secret_sdk.core.wasm import (
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateContract,
    MsgStoreCode,
)

from .base import create_demux

bank_msgs = [MsgSend, MsgMultiSend]
distribution_msgs = [
    MsgFundCommunityPool,
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
]

wasm_msgs = [
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateContract,
    MsgStoreCode,
]

parse_msg = create_demux(
    [
        *bank_msgs,
        *distribution_msgs,
        *wasm_msgs,
    ]
)
