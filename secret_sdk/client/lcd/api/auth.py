from typing import Optional, Union, List

from ..params import APIParams
from secret_sdk.core import AccAddress
from secret_sdk.core.auth import (
    Account,
    BaseAccount,
    ContinuousVestingAccount,
    DelayedVestingAccount,
    ModuleAccount,
    Params
)

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncAuthAPI", "AuthAPI"]


class AsyncAuthAPI(BaseAsyncAPI):
    async def account_info(
        self, address: AccAddress, params: Optional[APIParams] = None
    ) -> Union[
        BaseAccount,
        ContinuousVestingAccount,
        DelayedVestingAccount,
        ModuleAccount
    ]:
        """Fetches the account information.

        Args:
            address (AccAddress): account address
            params (APIParams): optional parameters

        Returns:
            Union[BaseAccount, ContinuousVestingAccount, DelayedVestingAccount, ModuleAccount]: account information
        """
        result = await self._c._get(f"/cosmos/auth/v1beta1/accounts/{address}", params)
        return Account.from_data(result["account"])

    async def accounts(
        self, params: Optional[APIParams] = None
    ) -> Union[
        BaseAccount,
        ContinuousVestingAccount,
        DelayedVestingAccount,
        ModuleAccount
    ]:
        """Fetches all accounts

        Args:
            params (APIParams): optional parameters

        Returns:
            List[Union[BaseAccount, ContinuousVestingAccount, DelayedVestingAccount, ModuleAccount]]: accounts information, pagination
        """
        result = await self._c._get(f"/cosmos/auth/v1beta1/accounts", params)
        return [Account.from_data(account) for account in result['accounts']], result['pagination']

    async def params(self):
        result = await self._c._get(f'/cosmos/auth/v1beta1/params')
        return Params.from_data(result['params'])


class AuthAPI(AsyncAuthAPI):
    @sync_bind(AsyncAuthAPI.account_info)
    def account_info(
        self, address: AccAddress, params: Optional[APIParams] = None
    ) -> Union[
        BaseAccount,
        ContinuousVestingAccount,
        DelayedVestingAccount,
        ModuleAccount
    ]:
        pass

    account_info.__doc__ = AsyncAuthAPI.account_info.__doc__

    @sync_bind(AsyncAuthAPI.accounts)
    def accounts(
            self, params: Optional[APIParams] = None
    ) -> List[Union[
        BaseAccount,
        ContinuousVestingAccount,
        DelayedVestingAccount,
        ModuleAccount
    ]]:
        pass

    accounts.__doc__ = AsyncAuthAPI.accounts.__doc__

    @sync_bind(AsyncAuthAPI.params)
    def params(
            self
    ):
        pass

    params.__doc__ = AsyncAuthAPI.params.__doc__
