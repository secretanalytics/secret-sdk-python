# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: tendermint/store/types.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


@dataclass(eq=False, repr=False)
class BlockStoreState(betterproto.Message):
    base: int = betterproto.int64_field(1)
    height: int = betterproto.int64_field(2)