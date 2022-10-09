# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: cosmos/crypto/ed25519/keys.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


@dataclass(eq=False, repr=False)
class PubKey(betterproto.Message):
    """
    PubKey is an ed25519 public key for handling Tendermint keys in SDK. It's
    needed for Any serialization and SDK compatibility. It must not be used in
    a non Tendermint key context because it doesn't implement ADR-28.
    Nevertheless, you will like to use ed25519 in app user level then you must
    create a new proto message and follow ADR-28 for Address construction.
    """

    key: bytes = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class PrivKey(betterproto.Message):
    """
    Deprecated: PrivKey defines a ed25519 private key. NOTE: ed25519 keys must
    not be used in SDK apps except in a tendermint validator context.
    """

    key: bytes = betterproto.bytes_field(1)
