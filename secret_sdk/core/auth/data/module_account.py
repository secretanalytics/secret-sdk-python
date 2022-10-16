"""Data objects pertaining to accounts."""

from __future__ import annotations

import attr
from typing import List
from ....protobuf.cosmos.auth.v1beta1 import (
    ModuleAccount as ModuleAccount_pb,
)

from secret_sdk.core import Coins
from secret_sdk.util.json import JSONSerializable

from ...public_key import PublicKey
from .base_account import BaseAccount

__all__ = ["ModuleAccount"]


@attr.s
class ModuleAccount(JSONSerializable):
    """Stores information about an account with vesting."""

    base_account: BaseAccount = attr.ib()

    name: str = attr.ib()
    permissions: List[str] = attr.ib(default=List)

    type_amino = "cosmos-sdk/ModuleAccount"
    type_url = "/cosmos.auth.v1beta1.ModuleAccount"

    def get_sequence(self) -> int:
        return self.base_account.get_sequence()

    def get_account_number(self) -> int:
        return self.base_account.get_account_number()

    def get_public_key(self) -> PublicKey:
        return self.base_account.get_public_key()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "base_account": self.base_account.to_amino(),
                "name": self.name,
                "permissions": self.permissions,
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "base_account": self.base_account.to_data(),
            "name": self.name,
            "permissions": self.permissions,
        }

    @classmethod
    def from_amino(cls, amino: dict) -> ModuleAccount:
        amino = amino["value"] if "value" in amino else amino
        return cls(
            base_account=BaseAccount.from_amino(amino["base_account"]),
            name=amino["name"],
            permissions=amino["permissions"]
        )

    @classmethod
    def from_data(cls, data: dict) -> ModuleAccount:
        return cls(
            base_account=BaseAccount.from_data(data["base_account"]),
            name=data["name"],
            permissions=data["permissions"]
        )

    @classmethod
    def from_proto(cls, proto: ModuleAccount_pb) -> ModuleAccount:
        return cls(
            base_account=BaseAccount.from_proto(proto.base_account),
            name=proto.name,
            permissions=proto.permissions
        )

    def to_proto(self) -> ModuleAccount_pb:
        return ModuleAccount_pb(
            base_account=self.base_account.to_proto(),
            name=self.name,
            permissions=self.permissions
        )
