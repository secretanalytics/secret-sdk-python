"""Data objects pertaining to accounts."""

from __future__ import annotations

from typing import Optional

import attr

from secret_sdk.core import AccAddress
from secret_sdk.util.json import JSONSerializable

from .public_key import PublicKey

__all__ = ["Account"]


@attr.s
class Account(JSONSerializable):
    """Stores information about an account."""

    address: AccAddress = attr.ib()
    """"""

    public_key: Optional[PublicKey] = attr.ib()
    """"""

    account_number: int = attr.ib(converter=int)
    """"""

    sequence: int = attr.ib(converter=int)
    """"""

    def to_data(self) -> dict:
        return {
            "type": "cosmos-sdk/BaseAccount",
            "value": {
                "address": self.address,
                "public_key": self.public_key and self.public_key.to_data(),
                "account_number": str(self.account_number),
                "sequence": str(self.sequence),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> Account:
        data = data["value"]
        return cls(
            address=data["address"],
            public_key=data.get("public_key")
            and PublicKey.from_data(data["public_key"]),
            account_number=data.get("account_number") or 0,
            sequence=data.get("sequence") or 0,
        )
