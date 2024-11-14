"Wasm module messages."

from __future__ import annotations

import base64
import json
import gzip
from typing import Optional, Union

import attr
from secret_sdk.util.address_converter import address_to_bytes, bytes_to_address
from secret_sdk.protobuf.secret.compute.v1beta1 import MsgExecuteContract as MsgExecuteContract_pb
from secret_sdk.protobuf.secret.compute.v1beta1 import (
    MsgInstantiateContract as MsgInstantiateContract_pb,
)
from secret_sdk.protobuf.secret.compute.v1beta1 import MsgStoreCode as MsgStoreCode_pb
from secret_sdk.core import AccAddress, Coins
from secret_sdk.core.msg import Msg
from secret_sdk.util.encrypt_utils import EncryptionUtils

__all__ = [
    "MsgStoreCode",
    "MsgInstantiateContract",
    "MsgExecuteContract"
]


def is_gz_file(byte_code):
    return byte_code[:2] == b'\x1f\x8b'


def parse_msg(msg: Union[dict, str, bytes]) -> dict:
    if type(msg) is dict:
        return msg
    try:
        msg = json.loads(msg)
    except:
        if isinstance(msg, str):
            msg = base64.b64decode(msg)
    return msg


@attr.s
class MsgStoreCode(Msg):
    """Upload a new smart contract WASM binary to the blockchain.

    Args:
        sender: address of sender
        wasm_byte_code: base64-encoded string containing bytecode
        instantiate_permission: access control to apply on contract creation, optional
    """

    type_amino = "wasm/MsgStoreCode"
    """"""
    type_url = "/secret.compute.v1beta1.MsgStoreCode"
    """"""
    prototype = MsgStoreCode_pb
    """"""

    sender: AccAddress = attr.ib()
    wasm_byte_code: bytes = attr.ib(converter=bytes)
    source: str = attr.ib(converter=str)
    builder: str = attr.ib(converter=str)

    def gzip_wasm(self):
        if not is_gz_file(self.wasm_byte_code):
            self.wasm_byte_code = gzip.compress(self.wasm_byte_code, compresslevel=9)

    def to_amino(self) -> dict:
        self.gzip_wasm()

        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "wasm_byte_code": self.wasm_byte_code,
                "source": self.source,
                "builder": self.builder
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgStoreCode:
        return cls(
            sender=data["sender"],
            wasm_byte_code=base64.b64decode(data["wasm_byte_code"]),
            source=data.get("source"),
            builder=data.get("builder")
        )

    def to_proto(self) -> MsgStoreCode_pb:
        self.gzip_wasm()

        return MsgStoreCode_pb(
            sender=address_to_bytes(self.sender),
            wasm_byte_code=self.wasm_byte_code,
            source=self.source,
            builder=self.builder
        )

    @classmethod
    def from_proto(cls, proto: MsgStoreCode_pb) -> MsgStoreCode:
        return cls(
            sender=AccAddress(bytes_to_address(proto.sender)),
            wasm_byte_code=base64.b64encode(proto.wasm_byte_code),
            source=proto.source,
            builder=proto.builder
        )


