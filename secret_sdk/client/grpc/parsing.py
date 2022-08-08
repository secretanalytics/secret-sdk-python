import base64
from dataclasses import dataclass
from enum import Enum
import json
import re
from typing import Any, Dict, List, TypedDict

from betterproto import Casing
from .encryption import EncryptionUtils
from .protobuf.cosmos.base.abci.v1beta1 import (
    TxMsgData,
    TxResponse,
)

from .protobuf.cosmos.tx.v1beta1 import AuthInfo
from .protobuf.tendermint.abci import Event as abciEvent

from .tx import get_msg

from .protobuf.cosmos.tx.v1beta1 import (
    AuthInfo,
    Tx as orgTx,
)


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


@dataclass
class ArrayLogElem:
    msg: int
    type: str
    key: str
    value: str


class Attribute(TypedDict):
    key: str
    value: str
    index: bool


class Event(TypedDict):
    type: str
    attributes: List[Attribute]


class JsonLogElem(TypedDict):
    msg_index: int
    events: List[Event]


class Message(TypedDict):
    type_url: str
    value: Any


class TxBody(TypedDict):
    messages: List[Message]
    memo: str
    timeout_height: str
    extension_options: Any
    non_critical_extension_options: Any


@dataclass
class TxContent:
    body: TxBody
    auth_info: AuthInfo
    signatures: List[int]


@dataclass
class Tx:
    """
    All of these types were ported from [secret.js](https://github.com/scrtlabs/secret.js/blob/0b2010110b0d172e92db69f1861bf1de10351582/src/secret_network_client.ts#L351)
    Look there for docs
    Disabled certain elements as it is duplicated data, formatted differently
    """

    height: int
    transaction_hash: str
    code: TxResultCode
    raw_log: str
    json_log: List[JsonLogElem]  # should be from json.loads
    # array_log: List[ArrayLogElem] # all arrow long info is included in json log so seems just like extra info in my opinion (left code so can be reenabled)
    events: List[abciEvent]
    data: List[int]
    tx: TxContent
    # tx_bytes: List[int] disabled because this is parsed out elsewhere
    gas_used: int
    gas_wanted: int


