from typing import Dict

from secret_sdk.key.mnemonic import MnemonicKey

from .lcd import AsyncLCDClient, AsyncWallet, LCDClient, Wallet

__all__ = ["LOCALSCRT_MNEMONICS", "LocalSecret", "AsyncLocalSecret"]

LOCALSCRT_MNEMONICS = {
    "test1": "hero innocent acquire shoulder captain plug clutch gloom increase use narrow impact woman warm cushion proud cereal sail theory expire funny wife panda tragic",
    "test2": "base bunker skin catalog assault field arctic often west problem bracket water diagram wing crunch series resource symptom call team sketch south ignore find",
    "test3": "wrist oak pool pond foot decrease excite theme work fresh punch film"
}

test_net_chain_id = "holodeck-2"
main_net_chain_id = "secret-4"

test_net_api = "https://bootstrap.secrettestnet.io"
main_net_api = "https://api.secretapi.io"


LOCALSCRT_DEFAULTS = {
    "url": test_net_api,
    "chain_id": test_net_chain_id,
    "gas_prices": {"uscrt": 0.25},
    "gas_adjustment": 1.4,
}


class AsyncLocalSecret(AsyncLCDClient):
    """An :class:`AsyncLCDClient` that comes preconfigured with the default settings for
    connecting to a LocalSecret node.
    """

    wallets: Dict[str, AsyncWallet]
    """Ready-to use :class:`AsyncWallet` objects with LocalSecret default accounts."""

    def __init__(self, *args, **kwargs):
        options = {**LOCALSCRT_DEFAULTS, **kwargs}
        super().__init__(*args, **options)
        self.wallets = {
            wallet_name: self.wallet(
                MnemonicKey(mnemonic=LOCALSCRT_MNEMONICS[wallet_name])
            )
            for wallet_name in LOCALSCRT_MNEMONICS
        }


class LocalSecret(LCDClient):
    """A :class:`LCDClient` that comes preconfigured with the default settings for
    connecting to a LocalSecret node.
    """

    wallets: Dict[str, Wallet]
    """Ready-to use :class:`Wallet` objects with LocalSecret default accounts.
    """

    def __init__(self, *args, **kwargs):
        options = {**LOCALSCRT_DEFAULTS, **kwargs}
        super().__init__(*args, **options)
        self.wallets = {
            wallet_name: self.wallet(
                MnemonicKey(mnemonic=LOCALSCRT_MNEMONICS[wallet_name])
            )
            for wallet_name in LOCALSCRT_MNEMONICS
        }
