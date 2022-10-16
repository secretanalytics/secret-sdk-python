"""Data objects pertaining to params."""

from __future__ import annotations

import attr
from ....protobuf.cosmos.auth.v1beta1 import Params as Params_pb

from ....util.json import JSONSerializable

__all__ = ["Params"]


@attr.s
class Params(JSONSerializable):
    """Stores information about auth params."""

    type_amino = "cosmos-sdk/Params"
    type_url = "/cosmos.auth.v1beta1.Params"

    max_memo_characters: int = attr.ib(converter=int)
    tx_sig_limit: int = attr.ib(converter=int)
    tx_size_cost_per_byte: int = attr.ib(converter=int)
    sig_verify_cost_ed25519: int = attr.ib(converter=int)
    sig_verify_cost_secp256_k1: int = attr.ib(converter=int)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "max_memo_characters": self.max_memo_characters,
                "tx_sig_limit": self.tx_sig_limit,
                "tx_size_cost_per_byte": self.tx_size_cost_per_byte,
                "sig_verify_cost_ed25519": self.sig_verify_cost_ed25519,
                "sig_verify_cost_secp256_k1": self.sig_verify_cost_secp256_k1
            },
        }

    @classmethod
    def from_amino(cls, amino: dict) -> Params:
        amino = amino["value"] if "value" in amino else amino
        return cls(
            max_memo_characters=amino["max_memo_characters"],
            tx_sig_limit=amino["tx_sig_limit"],
            tx_size_cost_per_byte=amino["tx_size_cost_per_byte"],
            sig_verify_cost_ed25519=amino["sig_verify_cost_ed25519"],
            sig_verify_cost_secp256_k1=amino["sig_verify_cost_secp256k1"]
        )

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "max_memo_characters": self.max_memo_characters,
            "tx_sig_limit": self.tx_sig_limit,
            "tx_size_cost_per_byte": self.tx_size_cost_per_byte,
            "sig_verify_cost_ed25519": self.sig_verify_cost_ed25519,
            "sig_verify_cost_secp256_k1": self.sig_verify_cost_secp256_k1
        }

    @classmethod
    def from_data(cls, data: dict) -> Params:
        return cls(
            max_memo_characters=data["max_memo_characters"],
            tx_sig_limit=data["tx_sig_limit"],
            tx_size_cost_per_byte=data["tx_size_cost_per_byte"],
            sig_verify_cost_ed25519=data["sig_verify_cost_ed25519"],
            sig_verify_cost_secp256_k1=data["sig_verify_cost_secp256k1"]
        )

    @classmethod
    def from_proto(cls, proto: Params_pb) -> Params:
        return cls(
            max_memo_characters=proto.max_memo_characters,
            tx_sig_limit=proto.tx_sig_limit,
            tx_size_cost_per_byte=proto.tx_size_cost_per_byte,
            sig_verify_cost_ed25519=proto.sig_verify_cost_ed25519,
            sig_verify_cost_secp256_k1=proto.sig_verify_cost_secp256_k1
        )

    def to_proto(self) -> Params_pb:
        return Params_pb(
            max_memo_characters=self.max_memo_characters,
            tx_sig_limit=self.tx_sig_limit,
            tx_size_cost_per_byte=self.tx_size_cost_per_byte,
            sig_verify_cost_ed25519=self.sig_verify_cost_ed25519,
            sig_verify_cost_secp256_k1=self.sig_verify_cost_secp256_k1
        )
