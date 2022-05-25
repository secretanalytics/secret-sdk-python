from atexit import register
import base64
from curses import noecho
from dataclasses import dataclass
from enum import Enum
import json
import re
from typing import Any, Dict, List, TypedDict

from bech32 import decode
from betterproto import Casing

from secret_sdk.client.grpc.encryption import EncryptionUtils
from secret_sdk.client.grpc.protobuf.cosmos.base.abci.v1beta1 import (
    TxMsgData,
    TxResponse,
)
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

from secret_sdk.client.grpc.protobuf.cosmos.tx.v1beta1 import (
    BroadcastMode,
    ServiceStub as txServiceStub,
    AuthInfo,
    TxBody as orgTxBody,
    Tx as orgTx,
)

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

from .protobuf.tendermint.abci import AbciApplicationStub, Event as abciEvent

from grpclib.client import Channel
import asyncio

from .query.compute import ComputeQuerier

from .tx import msg_decoder_mapper


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
    """

    height: int
    transaction_hash: str
    tx_result_code: TxResultCode
    raw_log: str
    json_log: List[JsonLogElem]  # should be from json.loads
    array_log: List[ArrayLogElem]
    events: List[abciEvent]
    data: List[int]
    tx: TxContent
    tx_bytes: List[int]
    gas_used: int
    gas_wanted: int


class BroadcastMode(Enum):
    Sync = "Sync"
    Async = "Async"


class AsyncGRPCClient:
    def __init__(self, *, host: str, port: str) -> None:
        self.channel = Channel(host=host, port=port)
        # apis

        # encryption
        self.encryption = EncryptionUtils(self.channel)

        # query
        self.query = self.Query(self.channel)

        # serviceStub
        self.tendermint = tendermintServiceStub(self.channel)
        self.reflection = reflectionServiceStub(self.channel)

        # msg
        self.msg = self.Msg(self.channel)

        # txs
        self.txService = txServiceStub(self.channel)

        self.msg_decoder_mapper = msg_decoder_mapper

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

    class Msg:
        def __init__(self, channel) -> None:
            self.authz = authzMsgStub(channel)
            self.distribution = distributionMsgStub(channel)
            self.bank = bankMsgStub(channel)
            self.crisis = crisisMsgStub(channel)
            self.evidence = evidenceMsgStub(channel)
            self.feegrant = feegrantMsgStub(channel)
            self.gov = govMsgStub(channel)
            self.slashing = slashingMsgStub(channel)
            self.staking = stakingMsgStub(channel)
            self.ibc = self.IBCMsg(channel)

        class IBCMsg:
            def __init__(self, channel) -> None:
                self.core = self.Core(channel)
                self.applications = self.Applications(channel)

            class Core:
                def __init__(self, channel) -> None:
                    self.channel = channelMsgStub(channel)
                    self.client = clientMsgStub(channel)
                    self.connection = connMsgStub(channel)

            class Applications:
                def __init__(self, channel) -> None:
                    self.transfer = transferMsgStub(channel)

    async def get_tx(self, hash: str, nonces: Dict = {}) -> Tx:
        query = f"tx.hash='{hash}'"
        results = await self.txs_query(query=query)
        if results:
            return results
        else:
            return None

    async def txs_query(self, query: str, nonces: Dict = {}) -> List[Tx]:
        events = [q.strip() for q in query.split(" AND ")]
        result = await self.txService.get_txs_event(events=events)
        tx_responses = result.tx_responses
        print(f"\n{result=}\n")
        # str_response = json.dumps(result.tx_responses, indent=4)
        # print(str_response)
        print(json.dumps(tx_responses[0].to_dict(), indent=4))

        # this logic is copied from https://github.com/scrtlabs/secret.js/blob/0b2010110b0d172e92db69f1861bf1de10351582/src/secret_network_client.ts#L879
        async def parse_tx(tx: TxResponse) -> Tx:
            raw_log = tx.raw_log
            json_log: List[JsonLogElem()] = []
            array_log: List[ArrayLogElem()] = []

            if tx.code == 0 and raw_log != "":
                json_log = [JsonLogElem(**i) for i in json.loads(raw_log)]
                print(f"{json_log=}")
                array_log = []
                for msg_index in range(len(json_log)):
                    if "msg_index" not in json_log[msg_index]:
                        json_log[msg_index]["msg_index"] = msg_index

                    log = json_log[msg_index]
                    for event in log["events"]:
                        print(f"\n {event=}")
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
                                                await self.encryption.decrypt(
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
                                                await self.encryption.decrypt(
                                                    base64.b64decode(attr["value"]),
                                                    nonce=nonce,
                                                )
                                            )
                                            .decode()
                                            .strip()
                                        )
                                    except:
                                        pass
                                array_log.append(
                                    ArrayLogElem(
                                        msg=msg_index,
                                        type=event.type,
                                        key=attr["key"],
                                        value=attr["value"],
                                    )
                                )
            elif tx.code != 0 and raw_log != "":
                try:
                    err_message_re = re.compile(
                        "/; message index: (\d+): encrypted: (.+?): (?:instantiate|execute|query) contract failed/g;"
                    )
                    rgx_matches = err_message_re.match(raw_log)
                    print(f"{rgx_matches}")
                    if len(rgx_matches) == 3:
                        encrypted_err = base64.b64decode(rgx_matches[3])
                        msg_index = int(rgx_matches[1])

                        decrypted_b64_err = await self.encryption.decrypt(
                            encrypted_err, nonce=nonces[msg_index]
                        )

                        decrypted_err = decrypted_b64_err.decode()

                        raw_log = raw_log.replace(
                            f"encrypted: {rgx_matches[2]}", decrypted_err
                        )

                        try:
                            json_log = json.loads(decrypted_err)
                        except:
                            pass

                except:
                    # Not encrypted or can't decrypt because not original sender
                    pass

            print("")
            print(f"final_{json_log=}")

            tx_msg_data = TxMsgData()
            tx_msg_data = tx_msg_data.FromString(data=bytes.fromhex(tx.data))
            print(f"og_{tx_msg_data=}")
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
                                    await self.encryption.decrypt(
                                        tx_msg_data.data[msg_index].data, nonce
                                    )
                                ).decode()
                            )
                        )
                    except:
                        # Not encrypted or can't decrypt because not original sender

                        data.append(tx_msg_data.data[msg_index].data)

            print(f"final_{data=}", "\n")

            # still have to do decoded tx
            decoded_tx = orgTx
            decoded_tx = decoded_tx.FromString(tx.tx.value)
            decoded_tx = TxContent(**decoded_tx.to_dict(casing=Casing.SNAKE))
            print("\n", f"og_{decoded_tx=}")
            for i in range(len(decoded_tx.body["messages"])):
                msg_type, msg_bytes = decoded_tx.body["messages"][i].values()

                msg_decoder = self.msg_decoder_mapper[msg_type]
                if not msg_decoder:
                    continue
                print(f"\n{msg_bytes=}")
                msg: Message = Message(
                    type_url=msg_type, value=msg_decoder(bytes(msg_bytes, "utf-8"))
                )

                print(f"{msg=}")

                # check if it needs decryption
                contract_input_msg_field_name = ""
                if msg["type_url"] == "/secret.compute.v1beta1.MsgInstantiateContract":
                    contract_input_msg_field_name = "initMsg"
                elif msg["type_url"] == "/secret.compute.v1beta1.MsgExecuteContract":
                    contract_input_msg_field_name = "msg"

                if contract_input_msg_field_name != "":
                    # Encrypted, try to decrypt
                    try:
                        contract_input_msg_bytes = msg.value[
                            contract_input_msg_field_name
                        ]

                        nonce = contract_input_msg_bytes[0:32]
                        # account pubkey not used
                        ciphertext = contract_input_msg_bytes[64:]
                        plaintext = await self.encryption.decrypt(
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

                decoded_tx.body["messages"].append(msg)

            print("\n", f"final_{decoded_tx=}")

            return Tx(
                height=tx.height,
                transaction_hash=tx.txhash,
                tx_result_code=tx.code,
                tx=decoded_tx,
                tx_bytes=tx.tx.value if tx.tx.value else None,
                raw_log=raw_log,
                json_log=json_log,
                array_log=array_log,
                events=tx.events,
                data=data,
                gas_used=tx.gas_used,
                gas_wanted=tx.gas_wanted,
            )

        return [await parse_tx(tx) for tx in tx_responses]
