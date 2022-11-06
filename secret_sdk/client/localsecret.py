from typing import Dict

from secret_sdk.key.mnemonic import MnemonicKey

from .lcd import AsyncLCDClient, AsyncWallet, LCDClient, Wallet

__all__ = ["LOCAL_DEFAULTS", "LOCAL_MNEMONICS", "LocalSecret", "AsyncLocalSecret"]

test_net_chain_id = "pulsar-2"
main_net_chain_id = "secret-4"

test_net_api = "http://testnet.securesecrets.org:1317"
main_net_api = "https://secret-4.api.trivium.network:1317"

LOCAL_MNEMONICS = {
    "holodeck-2": {
        "test1": {
            "name": "test1",
            "mnemonic": "hero innocent acquire shoulder captain plug clutch gloom increase use narrow impact woman warm cushion proud cereal sail theory expire funny wife panda tragic",
        },
        "test2": {
            "name": "test2",
            "mnemonic": "base bunker skin catalog assault field arctic often west problem bracket water diagram wing crunch series resource symptom call team sketch south ignore find",
        },
        "test3": {
            "name": "test3",
            "mnemonic": "wrist oak pool pond foot decrease excite theme work fresh punch film",
        },
    },
    "pulsar-2": {
        "test1": {
            "name": "test1",
            "type": "local",
            "address": "secret1snf0y77qz9hgh69fefffjdv5tedfd6rmewzzsz",
            "pubkey": "secretpub1addwnpepq06rnqyhjayqzr4r5jcgeawfe3mv84wk3c0dkmnghwe72fsmanyeckun6qw",
            "mnemonic": "arrest rain grunt tuna super test scan limit motion indicate weather script duty praise federal demand suffer grape learn arctic evil maple pumpkin pink",
        },
        "test2": {
            "name": "test2",
            "type": "local",
            "address": "secret1n654ua463c3fddlnu6jjverlas6k68f3659dqe",
            "pubkey": "secretpub1addwnpepqvgssw4qsq56hjz3z7c5drsjdpz6pp9tjyghanze4tcqanh5e92v6a4nk2f",
            "mnemonic": "tragic latin square great skate forget sentence gift blossom boss rate fragile belt mercy prepare rug biology exercise tiny canvas carry need hurry pepper",
        },
        "test3": {
            "name": "test3",
            "type": "local",
            "address": "secret1jp3pkxtnhp7h9fx2sl5nuhdx48ny240r8eeadq",
            "pubkey": "secretpub1addwnpepq2lkmnaelryvqznk8emrhqyxe3hznwnrgy4a24vkv0s9klzw44jzgh67n8f",
            "mnemonic": "possible chaos write danger tilt lobster valid thing enter science divide govern square lawsuit budget avoid cancel above dial pony eight display item armor",
        },
    },
    main_net_chain_id: {},
}

LOCAL_DEFAULTS = {
    test_net_chain_id: {
        "url": test_net_api,
        "chain_id": test_net_chain_id,
        "gas_prices": {"uscrt": 0.25},
        "gas_adjustment": 1.0,
    },
    main_net_chain_id: {
        "url": main_net_api,
        "chain_id": main_net_chain_id,
        "gas_prices": {"uscrt": 0.25},
        "gas_adjustment": 1.0,
    },
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
                MnemonicKey(mnemonic=LOCAL_MNEMONICS[chain_id][wallet_name]["mnemonic"])
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
                MnemonicKey(mnemonic=LOCAL_MNEMONICS[chain_id][wallet_name]["mnemonic"])
            )
            for wallet_name in LOCAL_MNEMONICS[chain_id]
        }
