"Wasm module messages."

from __future__ import annotations

import copy

import attr
from typing import Dict, Any

from secret_sdk.core import AccAddress, Coins
from secret_sdk.core.msg import Msg
from secret_sdk.util.json import dict_to_data
from secret_sdk.util.remove_none import remove_none

__all__ = [
    "MsgStoreCode",
    "MsgMigrateCode",
    "MsgInstantiateContract",
    "MsgExecuteContract",
    "MsgMigrateContract",
    "MsgUpdateContractAdmin",
    "MsgClearContractAdmin",
]


@attr.s
class MsgStoreCode(Msg):
    """Upload a new smart contract WASM binary to the blockchain.

    Args:
        sender: address of sender
        wasm_byte_code: base64-encoded string containing bytecode
    """

    type = "wasm/MsgStoreCode"
    """"""

    sender: AccAddress = attr.ib()
    wasm_byte_code: str = attr.ib(converter=str)
    source: str = attr.ib(converter=str)
    builder: str = attr.ib(converter=str)

    @classmethod
    def from_data(cls, data: dict) -> MsgStoreCode:
        data = data["value"]
        return cls(
            sender=data["sender"],
            wasm_byte_code=data["wasm_byte_code"],
            source=data.get("source"),
            builder=data.get("builder"),
        )


@attr.s
class MsgMigrateCode(Msg):
    """Upload a new smart contract WASM binary to the blockchain, replacing an existing code ID.
    Can only be called once by creator of the contract, and is used for migrating from Col-4 to Col-5.

    Args:
        sender: address of sender
        code_id: reference to the code on the blockchain
        wasm_byte_code: base64-encoded string containing bytecode
    """

    type = "wasm/MsgMigrateCode"
    """"""

    sender: AccAddress = attr.ib()
    code_id: int = attr.ib(converter=int)
    wasm_byte_code: str = attr.ib(converter=str)

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["sender"] = str(d["sender"])
        d["code_id"] = str(d["code_id"])
        d["wasm_byte_code"] = str(d["wasm_byte_code"])
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: dict) -> MsgMigrateCode:
        data = data["value"]
        return cls(
            sender=data["sender"],
            code_id=data["code_id"],
            wasm_byte_code=data["wasm_byte_code"],
        )


@attr.s
class MsgInstantiateContract(Msg):
    """Creates a new instance of a smart contract from existing code on the blockchain.

    Args:
        sender: address of sender
        admin: address of contract admin
        code_id (int): code ID to use for instantiation
        label (str): human-readable label for this contract
        init_msg (dict): InitMsg to initialize contract
        init_funds (Coins): initial amount of coins to be sent to contract
    """

    type = "wasm/MsgInstantiateContract"
    """"""

    sender: AccAddress = attr.ib()
    admin: AccAddress = attr.ib()
    code_id: int = attr.ib(converter=int)
    label: str = attr.ib(converter=str)
    init_msg: dict = attr.ib()
    init_funds: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d["code_id"] = str(d["code_id"])
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> MsgInstantiateContract:
        data = data["value"]
        return cls(
            sender=data["sender"],
            admin=data["admin"],
            code_id=data["code_id"],
            label=data.get("label"),
            init_msg=remove_none(data["init_msg"]),
            init_funds=Coins.from_data(data["init_funds"]),
        )


@attr.s
class MsgExecuteContract(Msg):
    """Execute a state-mutating function on a smart contract.

    Args:
        sender: address of sender
        contract: address of contract to execute function on
        execute_msg: ExecuteMsg (aka. HandleMsg) to pass
        coins: coins to be sent, if needed by contract to execute.
            Defaults to empty ``Coins()``
    """

    type = "wasm/MsgExecuteContract"
    """"""

    sender: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    msg: str = attr.ib()
    sent_funds: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        data = data["value"]
        return cls(
            sender=data["sender"],
            contract=data["contract"],
            msg=data["msg"],
            sent_funds=Coins.from_data(data["sent_funds"]),
        )


@attr.s
class MsgMigrateContract(Msg):
    """Migrate the contract to a different code ID.

    Args:
        admin: address of contract admin
        contract: address of contract to migrate
        new_code_id (int): new code ID to migrate to
        migrate_msg (dict): MigrateMsg to execute
    """

    type = "wasm/MsgMigrateContract"
    """"""

    admin: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    new_code_id: int = attr.ib(converter=int)
    migrate_msg: dict = attr.ib()

    def to_data(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        return {"type": self.type, "value": dict_to_data(d)}

    @classmethod
    def from_data(cls, data: dict) -> MsgMigrateContract:
        data = data["value"]
        return cls(
            admin=data["admin"],
            contract=data["contract"],
            new_code_id=data["new_code_id"],
            migrate_msg=data["migrate_msg"],
        )


@attr.s
class MsgUpdateContractAdmin(Msg):
    """Update a smart contract's admin.

    Args:
        owner: address of current admin (sender)
        new_owner: address of new admin
        contract: address of contract to change
    """

    type = "wasm/MsgUpdateContractAdmin"
    """"""

    admin: AccAddress = attr.ib()
    new_admin: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgUpdateContractAdmin:
        data = data["value"]
        return cls(
            admin=data["admin"],
            new_admin=data["new_admin"],
            contract=data["contract"],
        )


@attr.s
class MsgClearContractAdmin(Msg):
    """Clears the contract's admin field.

    Args:
        admin: address of current admin (sender)
        contract: address of contract to change
    """

    type = "wasm/MsgClearContractAdmin"
    """"""

    admin: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgClearContractAdmin:
        data = data["value"]
        return cls(
            admin=data["admin"],
            contract=data["contract"],
        )
