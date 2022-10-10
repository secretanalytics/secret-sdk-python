from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncRegistrationAPI", "RegistrationAPI"]


class AsyncRegistrationAPI(BaseAsyncAPI):
    async def tx_key(self) -> str:
        """Returns the key used for transactions"""
        result = await self._c._get(f"/registration/v1beta1/tx-key")
        return result['key']

    async def registration_key(self):
        """Returns the key used for registration"""
        result = await self._c._get(f"/registration/v1beta1/registration-key")
        return result

    async def encrypted_seed(self, pub_key: str):
        """Returns the encrypted seed for a registered node by public key"""
        result = await self._c._get(f"/registration/v1beta1/encrypted-seed/{pub_key}")
        return result


class RegistrationAPI(AsyncRegistrationAPI):
    @sync_bind(AsyncRegistrationAPI.tx_key)
    def tx_key(self) -> str:
        pass

    tx_key.__doc__ = AsyncRegistrationAPI.tx_key.__doc__

    @sync_bind(AsyncRegistrationAPI.registration_key)
    def registration_key(self):
        pass

    registration_key.__doc__ = AsyncRegistrationAPI.registration_key.__doc__

    @sync_bind(AsyncRegistrationAPI.encrypted_seed)
    def encrypted_seed(self, pub_key: str):
        pass

    encrypted_seed.__doc__ = AsyncRegistrationAPI.encrypted_seed.__doc__
