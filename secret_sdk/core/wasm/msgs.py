"Wasm module messages."

from __future__ import annotations

import base64
import json
from typing import Optional, Union

import attr
from secret_sdk.protobuf.secret.compute.v1beta1 import MsgExecuteContract as MsgExecuteContract_pb
from secret_sdk.protobuf.secret.compute.v1beta1 import (
    MsgInstantiateContract as MsgInstantiateContract_pb,
)
from secret_sdk.protobuf.secret.compute.v1beta1 import MsgStoreCode as MsgStoreCode_pb

from secret_sdk.core import AccAddress, Coins
from secret_sdk.core.msg import Msg
from secret_sdk.util.remove_none import remove_none

__all__ = [
    "MsgStoreCode",
    "MsgInstantiateContract",
    "MsgExecuteContract"
]


def parse_msg(msg: Union[dict, str, bytes]) -> dict:
    if type(msg) is dict:
        return msg
    try:
        msg = json.loads(msg)
    except:
        pass
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
    wasm_byte_code: str = attr.ib(converter=str)
    source: str = attr.ib(converter=str)
    builder: str = attr.ib(converter=str)

    # async def gzip_wasm(self):
    #     if not is_gzip(self.wasm_byte_code):
    #         self.wasm_byte_code = gzip(self.wasm_byte_code, level=9)

    def to_amino(self) -> dict:
        # await self.gzip_wasm()

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
            wasm_byte_code=data["wasm_byte_code"],
            source=data.get("source"),
            builder=data.get("builder")
        )

    def to_proto(self) -> MsgStoreCode_pb:
        # await self.gzip_wasm()

        return MsgStoreCode_pb(
            sender=self.sender,
            wasm_byte_code=base64.b64decode(self.wasm_byte_code),
            source=self.source,
            builder=self.builder
        )

    @classmethod
    def from_proto(cls, proto: MsgStoreCode_pb) -> MsgStoreCode:
        return cls(
            sender=proto.sender,
            wasm_byte_code=base64.b64encode(proto.wasm_byte_code).decode(),
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

    init_msg_encrypted: dict = None
    code_hash: str = None
    warn_code_hash: bool = False

    def __attrs_post_init__(self):
        if self.code_hash:
            self.code_hash = self.code_hash.replace('0x', '').lower()
        else:
            self.code_hash = ''
            self.warn_code_hash = True
            # print('WARNING: MsgInstantiateContract was used without the "codeHash" parameter. This is discouraged and will result in much slower execution times for your app.')

    def to_amino(self) -> dict:
        if not self.init_msg_encrypted:
            # The encryption uses a random nonce
            # toProto() & toAmino() are called multiple times during signing
            # so to keep the msg consistant across calls we encrypt the msg only once
            pass
            # self.init_msg_encrypted = await utils.encrypt(self.code_hash, self.init_msg)

        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "code_id": str(self.code_id),
                "label": self.label,
                "init_msg": remove_none(self.init_msg_encrypted),
                "init_funds": self.init_funds.to_amino(),
            },
        }

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
        if not self.init_msg_encrypted:
            # The encryption uses a random nonce
            # toProto() & toAmino() are called multiple times during signing
            # so to keep the msg consistant across calls we encrypt the msg only once
            pass
            # self.init_msg_encrypted = await utils.encrypt(self.code_hash, self.init_msg)

        return MsgInstantiateContract_pb(
            sender=self.sender,
            code_id=self.code_id,
            label=self.label,
            init_msg=bytes(json.dumps(self.init_msg_encrypted), "utf-8"),
            init_funds=self.init_funds.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgInstantiateContract_pb) -> MsgInstantiateContract:
        return cls(
            sender=proto.sender,
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

    msg_encrypted: Optional[Union[dict, str]] = None
    code_hash: str = None
    warn_code_hash: bool = False

    def __attrs_post_init__(self):
        if self.code_hash:
            self.code_hash = self.code_hash.replace('0x', '').lower()
        else:
            self.code_hash = ''
            self.warn_code_hash = True
            # print('WARNING: MsgExecuteContract was used without the "codeHash" parameter. This is discouraged and will result in much slower execution times for your app.')

    def to_amino(self) -> dict:
        if not self.msg_encrypted:
            # The encryption uses a random nonce
            # toProto() & toAmino() are called multiple times during signing
            # so to keep the msg consistant across calls we encrypt the msg only once
            pass
            # self.msg_encrypted = await utils.encrypt(self.code_hash, self.msg)

        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "contract": self.contract,
                "msg": remove_none(self.msg_encrypted),
                "sent_funds": self.sent_funds.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        return cls(
            sender=data["sender"],
            contract=data["contract"],
            msg=parse_msg(data["msg"]),
            sent_funds=Coins.from_data(data["sent_funds"]),
        )

    def to_proto(self) -> MsgExecuteContract_pb:
        if not self.msg_encrypted:
            # The encryption uses a random nonce
            # toProto() & toAmino() are called multiple times during signing
            # so to keep the msg consistant across calls we encrypt the msg only once
            pass
            # self.msg_encrypted = await utils.encrypt(self.code_hash, self.msg)

        return MsgExecuteContract_pb(
            sender=self.sender,
            contract=self.contract,
            msg=bytes(json.dumps(self.msg_encrypted), "utf-8"),
            sent_funds=self.sent_funds.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgExecuteContract_pb) -> MsgExecuteContract:
        return cls(
            sender=proto.sender,
            contract=proto.contract,
            msg=parse_msg(proto.msg),
            sent_funds=proto.sent_funds,
        )
