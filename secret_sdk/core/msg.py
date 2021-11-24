from __future__ import annotations

from secret_sdk.util.base import BaseTerraData


class Msg(BaseTerraData):
    @staticmethod
    def from_data(data: dict) -> Msg:
        from secret_sdk.util.parse_msg import parse_msg

        return parse_msg(data)
