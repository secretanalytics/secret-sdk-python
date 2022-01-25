from typing import Dict

from secret_sdk.key.mnemonic import MnemonicKey

from .lcd import AsyncLCDClient, AsyncWallet, LCDClient, Wallet

__all__ = ["LOCAL_MNEMONICS", "LocalSecret", "AsyncLocalSecret"]

test_net_chain_id = "pulsar-2"
main_net_chain_id = "secret-4"

test_net_api = "http://testnet.securesecrets.org:1317"
main_net_api = "https://api.scrt.network"

LOCAL_MNEMONICS = {
    test_net_chain_id: {
        "test1": "hero innocent acquire shoulder captain plug clutch gloom increase use narrow impact woman warm cushion proud cereal sail theory expire funny wife panda tragic",
        "test2": "base bunker skin catalog assault field arctic often west problem bracket water diagram wing crunch series resource symptom call team sketch south ignore find",
        "test3": "wrist oak pool pond foot decrease excite theme work fresh punch film"
    },
    main_net_chain_id: {}
}

LOCAL_DEFAULTS = {
    test_net_chain_id: {
        "url": test_net_api,
        "chain_id": test_net_chain_id,
        "gas_prices": {"uscrt": 0.25},
        "gas_adjustment": 1.4,
    },
    main_net_chain_id: {
        "url": main_net_api,
        "chain_id": main_net_chain_id,
        "gas_prices": {"uscrt": 0.25},
        "gas_adjustment": 1.4,
    }
}


class AsyncLocalSecret(AsyncLCDClient):
    """An :class:`AsyncLCDClient` that comes preconfigured with the default settings for
    connecting to a LocalSecret node.
    """

    wallets: Dict[str, AsyncWallet]
    """Ready-to use :class:`AsyncWallet` objects with LocalSecret default accounts."""

    def __init__(self, *args, **kwargs):
        chain_id = kwargs.get("chain_id", test_net_chain_id)
        options = {**LOCAL_DEFAULTS[chain_id], **kwargs}
        super().__init__(*args, **options)
        self.wallets = {
            wallet_name: self.wallet(
                MnemonicKey(mnemonic=LOCAL_MNEMONICS[chain_id][wallet_name])
            )
            for wallet_name in LOCAL_MNEMONICS[chain_id]
        }


class LocalSecret(LCDClient):
    """A :class:`LCDClient` that comes preconfigured with the default settings for
    connecting to a LocalSecret node.
    """

    wallets: Dict[str, Wallet]
    """Ready-to use :class:`Wallet` objects with LocalSecret default accounts.
    """

    def __init__(self, *args, **kwargs):
        chain_id = kwargs.get("chain_id", test_net_chain_id)
        options = {**LOCAL_DEFAULTS[chain_id], **kwargs}
        super().__init__(*args, **options)
        self.wallets = {
            wallet_name: self.wallet(
                MnemonicKey(mnemonic=LOCAL_MNEMONICS[chain_id][wallet_name])
            )
            for wallet_name in LOCAL_MNEMONICS[chain_id]
        }
