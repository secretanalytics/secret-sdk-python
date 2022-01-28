from __future__ import annotations

import attr

from secret_sdk.util.base import BaseSecretData


class Msg(BaseSecretData):
    @staticmethod
    def from_data(data: dict) -> Msg:
        from secret_sdk.util.parse_msg import parse_msg

        return parse_msg(data)


@attr.s
class MsgData(Msg):
    """Data structure holding MsgData.

    Args:
        type (str): message type
        value (string): data
    """

    type: str = attr.ib(converter=str)
    value: dict = attr.ib(converter=dict)

    def to_data(self) -> dict:
        return {"type": self.type, "value": self.value}

    @classmethod
    def from_data(cls, data: dict) -> MsgData:
        return cls(type=data["type"], value=data["value"])
