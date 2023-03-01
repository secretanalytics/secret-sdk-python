import base64
import json
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

    async def consensus_io_pub_key(self):
        """Returns the consensus_io_pub_key"""
        result = await self._c._get(f"/registration/v1beta1/tx-key")
        # return extract_consensus_io_pub_key(base64.b64decode(result['key']))
        return base64.b64decode(result['key'])


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

    @sync_bind(AsyncRegistrationAPI.consensus_io_pub_key)
    def consensus_io_pub_key(self):
        pass

    consensus_io_pub_key.__doc__ = AsyncRegistrationAPI.consensus_io_pub_key.__doc__



def extract_as_n1_value(cert: bytes, oid: bytes) -> bytes:
    # bytes: immutable, bytearray: mutable
    offset = cert.index(oid)
    if not isinstance(offset, (int,)):
        raise ValueError("Error parsing certificate - malformed certificate")
    offset += 12
    # we will be accessing offset + 2, so make sure it's not out-of-bounds
    if offset + 2 >= len(cert):
        raise ValueError("Error parsing certificate - malformed certificate")
    length = cert[offset]
    if length > 0x80: # 0x: hex literal, 80 = 8*16 + 0*1
        length = cert[offset + 1] * 0x100 + cert[offset + 2]
        offset+=2
    if offset + length + 1 >= len(cert):
        raise ValueError("Error parsing certificate - malformed certificate")
    # // Obtain Netscape Comment
    offset += 1
    payload = cert[offset:offset + length]
    return payload


def extract_consensus_io_pub_key(cert: bytes) -> bytes:
    ns_cmt_oid = bytes([ 0x06, 0x09, 0x60, 0x86, 0x48, 0x01, 0x86, 0xf8, 0x42, 0x01, 0x0d,])
    payload = extract_as_n1_value(cert, ns_cmt_oid)
    try:
        pubkey = base64.b64decode(payload.decode('utf-8'))
        if len(pubkey) == 32:
            return pubkey
    except:
        # not SW node
        pass
    try:
        #quote_hex = base64.b64encode()
        report = json.loads(payload.decode('utf-8'))['report']
        quoteHex = base64.b64decode(json.loads(base64.b64decode(report).decode('utf-8'))['isvEnclaveQuoteBody'])
        return quoteHex[368:400]
    except:
        raise ValueError("Cannot extract tx io pubkey: error parsing certificate - malformed certificate")
