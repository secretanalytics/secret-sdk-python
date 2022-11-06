import abc
import copy
from typing import Optional
import attr

from bech32 import bech32_encode, convertbits

from secret_sdk.core import (
    AccAddress,
    AccPubKey,
    ModeInfo,
    ModeInfoSingle,
    SignatureV2,
    SignDoc,
    ValAddress,
    ValPubKey,
)
from secret_sdk.core.public_key import (
    PublicKey,
    address_from_public_key,
    amino_pubkey_from_public_key as pubkey_from_public_key,
)

from secret_sdk.core.tx import AuthInfo, SignerInfo, SignMode, Tx
from secret_sdk.core.signature_v2 import Descriptor
from secret_sdk.core.signature_v2 import Single as SingleDescriptor


__all__ = ["Key"]


def get_bech(prefix: str, payload: str) -> str:
    data = convertbits(bytes.fromhex(payload), 8, 5)
    if data is None:
        raise ValueError(f"could not parse data: prefix {prefix}, payload {payload}")
    return bech32_encode(prefix, data)  # base64 -> base32



@attr.s
class SignOptions:
    account_number: int = attr.ib(converter=int)
    sequence: int = attr.ib(converter=int)
    chain_id: str = attr.ib()


class Key:
    """Abstract Key interface, representing an agent with transaction-signing capabilities.

    Args:
        public_key (Optional[bytes]): compressed public key bytes,
    """

    public_key: Optional[bytes]
    """Compressed public key bytes, used to derive :data:`raw_address` and :data:`raw_pubkey`."""

    raw_address: Optional[bytes]
    """Raw Bech32 words of address, used to derive associated account and validator
    operator addresses.
    """

    raw_pubkey: Optional[bytes]
    """Raw Bech32 words of pubkey, used to derive associated account and validator
    pubkeys.
    """

    def __init__(self, public_key: Optional[PublicKey] = None):
        self.public_key = public_key
        if public_key:
            self.raw_address = address_from_public_key(public_key)
            self.raw_pubkey = pubkey_from_public_key(public_key)

    @abc.abstractmethod
    def sign(self, payload: bytes) -> bytes:
        """Signs the data payload. An implementation of Key is expected to override this method.

        Args:
            payload (bytes): arbitrary data payload

        Raises:
            NotImplementedError: if not implemented

        Returns:
            bytes: signed payload
        """
        raise NotImplementedError("an instance of Key must implement Key.sign")

    @property
    def acc_address(self) -> AccAddress:
        """Secret Bech32 account address. Default derivation via :data:`public_key` is provided.

        Raises:
            ValueError: if Key was not initialized with proper public key

        Returns:
            AccAddress: account address
        """
        if not self.raw_address:
            raise ValueError("could not compute acc_address: missing raw_address")
        return AccAddress(get_bech("secret", self.raw_address.hex()))

    @property
    def val_address(self) -> ValAddress:
        """Secret Bech32 validator operator address. Default derivation via :data:`public_key` is provided.

        Raises:
            ValueError: if Key was not initialized with proper public key

        Returns:
            ValAddress: validator operator address
        """
        if not self.raw_address:
            raise ValueError("could not compute val_address: missing raw_address")
        return ValAddress(get_bech("secretvaloper", self.raw_address.hex()))

    @property
    def acc_pubkey(self) -> AccPubKey:
        """Secret Bech32 account pubkey. Default derivation via :data:`public_key` is provided.

        Raises:
            ValueError: if Key was not initialized with proper public key

        Returns:
            AccPubKey: account pubkey
        """
        if not self.raw_pubkey:
            raise ValueError("could not compute acc_pubkey: missing raw_pubkey")
        return AccPubKey(get_bech("secretpub", self.raw_pubkey.hex()))

    @property
    def val_pubkey(self) -> ValPubKey:
        """Secret Bech32 validator pubkey. Default derivation via ``public_key`` is provided.

        Raises:
            ValueError: if Key was not initialized with proper public key

        Returns:
            ValPubKey: validator pubkey
        """
        if not self.raw_pubkey:
            raise ValueError("could not compute val_pubkey: missing raw_pubkey")
        return ValPubKey(get_bech("secretvaloperpub", self.raw_pubkey.hex()))

    def create_signature(self, sign_doc: SignDoc) -> SignatureV2:
        """Signs the transaction with the signing algorithm provided by this Key implementation,
        and outputs the signature. The signature is only returned, and must be manually added to
        the ``signatures`` field of an :class:`Tx`.

        Args:
            sign_doc (SignDoc): unsigned transaction

        Raises:
            ValueError: if missing ``public_key``

        Returns:
            SignatureV2: signature object
        """
        if self.public_key is None:
            raise ValueError(
                "signature could not be created: Key instance missing public_key"
            )

        # make backup
        si_backup = copy.deepcopy(sign_doc.auth_info.signer_infos)
        sign_doc.auth_info.signer_infos = [
            SignerInfo(
                public_key=self.public_key,
                sequence=sign_doc.sequence,
                mode_info=ModeInfo(
                    single=ModeInfoSingle(mode=SignMode.SIGN_MODE_DIRECT)
                ),
            )
        ]
        signature = self.sign(sign_doc.to_bytes())

        # restore
        sign_doc.auth_info.signer_infos = si_backup

        return SignatureV2(
            public_key=self.public_key,
            data=Descriptor(
                single=SingleDescriptor(
                    mode=SignMode.SIGN_MODE_DIRECT, signature=signature
                )
            ),
            sequence=sign_doc.sequence,
        )

    def sign_tx(self, tx: Tx, options: SignOptions) -> Tx:
        """Signs the transaction with the signing algorithm provided by this Key implementation,
        and creates a ready-to-broadcast :class:`Tx` object with the signature applied.

        Args:
            tx (Tx): unsigned transaction
            options (SignOptions): options for signing

        Returns:
            Tx: ready-to-broadcast transaction object
        """
        signedTx = Tx(
            body=tx.body,
            auth_info=AuthInfo(signer_infos=[], fee=tx.auth_info.fee),
            signatures=[],
        )
        signDoc = SignDoc(
            chain_id=options.chain_id,
            account_number=options.account_number,
            sequence=options.sequence,
            auth_info=signedTx.auth_info,
            tx_body=signedTx.body,
        )

        signature: SignatureV2 = self.create_signature(signDoc)

        sigData: SingleDescriptor = signature.data.single
        for sig in tx.signatures:
            signedTx.signatures.append(sig)
        signedTx.signatures.append(sigData.signature)
        for infos in tx.auth_info.signer_infos:
            signedTx.auth_info.signer_infos.append(infos)
        signedTx.auth_info.signer_infos.append(
            SignerInfo(
                public_key=signature.public_key,
                sequence=signature.sequence,
                mode_info=ModeInfo(single=ModeInfoSingle(mode=sigData.mode)),
            )
        )
        return signedTx
