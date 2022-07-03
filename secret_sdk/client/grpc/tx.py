import base64
from dataclasses import dataclass
from typing import Any, List, Optional, TypedDict

from .protobuf.cosmos.base.v1beta1 import Coin
from .query.address import *
from .protobuf.cosmos.authz.v1beta1 import MsgGrant, MsgExec, MsgRevoke

from .protobuf.cosmos.bank.v1beta1 import MsgSend, MsgMultiSend

from .protobuf.cosmos.crisis.v1beta1 import MsgVerifyInvariant

from .protobuf.cosmos.distribution.v1beta1 import (
    MsgWithdrawDelegatorReward,
    MsgFundCommunityPool,
    MsgWithdrawValidatorCommission,
    MsgSetWithdrawAddress,
)

from .protobuf.cosmos.evidence.v1beta1 import MsgSubmitEvidence

from .protobuf.cosmos.feegrant.v1beta1 import MsgGrantAllowance, MsgRevokeAllowance
from .protobuf.cosmos.gov.v1beta1 import (
    MsgSubmitProposal,
    MsgVote,
    MsgVoteWeighted,
    MsgDeposit,
)

from .protobuf.cosmos.slashing.v1beta1 import MsgUnjail

from .protobuf.cosmos.staking.v1beta1 import (
    MsgCreateValidator,
    MsgEditValidator,
    MsgDelegate,
    MsgBeginRedelegate,
    MsgUndelegate,
)

from .protobuf.ibc.applications.transfer.v1 import MsgTransfer

from .protobuf.ibc.core.channel.v1 import (
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

from .protobuf.ibc.core.client.v1 import (
    MsgCreateClient,
    MsgUpdateClient,
    MsgUpgradeClient,
    MsgSubmitMisbehaviour,
)

from .protobuf.ibc.core.connection.v1 import (
    MsgConnectionOpenInit,
    MsgConnectionOpenTry,
    MsgConnectionOpenAck,
    MsgConnectionOpenConfirm,
)

from .protobuf.secret.compute.v1beta1 import (
    MsgStoreCode,
    MsgInstantiateContract,
    MsgExecuteContract,
)

from .protobuf.secret.registration.v1beta1 import RaAuthenticate


@dataclass
class DecodedMsgExecuteContract:
    sender: str
    contract: str
    msg: str  # hex string of bytes
    sent_funds: List[Coin]
    callback_code_hash: str
    callback_sig: bytes  # hex string of bytes


def decode_msg_execute_contract(msg: MsgExecuteContract) -> DecodedMsgExecuteContract:
    return DecodedMsgExecuteContract(
        sender=bytes_to_address(msg.sender),
        contract=bytes_to_address(msg.contract),
        msg=msg.msg.hex(),
        callback_code_hash=msg.callback_code_hash,
        sent_funds=msg.sent_funds,
        callback_sig=msg.callback_sig.hex(),
    )


class Message(TypedDict):
    type_url: str
    value: Any


def get_msg(type_url, msg_bytes):
    msg_decoder = msg_decoder_mapper[type_url]
    if not msg_decoder:
        return

    proto_msg = msg_decoder.FromString(base64.b64decode(msg_bytes))
    # get decoded msg will return the original proto_msg if no decoder is found
    msg: Message = Message(type_url=type_url, value=get_decoded_protobuf_msg(proto_msg))

    return msg


def get_decoded_protobuf_msg(proto_msg):
    try:
        proto_decoder = msg_protobuf_decoder_mapper[type(proto_msg)]
        if not proto_decoder:
            return proto_msg
    except:
        return proto_msg
    decoded = proto_decoder(proto_msg)
    return decoded


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

msg_protobuf_decoder_mapper = {MsgExecuteContract: decode_msg_execute_contract}
