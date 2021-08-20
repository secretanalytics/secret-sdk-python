from typing import Dict

from terra_sdk.key.mnemonic import MnemonicKey

from .lcd import AsyncLCDClient, AsyncWallet, LCDClient, Wallet

__all__ = ["LOCALTERRA_MNEMONICS", "LocalTerra", "AsyncLocalTerra"]

LOCALTERRA_MNEMONICS = {
    "test1": "hero innocent acquire shoulder captain plug clutch gloom increase use narrow impact woman warm cushion proud cereal sail theory expire funny wife panda tragic",
    "test2": "base bunker skin catalog assault field arctic often west problem bracket water diagram wing crunch series resource symptom call team sketch south ignore find"
}

test_net_chain_id = "holodeck-2"
main_net_chain_id = "secret-2"

test_net_api = "https://bootstrap.secrettestnet.io"
main_net_api = "https://api.secretapi.io"

LOCALTERRA_DEFAULTS = {
    "url": test_net_api,
    "chain_id": test_net_chain_id,
    "gas_prices": {"uscrt": 0.25},
    "gas_adjustment": 1.4,
}


class AsyncLocalTerra(AsyncLCDClient):
    """An :class:`AsyncLCDClient` that comes preconfigured with the default settings for
    connecting to a LocalTerra node.
    """

    wallets: Dict[str, AsyncWallet]
    """Ready-to use :class:`Wallet` objects with LocalTerra default accounts."""

    def __init__(self, *args, **kwargs):
        options = {**LOCALTERRA_DEFAULTS, **kwargs}
        super().__init__(*args, **options)
        self.wallets = {
            wallet_name: self.wallet(
                MnemonicKey(mnemonic=LOCALTERRA_MNEMONICS[wallet_name])
            )
            for wallet_name in LOCALTERRA_MNEMONICS
        }


class LocalTerra(LCDClient):
    """A :class:`LCDClient` that comes preconfigured with the default settings for
    connecting to a LocalTerra node.
    """

    wallets: Dict[str, Wallet]
    """Ready-to use :class:`Wallet` objects with LocalTerra default accounts.

    >>> terra = LocalTerra()
    >>> terra.wallets['test1'].key.acc_address
    'terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v'
    """

    def __init__(self, *args, **kwargs):
        options = {**LOCALTERRA_DEFAULTS, **kwargs}
        super().__init__(*args, **options)
        self.wallets = {
            wallet_name: self.wallet(
                MnemonicKey(mnemonic=LOCALTERRA_MNEMONICS[wallet_name])
            )
            for wallet_name in LOCALTERRA_MNEMONICS
        }
