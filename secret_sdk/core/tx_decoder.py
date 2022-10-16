from enum import Enum
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


class TxResultCode(Enum):
    # Success is returned if the transaction executed successfuly
    Success = 0

    # ErrInternal should never be exposed, but we reserve this code for non-specified errors
    ErrInternal = 1

    # ErrTxDecode is returned if we cannot parse a transaction
    ErrTxDecode = 2

    # ErrInvalidSequence is used the sequence number (nonce) is incorrect for the signature
    ErrInvalidSequence = 3

    # ErrUnauthorized is used whenever a request without sufficient authorization is handled.
    ErrUnauthorized = 4

    # ErrInsufficientFunds is used when the account cannot pay requested amount.
    ErrInsufficientFunds = 5

    # ErrUnknownRequest to doc
    ErrUnknownRequest = 6

    # ErrInvalidAddress to doc
    ErrInvalidAddress = 7

    # ErrInvalidPubKey to doc
    ErrInvalidPubKey = 8

    # ErrUnknownAddress to doc
    ErrUnknownAddress = 9

    # ErrInvalidCoins to doc
    ErrInvalidCoins = 10

    # ErrOutOfGas to doc
    ErrOutOfGas = 11

    # ErrMemoTooLarge to doc
    ErrMemoTooLarge = 12

    # ErrInsufficientFee to doc
    ErrInsufficientFee = 13

    # ErrTooManySignatures to doc
    ErrTooManySignatures = 14

    # ErrNoSignatures to doc
    ErrNoSignatures = 15

    # ErrJSONMarshal defines an ABCI typed JSON marshalling error
    ErrJSONMarshal = 16

    # ErrJSONUnmarshal defines an ABCI typed JSON unmarshalling error
    ErrJSONUnmarshal = 17

    # ErrInvalidRequest defines an ABCI typed error where the request contains invalid data.
    ErrInvalidRequest = 18

    # ErrTxInMempoolCache defines an ABCI typed error where a tx already exists in the mempool.
    ErrTxInMempoolCache = 19

    # ErrMempoolIsFull defines an ABCI typed error where the mempool is full.
    ErrMempoolIsFull = 20

    # ErrTxTooLarge defines an ABCI typed error where tx is too large.
    ErrTxTooLarge = 21

    # ErrKeyNotFound defines an error when the key doesn't exist
    ErrKeyNotFound = 22

    # ErrWrongPassword defines an error when the key password is invalid.
    ErrWrongPassword = 23

    # ErrorInvalidSigner defines an error when the tx intended signer does not match the given signer.
    ErrorInvalidSigner = 24

    # ErrorInvalidGasAdjustment defines an error for an invalid gas adjustment
    ErrorInvalidGasAdjustment = 25

    # ErrInvalidHeight defines an error for an invalid height
    ErrInvalidHeight = 26

    # ErrInvalidVersion defines a general error for an invalid version
    ErrInvalidVersion = 27

    # ErrInvalidChainID defines an error when the chain-id is invalid.
    ErrInvalidChainID = 28

    # ErrInvalidType defines an error an invalid type.
    ErrInvalidType = 29

    # ErrTxTimeoutHeight defines an error for when a tx is rejected out due to an explicitly set timeout height.
    ErrTxTimeoutHeight = 30

    # ErrUnknownExtensionOptions defines an error for unknown extension options.
    ErrUnknownExtensionOptions = 31

    # ErrWrongSequence defines an error where the account sequence defined in the signer info doesn't match the account's actual sequence number.
    ErrWrongSequence = 32

    # ErrPackAny defines an error when packing a protobuf message to Any fails.
    ErrPackAny = 33

    # ErrUnpackAny defines an error when unpacking a protobuf message from Any fails.
    ErrUnpackAny = 34

    # ErrLogic defines an internal logic error, e.g. an invariant or assertion that is violated. It is a programmer error, not a user-facing error.
    ErrLogic = 35

    # ErrConflict defines a conflict error, e.g. when two go routines try to access the same resource and one of them fails.
    ErrConflict = 36

    # ErrNotSupported is returned when we call a branch of a code which is currently not supported.
    ErrNotSupported = 37

    # ErrNotFound defines an error when requested entity doesn't exist in the state.
    ErrNotFound = 38

    # ErrIO should be used to wrap internal errors caused by external operation. Examples: not DB domain error file writing etc...
    ErrIO = 39

    # ErrAppConfig defines an error occurred if min-gas-prices field in BaseConfig is empty.
    ErrAppConfig = 40

    # ErrPanic is only set when we recover from a panic so we know to redact potentially sensitive system info.
    ErrPanic = 111222