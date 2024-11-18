import base64
import secrets
from typing import Any, Dict, List

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from miscreant.aes.siv import SIV

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


class EncryptionUtils():
    def __init__(self, consensus_io_pubkey: bytes, encryption_seed: bytes = None):
        if encryption_seed:
            self.seed = encryption_seed
        else:
            self.seed = self.generate_new_seed()
            
        self.privkey, self.pubkey = self.generate_new_key_pair_from_seed(self.seed)
        self.consensus_io_pubkey = consensus_io_pubkey

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


    def get_tx_encryption_key(self, nonce):
        consensus_io_pubkey = X25519PublicKey.from_public_bytes(
            self.consensus_io_pubkey
        )
        tx_encryption_ikm = self.privkey.exchange(consensus_io_pubkey)

        master_secret = bytes([x for x in tx_encryption_ikm] + nonce)

        tx_encryption_key = HKDF(
            algorithm=hashes.SHA256(), length=32, salt=hkdf_salt, info=b"", backend=None
        ).derive(master_secret)

        return tx_encryption_key

    def encrypt(self, contract_code_hash: str, msg: Any) -> List[int]:
        nonce = self.generate_new_seed()
        tx_encryption_key = self.get_tx_encryption_key(nonce)

        siv = SIV(tx_encryption_key)

        plaintext = bytes(contract_code_hash, "utf-8") + bytes(msg, "utf-8")
        ciphertext = siv.seal(plaintext, [bytes()])

        key_dump = self.pubkey.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
        )

        return nonce + [x for x in key_dump] + [x for x in ciphertext]

    def decrypt(self, ciphertext: bytes, nonce: List[int]) -> bytes:
        if not ciphertext:
            return bytes([])

        tx_encryption_key = self.get_tx_encryption_key(nonce)
        siv = SIV(tx_encryption_key)
        plaintext = siv.open(ciphertext, [bytes()])
        return plaintext

    def get_pub_key(self):
        return self.pubkey.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
        )

    def decrypt_data_field(self, data_field, nonces):
        # nonces are a list of nonce in the case of multi execute
        wasm_output_data_cipher_bz = bytes.fromhex(data_field)
        for nonce in nonces:
            decrypted_data = self.decrypt(wasm_output_data_cipher_bz, nonce)
            decrypted = base64.b64decode(decrypted_data.decode("utf-8"))
            return decrypted

