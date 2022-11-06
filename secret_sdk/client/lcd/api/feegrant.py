from typing import Optional

from secret_sdk.core import AccAddress
from secret_sdk.core.feegrant import Allowance

from ..params import APIParams
from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncFeeGrantAPI", "FeeGrantAPI"]


class AsyncFeeGrantAPI(BaseAsyncAPI):
    async def allowances(
        self, address: AccAddress, params: Optional[APIParams] = None
    ) -> (Allowance, dict):
        """fetch fee allowances

        Args:
            address (AccAddress): grantee address
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            Allowances[]: granted allowances
            pagination[]: pagination info
        """
        res = await self._c._get(
            f"cosmos/feegrant/v1beta1/allowances/{address}", params
        )
        allowances = []
        for i in res["allowances"]:
            allowance = {
                "granter": i.get("granter"),
                "grantee": i.get("grantee"),
                "allowance": Allowance.from_data(i.get("allowance")),
            }
            allowances.append(allowance)
        return allowances, res.get("pagination")

    async def allowance(
        self,
        granter: AccAddress,
        grantee: AccAddress,
        params: Optional[APIParams] = None,
    ) -> Allowance:
        """fetch granter's allowance for the grantee

        Args:
            granter (AccAddress): granter is the address of the user granting an allowance of their funds.
            grantee (AccAddress): grantee is the address of the user being granted an allowance of another user’s funds.
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            Allowance: granted allowance
        """
        res = await self._c._get(
            f"cosmos/feegrant/v1beta1/allowance/{granter}/{grantee}", params
        )
        res = res.get("allowance")
        return {
            "granter": res.get("granter"),
            "grantee": res.get("grantee"),
            "allowance": Allowance.from_data(res.get("allowance")),
        }

    async def allowances_by_granter(
        self,
        granter: AccAddress,
        params: Optional[APIParams] = None,
    ) -> Allowance:
        """all the grants given by an granter

        Args:
            granter (AccAddress): granter is the address of the user granting an allowance of their funds.
            params (APIParams, optional): additional params for the API like pagination

        Returns:
            Allowance: granted allowance
        """
        res = await self._c._get(
            f"cosmos/feegrant/v1beta1/issued/{granter}", params
        )
        res = res.get("allowance")
        return {
            "granter": res.get("granter"),
            "allowance": Allowance.from_data(res.get("allowance")),
        }

class FeeGrantAPI(AsyncFeeGrantAPI):
    @sync_bind(AsyncFeeGrantAPI.allowances)
    def allowances(
        self, address: AccAddress, params: Optional[APIParams] = None
    ) -> (Allowance, dict):
        pass

    allowances.__doc__ = AsyncFeeGrantAPI.allowances.__doc__

    @sync_bind(AsyncFeeGrantAPI.allowance)
    def allowance(self, granter: AccAddress, grantee: AccAddress, params: Optional[APIParams] = None) -> Allowance:
        pass

    allowance.__doc__ = AsyncFeeGrantAPI.allowance.__doc__

    @sync_bind(AsyncFeeGrantAPI.allowance)
    def allowances_by_granter(self, granter: AccAddress, params: Optional[APIParams] = None) -> Allowance:
        pass

    allowances_by_granter.__doc__ = AsyncFeeGrantAPI.allowances_by_granter.__doc__
