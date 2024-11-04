# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: cosmos/tx/config/v1/config.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


@dataclass
class Config(betterproto.Message):
    """Config is the config object of the x/auth/tx package."""

    # skip_ante_handler defines whether the ante handler registration should be
    # skipped in case an app wants to override this functionality.
    skip_ante_handler: bool = betterproto.bool_field(1)
    # skip_post_handler defines whether the post handler registration should be
    # skipped in case an app wants to override this functionality.
    skip_post_handler: bool = betterproto.bool_field(2)
