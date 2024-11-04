# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: cosmos/app/runtime/v1alpha1/module.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto


@dataclass
class Module(betterproto.Message):
    """Module is the config object for the runtime module."""

    # app_name is the name of the app.
    app_name: str = betterproto.string_field(1)
    # begin_blockers specifies the module names of begin blockers to call in the
    # order in which they should be called. If this is left empty no begin
    # blocker will be registered.
    begin_blockers: List[str] = betterproto.string_field(2)
    # end_blockers specifies the module names of the end blockers to call in the
    # order in which they should be called. If this is left empty no end blocker
    # will be registered.
    end_blockers: List[str] = betterproto.string_field(3)
    # init_genesis specifies the module names of init genesis functions to call
    # in the order in which they should be called. If this is left empty no init
    # genesis function will be registered.
    init_genesis: List[str] = betterproto.string_field(4)
    # export_genesis specifies the order in which to export module genesis data.
    # If this is left empty, the init_genesis order will be used for export
    # genesis if it is specified.
    export_genesis: List[str] = betterproto.string_field(5)
    # override_store_keys is an optional list of overrides for the module store
    # keys to be used in keeper construction.
    override_store_keys: List["StoreKeyConfig"] = betterproto.message_field(6)
    # order_migrations defines the order in which module migrations are
    # performed. If this is left empty, it uses the default migration order.
    # https://pkg.go.dev/github.com/cosmos/cosmos-
    # sdk@v0.47.0-alpha2/types/module#DefaultMigrationsOrder
    order_migrations: List[str] = betterproto.string_field(7)
    # precommiters specifies the module names of the precommiters to call in the
    # order in which they should be called. If this is left empty no precommit
    # function will be registered.
    precommiters: List[str] = betterproto.string_field(8)
    # prepare_check_staters specifies the module names of the
    # prepare_check_staters to call in the order in which they should be called.
    # If this is left empty no preparecheckstate function will be registered.
    prepare_check_staters: List[str] = betterproto.string_field(9)


@dataclass
class StoreKeyConfig(betterproto.Message):
    """
    StoreKeyConfig may be supplied to override the default module store key,
    which is the module name.
    """

    # name of the module to override the store key of
    module_name: str = betterproto.string_field(1)
    # the kv store key to use instead of the module name.
    kv_store_key: str = betterproto.string_field(2)
