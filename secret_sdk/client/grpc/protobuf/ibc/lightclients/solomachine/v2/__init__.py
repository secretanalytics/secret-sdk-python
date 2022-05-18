# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: ibc/lightclients/solomachine/v2/solomachine.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class DataType(betterproto.Enum):
    """
    DataType defines the type of solo machine proof being created. This is done
    to preserve uniqueness of different data sign byte encodings.
    """

    # Default State
    DATA_TYPE_UNINITIALIZED_UNSPECIFIED = 0
    # Data type for client state verification
    DATA_TYPE_CLIENT_STATE = 1
    # Data type for consensus state verification
    DATA_TYPE_CONSENSUS_STATE = 2
    # Data type for connection state verification
    DATA_TYPE_CONNECTION_STATE = 3
    # Data type for channel state verification
    DATA_TYPE_CHANNEL_STATE = 4
    # Data type for packet commitment verification
    DATA_TYPE_PACKET_COMMITMENT = 5
    # Data type for packet acknowledgement verification
    DATA_TYPE_PACKET_ACKNOWLEDGEMENT = 6
    # Data type for packet receipt absence verification
    DATA_TYPE_PACKET_RECEIPT_ABSENCE = 7
    # Data type for next sequence recv verification
    DATA_TYPE_NEXT_SEQUENCE_RECV = 8
    # Data type for header verification
    DATA_TYPE_HEADER = 9


@dataclass(eq=False, repr=False)
class ClientState(betterproto.Message):
    """
    ClientState defines a solo machine client that tracks the current consensus
    state and if the client is frozen.
    """

    # latest sequence of the client state
    sequence: int = betterproto.uint64_field(1)
    # frozen sequence of the solo machine
    is_frozen: bool = betterproto.bool_field(2)
    consensus_state: "ConsensusState" = betterproto.message_field(3)
    # when set to true, will allow governance to update a solo machine client.
    # The client will be unfrozen if it is frozen.
    allow_update_after_proposal: bool = betterproto.bool_field(4)


@dataclass(eq=False, repr=False)
class ConsensusState(betterproto.Message):
    """
    ConsensusState defines a solo machine consensus state. The sequence of a
    consensus state is contained in the "height" key used in storing the
    consensus state.
    """

    # public key of the solo machine
    public_key: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(1)
    # diversifier allows the same public key to be re-used across different solo
    # machine clients (potentially on different chains) without being considered
    # misbehaviour.
    diversifier: str = betterproto.string_field(2)
    timestamp: int = betterproto.uint64_field(3)


@dataclass(eq=False, repr=False)
class Header(betterproto.Message):
    """Header defines a solo machine consensus header"""

    # sequence to update solo machine public key at
    sequence: int = betterproto.uint64_field(1)
    timestamp: int = betterproto.uint64_field(2)
    signature: bytes = betterproto.bytes_field(3)
    new_public_key: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(4)
    new_diversifier: str = betterproto.string_field(5)


@dataclass(eq=False, repr=False)
class Misbehaviour(betterproto.Message):
    """
    Misbehaviour defines misbehaviour for a solo machine which consists of a
    sequence and two signatures over different messages at that sequence.
    """

    client_id: str = betterproto.string_field(1)
    sequence: int = betterproto.uint64_field(2)
    signature_one: "SignatureAndData" = betterproto.message_field(3)
    signature_two: "SignatureAndData" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class SignatureAndData(betterproto.Message):
    """
    SignatureAndData contains a signature and the data signed over to create
    that signature.
    """

    signature: bytes = betterproto.bytes_field(1)
    data_type: "DataType" = betterproto.enum_field(2)
    data: bytes = betterproto.bytes_field(3)
    timestamp: int = betterproto.uint64_field(4)


@dataclass(eq=False, repr=False)
class TimestampedSignatureData(betterproto.Message):
    """
    TimestampedSignatureData contains the signature data and the timestamp of
    the signature.
    """

    signature_data: bytes = betterproto.bytes_field(1)
    timestamp: int = betterproto.uint64_field(2)


@dataclass(eq=False, repr=False)
class SignBytes(betterproto.Message):
    """SignBytes defines the signed bytes used for signature verification."""

    sequence: int = betterproto.uint64_field(1)
    timestamp: int = betterproto.uint64_field(2)
    diversifier: str = betterproto.string_field(3)
    # type of the data used
    data_type: "DataType" = betterproto.enum_field(4)
    # marshaled data
    data: bytes = betterproto.bytes_field(5)


@dataclass(eq=False, repr=False)
class HeaderData(betterproto.Message):
    """HeaderData returns the SignBytes data for update verification."""

    # header public key
    new_pub_key: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(1)
    # header diversifier
    new_diversifier: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class ClientStateData(betterproto.Message):
    """
    ClientStateData returns the SignBytes data for client state verification.
    """

    path: bytes = betterproto.bytes_field(1)
    client_state: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class ConsensusStateData(betterproto.Message):
    """
    ConsensusStateData returns the SignBytes data for consensus state
    verification.
    """

    path: bytes = betterproto.bytes_field(1)
    consensus_state: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(
        2
    )


@dataclass(eq=False, repr=False)
class ConnectionStateData(betterproto.Message):
    """
    ConnectionStateData returns the SignBytes data for connection state
    verification.
    """

    path: bytes = betterproto.bytes_field(1)
    connection: "___core_connection_v1__.ConnectionEnd" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class ChannelStateData(betterproto.Message):
    """
    ChannelStateData returns the SignBytes data for channel state verification.
    """

    path: bytes = betterproto.bytes_field(1)
    channel: "___core_channel_v1__.Channel" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class PacketCommitmentData(betterproto.Message):
    """
    PacketCommitmentData returns the SignBytes data for packet commitment
    verification.
    """

    path: bytes = betterproto.bytes_field(1)
    commitment: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class PacketAcknowledgementData(betterproto.Message):
    """
    PacketAcknowledgementData returns the SignBytes data for acknowledgement
    verification.
    """

    path: bytes = betterproto.bytes_field(1)
    acknowledgement: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class PacketReceiptAbsenceData(betterproto.Message):
    """
    PacketReceiptAbsenceData returns the SignBytes data for packet receipt
    absence verification.
    """

    path: bytes = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class NextSequenceRecvData(betterproto.Message):
    """
    NextSequenceRecvData returns the SignBytes data for verification of the
    next sequence to be received.
    """

    path: bytes = betterproto.bytes_field(1)
    next_seq_recv: int = betterproto.uint64_field(2)


from ....core.channel import v1 as ___core_channel_v1__
from ....core.connection import v1 as ___core_connection_v1__
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
