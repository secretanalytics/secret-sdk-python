from terra_sdk.core.bank import MsgMultiSend, MsgSend
from terra_sdk.core.distribution import (
    MsgFundCommunityPool,
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
)
from terra_sdk.core.gov.msgs import MsgDeposit, MsgSubmitProposal, MsgVote
from terra_sdk.core.slashing import MsgUnjail
from terra_sdk.core.staking import (
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
)
from terra_sdk.core.wasm import (
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateContract,
    MsgStoreCode,
    MsgUpdateContractOwner,
)

from .base import create_demux

bank_msgs = [MsgSend, MsgMultiSend]
distribution_msgs = [
    MsgFundCommunityPool,
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
]
gov_msgs = [MsgDeposit, MsgSubmitProposal, MsgVote]
slashing_msgs = [MsgUnjail]
staking_msgs = [
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
]
wasm_msgs = [
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateContract,
    MsgStoreCode,
    MsgUpdateContractOwner,
]

parse_msg = create_demux(
    [
        *bank_msgs,
        *distribution_msgs,
        *gov_msgs,
        *slashing_msgs,
        *staking_msgs,
        *wasm_msgs,
    ]
)
