from abc import ABC, abstractmethod

from secret_sdk.core.public_key import PublicKey
from secret_sdk.util.json import JSONSerializable

from .base_account import BaseAccount
from .continuous_vesting_account import ContinuousVestingAccount
from .delayed_vesting_account import DelayedVestingAccount
from .module_account import ModuleAccount


class Account(JSONSerializable, ABC):
    @abstractmethod
    def get_account_number(self) -> int:
        pass

    @abstractmethod
    def get_sequence(self) -> int:
        pass

    @abstractmethod
    def get_public_key(self) -> PublicKey:
        pass

    @classmethod
    def from_amino(cls, amino: dict):  # -> Account:
        if amino["type"] == BaseAccount.type_amino:
            return BaseAccount.from_amino(amino)
        elif amino["type"] == ContinuousVestingAccount.type_amino:
            return ContinuousVestingAccount.from_amino(amino)
        elif amino["type"] == DelayedVestingAccount.type_amino:
            return DelayedVestingAccount.from_amino(amino)
        elif amino["type"] == ModuleAccount.type_amino:
            return ModuleAccount.from_amino(amino)

    @classmethod
    def from_data(cls, data: dict):  # -> Account:
        if data["@type"] == BaseAccount.type_url:
            return BaseAccount.from_data(data)
        elif data["@type"] == ContinuousVestingAccount.type_url:
            return ContinuousVestingAccount.from_data(data)
        elif data["@type"] == DelayedVestingAccount.type_url:
            return DelayedVestingAccount.from_data(data)
        elif data["@type"] == ModuleAccount.type_url:
            return ModuleAccount.from_data(data)

    @classmethod
    def from_proto(cls, data: dict):  # -> Account:
        if data["@type"] == BaseAccount.type_url:
            return BaseAccount.from_proto(data)
        elif data["@type"] == ContinuousVestingAccount.type_url:
            return ContinuousVestingAccount.from_proto(data)
        elif data["@type"] == DelayedVestingAccount.type_url:
            return DelayedVestingAccount.from_proto(data)
        elif data["@type"] == ModuleAccount.type_url:
            return ModuleAccount.from_proto(data)
