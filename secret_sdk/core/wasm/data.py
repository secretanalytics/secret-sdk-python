from __future__ import annotations

import json
from typing import Union

import attr
from secret_sdk.protobuf.secret.compute.v1beta1 import AbsoluteTxPosition as AbsoluteTxPosition_pb
from secret_sdk.protobuf.secret.compute.v1beta1 import AccessType
from secret_sdk.protobuf.secret.compute.v1beta1 import AccessTypeParam as AccessTypeParam_pb

from secret_sdk.util.json import JSONSerializable

__all__ = ["AccessType", "AccessTypeParam"]


def parse_msg(msg: Union[dict, str, bytes]) -> dict:
    if type(msg) is dict:
        return msg
    return json.loads(msg)


def convert_access_type_from_json(access_type: str) -> AccessType:
    if access_type == "Everybody":
        return AccessType.ACCESS_TYPE_EVERYBODY
    elif access_type == "Nobody":
        return AccessType.ACCESS_TYPE_NOBODY
    elif access_type == "OnlyAddress":
        return AccessType.ACCESS_TYPE_ONLY_ADDRESS
    elif access_type == "Unspecified":
        return AccessType.ACCESS_TYPE_UNSPECIFIED


def convert_access_type_to_json(access_type: AccessType) -> str:
    if access_type == AccessType.ACCESS_TYPE_EVERYBODY:
        return AccessType.ACCESS_TYPE_EVERYBODY.name
    elif access_type == AccessType.ACCESS_TYPE_NOBODY:
        return AccessType.ACCESS_TYPE_NOBODY.name
    elif access_type == AccessType.ACCESS_TYPE_ONLY_ADDRESS:
        return AccessType.ACCESS_TYPE_ONLY_ADDRESS.name
    elif access_type == AccessType.ACCESS_TYPE_UNSPECIFIED:
        return AccessType.ACCESS_TYPE_UNSPECIFIED.name


@attr.s
class AccessTypeParam(JSONSerializable):
    value: AccessType = attr.ib()
    """"""

    def to_amino(self) -> dict:
        return {
            "value": convert_access_type_to_json(self.value),
        }

    def to_proto(self) -> AccessTypeParam_pb:
        return AccessTypeParam_pb(
            value=self.value,
        )

    @classmethod
    def from_data(cls, data: dict) -> AccessTypeParam:
        return cls(
            value=convert_access_type_from_json(data["value"]),
        )

    @classmethod
    def from_proto(cls, proto: AccessTypeParam_pb) -> AccessTypeParam:
        return cls(value=proto.value)


@attr.s
class AbsoluteTxPosition(JSONSerializable):
    block_height: int = attr.ib()
    tx_index: int = attr.ib()
    """"""

    def to_amino(self):
        return {"block_height": self.block_height, "tx_index": self.tx_index}

    def to_proto(self) -> AbsoluteTxPosition_pb:
        return AbsoluteTxPosition_pb(
            block_height=self.block_height, tx_index=self.tx_index
        )

    @classmethod
    def from_data(cls, data: dict) -> AbsoluteTxPosition:
        return cls(block_height=data["block_height"], tx_index=data["tx_index"])

    @classmethod
    def from_proto(cls, proto: AbsoluteTxPosition_pb) -> AbsoluteTxPosition:
        return cls(block_height=proto.block_height, tx_index=proto.tx_index)

