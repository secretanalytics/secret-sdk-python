from secret_sdk.core import AccAddress
from secret_sdk.core.auth import Account

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncAuthAPI", "AuthAPI"]


class AsyncAuthAPI(BaseAsyncAPI):
    async def account_info(self, address: AccAddress) -> Account:
        """Fetches the account information.

        Args:
            address (AccAddress): account address

        Returns:
            Account: account information
        """
        result = await self._c._get(f"/auth/accounts/{address}")
        if result["type"] == "cosmos-sdk/BaseAccount":
            return Account.from_data(result)
        else:
            raise


class AuthAPI(AsyncAuthAPI):
    @sync_bind(AsyncAuthAPI.account_info)
    def account_info(self, address: AccAddress) -> Account:
        pass

    account_info.__doc__ = AsyncAuthAPI.account_info.__doc__
