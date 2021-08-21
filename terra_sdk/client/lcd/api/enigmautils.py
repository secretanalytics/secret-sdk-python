import os
import base64
import json
import requests
import secrets

from miscreant.aes.siv import SIV
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

hkdf_salt = bytes([
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x02, 0x4b, 0xea, 0xd8, 0xdf, 0x69, 0x99,
    0x08, 0x52, 0xc2, 0x02, 0xdb, 0x0e, 0x00, 0x97,
    0xc1, 0xa1, 0x2e, 0xa6, 0x37, 0xd7, 0xe9, 0x6d,
])


class EnigmaUtils():
    def __init__(self):
        self.api_url = r'https://api.secretapi.io'
        self.seed = self.generate_new_seed()
        self.privkey, self.pubkey = self.generate_new_key_pair_from_seed(self.seed)
        self.consensus_io_pubkey = self.get_consensus_io_pubkey(self.api_url)
    
    def generate_new_seed(self):
        return [secrets.randbits(8) for x in range(32)]
    
    def generate_key_pair(self, seed):
        privkey = X25519PrivateKey.generate()
        pubkey = privkey.public_key()
        return privkey, pubkey
    
    def generate_new_key_pair_from_seed(self, seed):
        privkey, pubkey = self.generate_key_pair(seed)
        return privkey, pubkey
    
    def generate_new_key_pair(self):
        return self.generate_new_key_pair_from_seed(self.generate_new_seed())
        
    def get_consensus_io_pubkey(self, api_url):
        io_exch_pubkey = requests.get(self.api_url + "/reg/consensus-io-exch-pubkey").json()['result']['ioExchPubkey']
        consensus_io_pubkey = base64.b64decode(io_exch_pubkey)
        return bytes([x for x in consensus_io_pubkey])
    
    def get_tx_encryption_key(self, nonce):
        consensus_io_pubkey = X25519PublicKey.from_public_bytes(self.consensus_io_pubkey)
        tx_encryption_ikm = self.privkey.exchange(consensus_io_pubkey)
        
        master_secret = bytes([x for x in tx_encryption_ikm] + nonce)
        
        tx_encryption_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=hkdf_salt,
            info=b'',
            backend=None
        ).derive(master_secret)
        
        return tx_encryption_key
    
    def encrypt(self, contract_code_hash, msg):
        nonce = self.generate_new_seed()
        tx_encryption_key = self.get_tx_encryption_key(nonce)
        
        siv = SIV(tx_encryption_key)
        
        plaintext = bytes(contract_code_hash, 'utf-8') + bytes(msg, 'utf-8')
        ciphertext = siv.seal(plaintext, [bytes()])

        key_dump = eu.pubkey.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

        return nonce + [x for x in key_dump] + [x for x in ciphertext]
    
    def decrypt(self, ciphertext, nonce):
        if not ciphertext:
            return bytes([])

        tx_encryption_key = self.get_tx_encryption_key(nonce)
        siv = SIV(tx_encryption_key)
        plaintext = siv.open(ciphertext, [bytes()])

        return plaintext
