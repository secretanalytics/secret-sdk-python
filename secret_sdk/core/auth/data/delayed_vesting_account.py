"""Data objects pertaining to accounts."""

from __future__ import annotations


import attr
from ....protobuf.cosmos.vesting.v1beta1 import (
    DelayedVestingAccount as DelayedVestingAccount_pb,
)

from ...public_key import PublicKey
from .base_vesting_account import BaseVestingAccount

__all__ = ["DelayedVestingAccount"]


@attr.s
class DelayedVestingAccount:
    """Stores information about an account with delayed vesting."""

    base_vesting_account: BaseVestingAccount = attr.ib()

    type_amino = "cosmos-sdk/DelayedVestingAccount"
    type_url = "/cosmos.vesting.v1beta1.DelayedVestingAccount"

    def get_sequence(self) -> int:
        return self.base_vesting_account.get_sequence()

    def get_account_number(self) -> int:
        return self.base_vesting_account.get_account_number()

    def get_public_key(self) -> PublicKey:
        return self.base_vesting_account.get_public_key()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "base_vesting_account": self.base_vesting_account.to_amino(),
            },
        }

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "base_vesting_account": self.base_vesting_account.to_data(),
        }

    def to_proto(self) -> DelayedVestingAccount_pb:
        return DelayedVestingAccount_pb(
            base_vesting_account=self.base_vesting_account.to_proto(),
        )

    @classmethod
    def from_amino(cls, amino: dict) -> DelayedVestingAccount:
        amino = amino["value"]
        return cls(
            base_vesting_account=BaseVestingAccount.from_amino(
                {
                    "type": BaseVestingAccount.type_amino,
                    "value": amino["base_vesting_account"],
                }
            )
        )

    @classmethod
    def from_data(cls, data: dict) -> DelayedVestingAccount:
        return cls(
            base_vesting_account=BaseVestingAccount.from_data(
                data["base_vesting_account"]
            )
        )

    @classmethod
    def from_proto(cls, proto: DelayedVestingAccount_pb) -> DelayedVestingAccount:
        return cls(
            base_vesting_account=BaseVestingAccount.from_proto(
                proto.base_vesting_account
            )
        )
