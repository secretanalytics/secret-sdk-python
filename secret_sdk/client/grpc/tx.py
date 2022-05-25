from .protobuf.cosmos.authz.v1beta1 import MsgGrant, MsgExec, MsgRevoke

from .protobuf.cosmos.bank.v1beta1 import MsgSend, MsgMultiSend

msg_decoder_mapper = {
    "/cosmos.authz.v1beta1.MsgGrant": MsgGrant,
    "/cosmos.authz.v1beta1.MsgExec": MsgExec,
    "/cosmos.authz.v1beta1.MsgRevoke": MsgRevoke,
    "/cosmos.bank.v1beta1.MsgSend": MsgSend,
    "/cosmos.bank.v1beta1.MsgMultiSend": MsgMultiSend,
}
