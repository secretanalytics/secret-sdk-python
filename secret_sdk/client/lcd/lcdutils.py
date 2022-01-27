import base64
import secrets
from functools import reduce
from typing import Any, Dict, List

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from miscreant.aes.siv import SIV

from .api._base import BaseAsyncAPI, sync_bind

hkdf_salt = bytes(
    [
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,
        0x4B,
        0xEA,
        0xD8,
        0xDF,
        0x69,
        0x99,
        0x08,
        0x52,
        0xC2,
        0x02,
        0xDB,
        0x0E,
        0x00,
        0x97,
        0xC1,
        0xA1,
        0x2E,
        0xA6,
        0x37,
        0xD7,
        0xE9,
        0x6D,
    ]
)


def index_by_pub_key(m: Dict[str, Any], o: Any):
    m[o["pub_key"]["value"]] = o
    return m


class AsyncLCDUtils(BaseAsyncAPI):
    def __init__(self, c):
        super().__init__(c)
        self.seed = self.generate_new_seed()
        self.privkey, self.pubkey = self.generate_new_key_pair_from_seed(self.seed)

    async def validators_with_voting_power(self) -> Dict[str, dict]:
        """Gets current validators and merges their voting power from the validator set query.

        Returns:
            Dict[str, dict]: validators with voting power
        """
        validator_set_response = await BaseAsyncAPI._try_await(
            self._c.tendermint.validator_set()
        )
        validators = await BaseAsyncAPI._try_await(self._c.staking.validators())
        validator_set: Dict[str, Any] = reduce(
            index_by_pub_key, validator_set_response["validators"], {}
        )
        res = {}
        for v in validators:
            delegate_info = validator_set.get(v.consensus_pubkey["value"])
            if delegate_info is None:
                continue
            res[v.operator_address] = {
                "validator_info": v,
                "voting_power": int(delegate_info["voting_power"]),
                "proposer_priority": int(delegate_info["proposer_priority"]),
            }
        return res

    def generate_new_seed(self):
        return [secrets.randbits(8) for _ in range(32)]

    def generate_key_pair(self, seed):
        privkey = X25519PrivateKey.from_private_bytes(bytes(seed))
        pubkey = privkey.public_key()
        return privkey, pubkey

    def generate_new_key_pair_from_seed(self, seed):
        privkey, pubkey = self.generate_key_pair(seed)
        return privkey, pubkey

    def generate_new_key_pair(self):
        return self.generate_new_key_pair_from_seed(self.generate_new_seed())

    async def get_consensus_io_pubkey(self):
        io_exch_pubkey = await BaseAsyncAPI._try_await(self._c._get("/reg/tx-key"))
        io_exch_pubkey = io_exch_pubkey["TxKey"]
        consensus_io_pubkey = base64.b64decode(io_exch_pubkey)
        return bytes([x for x in consensus_io_pubkey])

    async def get_tx_encryption_key(self, nonce):
        if not hasattr(self, "consensus_io_pubkey"):
            self.consensus_io_pubkey = await BaseAsyncAPI._try_await(
                self.get_consensus_io_pubkey()
            )
        consensus_io_pubkey = X25519PublicKey.from_public_bytes(
            self.consensus_io_pubkey
        )
        tx_encryption_ikm = self.privkey.exchange(consensus_io_pubkey)

        master_secret = bytes([x for x in tx_encryption_ikm] + nonce)

        tx_encryption_key = HKDF(
            algorithm=hashes.SHA256(), length=32, salt=hkdf_salt, info=b"", backend=None
        ).derive(master_secret)

        return tx_encryption_key

    async def encrypt(self, contract_code_hash: str, msg: Any):
        nonce = self.generate_new_seed()
        tx_encryption_key = await BaseAsyncAPI._try_await(
            self.get_tx_encryption_key(nonce)
        )

        siv = SIV(tx_encryption_key)

        plaintext = bytes(contract_code_hash, "utf-8") + bytes(msg, "utf-8")
        ciphertext = siv.seal(plaintext, [bytes()])

        key_dump = self.pubkey.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
        )

        return nonce + [x for x in key_dump] + [x for x in ciphertext]

    async def decrypt(self, ciphertext: bytes, nonce: List[int]) -> bytes:
        if not ciphertext:
            return bytes([])

        tx_encryption_key = await BaseAsyncAPI._try_await(
            self.get_tx_encryption_key(nonce)
        )
        siv = SIV(tx_encryption_key)
        plaintext = siv.open(ciphertext, [bytes()])
        return plaintext

    async def get_pub_key(self):
        return self.pubkey.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
        )

    async def decrypt_data_field(self, data_field, nonces):
        # nonces are a list of nonce in the case of multi execute
        wasm_output_data_cipher_bz = bytes.fromhex(data_field)
        for nonce in nonces:
            decrypted_data = await self.decrypt(wasm_output_data_cipher_bz, nonce)
            decrypted = base64.b64decode(decrypted_data.decode("utf-8"))
            return decrypted


class LCDUtils(AsyncLCDUtils):
    def __init__(self, c):
        super().__init__(c)
        self.seed = self.generate_new_seed()
        self.privkey, self.pubkey = self.generate_new_key_pair_from_seed(self.seed)
        self.consensus_io_pubkey = self.get_consensus_io_pubkey()

    @sync_bind(AsyncLCDUtils.validators_with_voting_power)
    async def validators_with_voting_power(self) -> Dict[str, dict]:
        pass

    validators_with_voting_power.__doc__ = (
        AsyncLCDUtils.validators_with_voting_power.__doc__
    )

    @sync_bind(AsyncLCDUtils.get_consensus_io_pubkey)
    async def get_consensus_io_pubkey(self):
        pass

    get_consensus_io_pubkey.__doc__ = AsyncLCDUtils.get_consensus_io_pubkey.__doc__

    @sync_bind(AsyncLCDUtils.get_tx_encryption_key)
    async def get_tx_encryption_key(self, nonce):
        pass

    get_tx_encryption_key.__doc__ = AsyncLCDUtils.get_tx_encryption_key.__doc__

    @sync_bind(AsyncLCDUtils.encrypt)
    async def encrypt(self, contract_code_hash, msg):
        pass

    encrypt.__doc__ = AsyncLCDUtils.encrypt.__doc__

    @sync_bind(AsyncLCDUtils.decrypt)
    async def decrypt(self, ciphertext, nonce) -> str:
        pass

    decrypt.__doc__ = AsyncLCDUtils.decrypt.__doc__