@attr.s
class MsgInstantiateContract(Msg):
    """Creates a new instance of a smart contract from existing code on the blockchain.

    Args:
        sender: address of sender
        code_id (int): code ID to use for instantiation
        label (str): label for the contract.
        init_msg (dict): InitMsg to initialize contract
        init_funds (Coins): initial amount of coins to be sent to contract
    """

    type_amino = "wasm/MsgInstantiateContract"
    """"""
    type_url = "/secret.compute.v1beta1.MsgInstantiateContract"
    """"""
    prototype = MsgInstantiateContract_pb
    """"""

    sender: AccAddress = attr.ib()
    code_id: int = attr.ib(converter=int)
    label: str = attr.ib(converter=str)
    init_msg: dict = attr.ib()
    init_funds: Coins = attr.ib(converter=Coins, factory=Coins)

    code_hash: str = attr.ib(default=None)

    init_msg_encrypted: dict = None
    warn_code_hash: bool = False
    _msg_str: str = ''

    encryption_utils: Optional[EncryptionUtils] = attr.ib(default=None)

    def __attrs_post_init__(self):
        if self.code_hash:
            self.code_hash = self.code_hash.replace('0x', '').lower()
        else:
            self.code_hash = ''
            self.warn_code_hash = True
            # print('WARNING: MsgInstantiateContract was used without the "codeHash" parameter. This is discouraged and will result in much slower execution times for your app.')

        if isinstance(self.init_msg, dict):
            self._msg_str = json.dumps(self.init_msg, separators=(",", ":"))

    @classmethod
    def from_data(cls, data: dict) -> MsgInstantiateContract:
        return cls(
            sender=data.get("sender"),
            code_id=data["code_id"],
            label=data["label"],
            init_msg=parse_msg(data["init_msg"]),
            init_funds=Coins.from_data(data["init_funds"]),
        )

    def to_proto(self) -> MsgInstantiateContract_pb:
        if not self.init_msg_encrypted and not self.encryption_utils:
            raise NotImplementedError('Cannot serialized MsgExecuteContract without encryption')
        if not self.init_msg_encrypted:
            self.init_msg_encrypted = bytes(self.encryption_utils.encrypt(self.code_hash, self._msg_str))

        return MsgInstantiateContract_pb(
            sender=address_to_bytes(self.sender),
            code_id=self.code_id,
            label=self.label,
            init_msg=self.init_msg_encrypted,
            init_funds=self.init_funds.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgInstantiateContract_pb) -> MsgInstantiateContract:
        return cls(
            sender=AccAddress(bytes_to_address(proto.sender)),
            code_id=proto.code_id,
            label=proto.label,
            init_msg=parse_msg(proto.init_msg),
            init_funds=Coins.from_proto(proto.init_funds),
        )


@attr.s
class MsgExecuteContract(Msg):
    """Execute a state-mutating function on a smart contract.

    Args:
        sender: address of sender
        contract: address of contract to execute function on
        msg (dict|str): ExecuteMsg to pass
        sent_funds: coins to be sent, if needed by contract to execute.
            Defaults to empty ``Coins()``
        code_hash: hash of the contract (optional)
    """

    type_amino = "wasm/MsgExecuteContract"
    """"""
    type_url = "/secret.compute.v1beta1.MsgExecuteContract"
    """"""
    prototype = MsgExecuteContract_pb
    """"""

    sender: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    msg: Union[dict, str] = attr.ib()
    sent_funds: Coins = attr.ib(converter=Coins, factory=Coins)
    code_hash: Optional[str] = attr.ib(default=None)

    msg_encrypted: Optional[bytes] = None
    warn_code_hash: bool = False
    _msg_str: str = ''

    encryption_utils: Optional[EncryptionUtils] = attr.ib(default=None)

    def __attrs_post_init__(self):
        if self.code_hash:
            self.code_hash = self.code_hash.replace('0x', '').lower()
        else:
            self.code_hash = ''
            self.warn_code_hash = True
            # print('WARNING: MsgExecuteContract was used without the "codeHash" parameter. This is discouraged and will result in much slower execution times for your app.')
        if isinstance(self.msg, (dict,)):
            self._msg_str = json.dumps(self.msg, separators=(",", ":"))
        else:
            self._msg_str = self.msg


    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        return cls(
            sender=data["sender"],
            contract=data["contract"],
            msg=parse_msg(data["msg"]),
            sent_funds=Coins.from_data(data["sent_funds"]),
        )

    def to_proto(self) -> MsgExecuteContract_pb:
        if not self.msg_encrypted and not self.encryption_utils:
            raise NotImplementedError('Cannot serialized MsgExecuteContract without encryption')
        if not self.msg_encrypted:
            self.msg_encrypted = bytes(self.encryption_utils.encrypt(self.code_hash, self._msg_str))

        return MsgExecuteContract_pb(
            sender=address_to_bytes(self.sender),
            contract=address_to_bytes(self.contract),
            msg=self.msg_encrypted,
            sent_funds=self.sent_funds.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgExecuteContract_pb) -> MsgExecuteContract:
        return cls(
            sender=AccAddress(bytes_to_address(proto.sender)),
            contract=AccAddress(bytes_to_address(proto.contract)),
            msg=parse_msg(proto.msg),
            sent_funds=Coins.from_proto(proto.sent_funds),
        )
