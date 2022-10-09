import base64
import json
import secrets
from typing import Any, Dict, List, Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from miscreant.aes.siv import SIV


from grpclib.client import Channel

from .protobuf.secret.registration.v1beta1 import QueryStub as registrationQueryStub
from dataclasses import dataclass
import betterproto


@dataclass(eq=False, repr=False)
class EmptyRequest(betterproto.Message):
    pass


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

mainnet_consensus_io_pubkey = bytes(
    [
        0x08,
        0x3B,
        0x1A,
        0x03,
        0x66,
        0x12,
        0x11,
        0xD5,
        0xA4,
        0xCC,
        0x8D,
        0x39,
        0xA7,
        0x77,
        0x95,
        0x79,
        0x58,
        0x62,
        0xF7,
        0x73,
        0x06,
        0x45,
        0x57,
        0x3B,
        0x2B,
        0xCC,
        0x2C,
        0x19,
        0x20,
        0xC5,
        0x3C,
        0x04,
    ]
)

mainnet_chain_ids = {"secret-2", "secret-3", "secret-4"}


class EncryptionUtils:
    def __init__(
        self, channel: Channel, seed: str = None, chain_id: str = None
    ) -> None:
        self.registrationQuerier = registrationQueryStub(channel)

        if not seed:
            self.seed = EncryptionUtils.generate_new_seed()
        else:
            self.seed = seed

        self.privkey, self.pubkey = EncryptionUtils.generate_new_key_pair_from_seed(
            self.seed
        )

        if chain_id and chain_id in mainnet_chain_ids:
            # comments copied from secretjs impl
            # Major speedup
            # TODO: not sure if this is the best approach for detecting mainnet
            self.consensus_io_pubkey = mainnet_consensus_io_pubkey

    def generate_new_key_pair() -> Tuple[List[int], List[int]]:
        """Returns: (privkey, pubkey)"""
        return EncryptionUtils.generate_new_key_pair_from_seed(
            EncryptionUtils.generate_new_seed()
        )

    def generate_new_seed() -> List[int]:
        return [secrets.randbits(8) for _ in range(32)]

    def generate_key_pair(seed):
        privkey = X25519PrivateKey.generate()
        pubkey = privkey.public_key()
        return privkey, pubkey

    def generate_new_key_pair_from_seed(seed: List[int]) -> Tuple[List[int], List[int]]:
        privkey, pubkey = EncryptionUtils.generate_key_pair(seed)
        return (privkey, pubkey)

    async def get_consensus_io_pubkey(self) -> List[int]:
        tx_key = await self.registrationQuerier.tx_key(EmptyRequest())
        consensus_io_pubkey = EncryptionUtils.extract_pubkey(tx_key.key)
        return consensus_io_pubkey

    # async def get_consensus_io_pubkey(self):
    #     io_exch_pubkey = await self.registrationQuerier.tx_key()
    #     io_exch_pubkey = io_exch_pubkey.key
    #     consensus_io_pubkey = base64.b64decode(io_exch_pubkey)
    #     return bytes([x for x in consensus_io_pubkey])

    async def get_tx_encryption_key(self, nonce: List[int]) -> List[int]:
        self.consensus_io_pubkey = await self.get_consensus_io_pubkey()

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
        nonce = EncryptionUtils.generate_new_seed()
        tx_encryption_key = await self.get_tx_encryption_key(nonce)

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

        tx_encryption_key = await self.get_tx_encryption_key(nonce)
        siv = SIV(tx_encryption_key)
        plaintext = siv.open(ciphertext, [bytes()])
        return plaintext

    async def get_pub_key(self):
        return self.pubkey.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
        )

    ## following functions are ported from secret.js

    def extract_pubkey(cert: List[int]) -> List[int]:
        nsCmtOid = [
            0x06,
            0x09,
            0x60,
            0x86,
            0x48,
            0x01,
            0x86,
            0xF8,
            0x42,
            0x01,
            0x0D,
        ]
        payload = EncryptionUtils.extract_asn1_value(cert, nsCmtOid)
        try:
            # Try SW mode
            pubkey = base64.b64decode(payload.decode())

            if len(pubkey) == 32:
                return pubkey

        except:
            # Not SW mode
            pass

        try:
            # try HW mode
            quoteHex = base64.b64decode(
                json.loads(
                    base64.b64decode(json.loads(payload.decode())["report"]).decode()
                )["isvEnclaveQuoteBody"]
            )
            reportData = quoteHex[368:400]
            return reportData
        except:
            raise ValueError(
                "Cannot extract tx io pubkey: error parsing certificate - malformed certificate",
            )

    def extract_asn1_value(cert: List[int], oid: List[int]) -> List[int]:
        offset = (cert.hex()).index(bytes(oid).hex()) / 2

        def check_and_convert_to_int(num: float):
            q, r = divmod(num, 1)
            if not r:
                return int(q)
            return num  # returns float if can't be converted evenly

        offset = check_and_convert_to_int(offset)
        if not isinstance(offset, int):
            raise ValueError("Error parsing certificate - malformed certificate")

        offset += 12

        if offset + 2 >= len(cert):
            raise ValueError("Error parsing certificate - malformed certificate")

        length = cert[offset]
        if length > 0x80:
            length = cert[offset + 1] * 0x100 + cert[offset + 2]
            offset += 2

        if offset + length + 1 >= len(cert):
            raise ValueError("Error parsing certificate - malformed certificate")

        offset += 1
        payload = cert[offset : offset + length]

        return payload
