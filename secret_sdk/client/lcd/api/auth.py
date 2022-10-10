from typing import Optional, Union

from ..params import APIParams
from secret_sdk.core import AccAddress
from secret_sdk.core.auth import (
    Account,
    BaseAccount,
    ContinuousVestingAccount,
    DelayedVestingAccount,
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
    ]:
        """Fetches the account information.

        Args:
            address (AccAddress): account address
            params (APIParams): optional parameters

        Returns:
            Union[BaseAccount, ContinuousVestingAccount, DelayedVestingAccount, PeriodicVestingAccount]: account information
        """
        result = await self._c._get(f"/cosmos/auth/v1beta1/accounts/{address}", params)
        return Account.from_data(result["account"])


class AuthAPI(AsyncAuthAPI):
    @sync_bind(AsyncAuthAPI.account_info)
    def account_info(
        self, address: AccAddress, params: Optional[APIParams] = None
    ) -> Union[
        BaseAccount,
        ContinuousVestingAccount,
        DelayedVestingAccount,
    ]:
        pass

    account_info.__doc__ = AsyncAuthAPI.account_info.__doc__
