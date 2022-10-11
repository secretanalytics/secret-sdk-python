from typing import Optional

from secret_sdk.core import AccAddress, Coins

from ..params import APIParams
from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncBankAPI", "BankAPI"]


class AsyncBankAPI(BaseAsyncAPI):
    async def balance(
        self, address: AccAddress, params: Optional[APIParams] = None, block_height: Optional[int] = 0
    ) -> (Coins, dict):
        """Fetches an account's current balance.

        Args:
            address (AccAddress): account address
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            Coins: balance
            Pagination: pagination info
        """
        res = await self._c._get(f"/cosmos/bank/v1beta1/balances/{address}", params, block_height=block_height)
        return Coins.from_data(res["balances"]), res.get("pagination")

    async def total(self, params: Optional[APIParams] = None, block_height: Optional[int] = 0) -> (Coins, dict):
        """Fetches the current total supply of all tokens.

        Returns:
            Coins: total supply
            params (APIParams, optional): additional params for the API like pagination
        """
        res = await self._c._get("/cosmos/bank/v1beta1/supply", params, block_height=block_height)
        return Coins.from_data(res.get("supply")), res.get("pagination")

    async def spendable_balances(
        self, address: AccAddress, params: Optional[APIParams] = None,
            block_height: Optional[int] = 0
    ) -> (Coins, dict):
        """Queries the spenable balance of all coins for a single account

        Returns:
            Coins: spendable balance
            params (APIParams, optional): additional params for the API like pagination
        """
        res = await self._c._get(
            f"/cosmos/bank/v1beta1/spendable_balances/{address}", params, block_height=block_height
        )
        return Coins.from_data(res.get("balances")), res.get("pagination")


class BankAPI(AsyncBankAPI):
    @sync_bind(AsyncBankAPI.balance)
    def balance(
        self, address: AccAddress, params: Optional[APIParams] = None, block_height: Optional[int] = 0
    ) -> (Coins, dict):
        pass

    balance.__doc__ = AsyncBankAPI.balance.__doc__

    @sync_bind(AsyncBankAPI.total)
    def total(self, params: Optional[APIParams] = None, block_height: Optional[int] = 0) -> (Coins, dict):
        pass

    @sync_bind(AsyncBankAPI.spendable_balances)
    def spendable_balances(self, params: Optional[APIParams] = None, block_height: Optional[int] = 0) -> (Coins, dict):
        pass

    balance.__doc__ = AsyncBankAPI.balance.__doc__
    total.__doc__ = AsyncBankAPI.total.__doc__
    spendable_balances.__doc__ = AsyncBankAPI.spendable_balances.__doc__