# this logic is copied from https://github.com/scrtlabs/secret.js/blob/0b2010110b0d172e92db69f1861bf1de10351582/src/secret_network_client.ts#L879
async def parse_tx(
    tx: TxResponse,
    encryption: EncryptionUtils,
    nonces: Dict = {},
) -> Tx:
    raw_log = tx.raw_log
    json_log: List[JsonLogElem()] = []
    array_log: List[ArrayLogElem()] = []

    if tx.code == 0 and raw_log != "":
        json_log = [JsonLogElem(**i) for i in json.loads(raw_log)]
        # print(f"{json_log=}")
        array_log = []
        for msg_index in range(len(json_log)):
            if "msg_index" not in json_log[msg_index]:
                json_log[msg_index]["msg_index"] = msg_index

            log = json_log[msg_index]
            for event in log["events"]:
                # print(f"\n {event=}")
                for attr in event["attributes"]:
                    if event["type"] == "wasm":
                        try:
                            nonce = nonces[msg_index]
                        except:
                            nonce = None
                        if nonce and len(nonce) == 32:
                            try:  # try to decode key
                                attr["key"] = (
                                    (
                                        await encryption.decrypt(
                                            base64.b64decode(attr["key"]),
                                            nonce=nonce,
                                        )
                                    )
                                    .decode()
                                    .strip()
                                )

                            except:
                                pass
                            try:  # try to decode value
                                attr["value"] = (
                                    (
                                        await encryption.decrypt(
                                            base64.b64decode(attr["value"]),
                                            nonce=nonce,
                                        )
                                    )
                                    .decode()
                                    .strip()
                                )
                            except:
                                pass
                        # print(event)

                    array_log.append(
                        ArrayLogElem(
                            msg=msg_index,
                            type=event["type"],
                            key=attr["key"],
                            value=attr["value"] if "value" in attr else "",
                        )
                    )

    elif tx.code != 0 and raw_log != "":
        try:
            err_message_re = re.compile(
                "/; message index: (\d+): encrypted: (.+?): (?:instantiate|execute|query) contract failed/g;"
            )
            rgx_matches = err_message_re.match(raw_log)
            # print(f"{rgx_matches}")
            if len(rgx_matches) == 3:
                encrypted_err = base64.b64decode(rgx_matches[3])
                msg_index = int(rgx_matches[1])

                decrypted_b64_err = await encryption.decrypt(
                    encrypted_err, nonce=nonces[msg_index]
                )

                decrypted_err = decrypted_b64_err.decode()

                raw_log = raw_log.replace(f"encrypted: {rgx_matches[2]}", decrypted_err)

                try:
                    json_log = json.loads(decrypted_err)
                except:
                    pass

        except:
            # Not encrypted or can't decrypt because not original sender
            pass

    # print("")
    # print(f"final_{json_log=}")
    # print(f"final_{array_log=}")

    tx_msg_data = TxMsgData()
    tx_msg_data = tx_msg_data.FromString(data=bytes.fromhex(tx.data))
    # print(f"og_{tx_msg_data=}")
    data = []

    for msg_index in range(len(tx_msg_data.data)):
        try:
            nonce = nonces[msg_index]
        except:
            nonce = None
        if nonce and len(nonce) == 32:
            try:
                # note: secret.js has the following two lines outside of try but I moved them in cause you can't decrypt without a nonce?
                data.append(
                    base64.b64decode(
                        (
                            await encryption.decrypt(
                                tx_msg_data.data[msg_index].data, nonce
                            )
                        ).decode()
                    )
                )
            except:
                # Not encrypted or can't decrypt because not original sender
                data.append(tx_msg_data.data[msg_index].data)

    # print(f"final_{data=}", "\n")

    decoded_tx = orgTx
    decoded_tx = decoded_tx.FromString(tx.tx.value)
    decoded_tx = TxContent(**decoded_tx.to_dict(casing=Casing.SNAKE))

    for i in range(len(decoded_tx.body["messages"])):
        msg_type, msg_bytes = decoded_tx.body["messages"][i].values()

        # print(f"{msg_bytes=}")

        msg = get_msg(msg_type, msg_bytes)

        # check if it needs decryption
        contract_input_msg_field_name = ""
        if msg["type_url"] == "/secret.compute.v1beta1.MsgInstantiateContract":
            contract_input_msg_field_name = "initMsg"
        elif msg["type_url"] == "/secret.compute.v1beta1.MsgExecuteContract":
            contract_input_msg_field_name = "msg"

        if contract_input_msg_field_name != "":
            # Encrypted, try to decrypt
            try:
                contract_input_msg_bytes = msg.value[contract_input_msg_field_name]

                nonce = contract_input_msg_bytes[0:32]
                # account pubkey not used
                ciphertext = contract_input_msg_bytes[64:]
                plaintext = await encryption.decrypt(
                    ciphertext,
                    nonce,
                )

                msg.value[contract_input_msg_field_name] = json.loads(
                    plaintext.decode()
                )[
                    64:
                ]  # first 64 chars is the codeHash as a hex string

            except:
                # Not encrypted or can't decrypt because not original sender
                pass

        # print(f"\n\n{msg=}\n\n")

        decoded_tx.body["messages"][i] = msg

    # print("\n", f"final_{decoded_tx=}")
    parsed_events = []
    for event in tx.events:
        parsed_attributes = []
        for attribute in event.attributes:
            try:
                key = attribute.key.decode()
            except:
                key = str(attribute.key)

            try:
                value = attribute.value.decode()
            except:
                value = attribute.value
            parsed_attributes.append(
                Attribute(key=key, value=value, index=attribute.index)
            )

        event = Event(type=event.type, attributes=parsed_attributes)
        parsed_events.append(event)
    # print(f"final_{parsed_events=}")

    return Tx(
        height=tx.height,
        transaction_hash=tx.txhash,
        code=tx.code,
        tx=decoded_tx,
        # tx_bytes=tx.tx.value if tx.tx.value else None,
        raw_log=raw_log,
        json_log=json_log,
        # array_log=array_log,
        events=parsed_events,
        data=data,
        gas_used=tx.gas_used,
        gas_wanted=tx.gas_wanted,
    )
