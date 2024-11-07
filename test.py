import time
from secret_sdk.protobuf.cosmos.tx.v1beta1 import BroadcastMode
from secret_sdk.core import Coins
from secret_sdk.client.lcd import LCDClient
from secret_sdk.key.mnemonic import MnemonicKey

secret = LCDClient(chain_id="secretdev-1", url='http://localhost:1317')
wallet = secret.wallet(MnemonicKey('grant rice replace explain federal release fix clever romance raise often wild taxi quarter soccer fiber love must tape steak together observe swap guitar'))
tx = wallet.send_tokens(recipient_addr='secret1ap26qrlp8mcq2pg6r47w43l0y8zkqm8a450s03', transfer_amount=Coins({'uscrt': 10**6}), broadcast_mode=BroadcastMode.BROADCAST_MODE_ASYNC)
print("tx:", tx)
while True:
    try:
        tx = wallet.lcd.tx.tx_info(tx.txhash)
        break
    except Exception as e:
        time.sleep(1)
        continue
print(tx)
print(tx.events)