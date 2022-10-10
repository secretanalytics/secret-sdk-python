from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id, test_net_chain_id
from secret_sdk.util.address_converter import address_to_bytes
import json
import base64
import requests
import copy
from secret_sdk.protobuf.cosmos.crypto.ed25519 import PubKey
from betterproto.lib.google.protobuf import Any as Any_pb
from secret_sdk.client.lcd import LCDClient
from secret_sdk.key.mnemonic import MnemonicKey

from secret_sdk.protobuf.secret.compute.v1beta1 import MsgExecuteContract
from secret_sdk.protobuf.cosmos.bank.v1beta1 import MsgSend
from secret_sdk.protobuf.cosmos.tx.v1beta1 import Tx, TxBody, AuthInfo, SignDoc, SignerInfo, ModeInfo, ModeInfoSingle, BroadcastTxRequest, BroadcastMode
from secret_sdk.protobuf.cosmos.tx.signing.v1beta1 import SignMode
from secret_sdk.protobuf.cosmos.tx.v1beta1 import Fee
from secret_sdk.protobuf.cosmos.base.v1beta1 import Coin


# light_clinet_address = "https://pisco-lcd.terra.dev"
# chain_id = "pisco-1"
# terra = LCDClient(
#     url=light_clinet_address,
#     chain_id=chain_id,
# )
# key = MnemonicKey(
#     mnemonic="notice oak worry limit wrap speak medal online prefer cluster roof addict wrist behave treat actual wasp year salad speed social layer crew genius"
# )
# test1 = terra.wallet(key=key)
#
# msg_send = MsgSend(
#     "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v",
#     "terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp",
#     [Coin('uluna','20000')],
# )
secret = LocalSecret(chain_id=test_net_chain_id)
# secret = LCDClient(url='http://23.108.55.7:1317', chain_id = 'secret-4')
# wallet = secret.wallet(MnemonicKey(luigi))
wallet = secret.wallets['test1']
wallet_end = secret.wallets['test2']
chain_id = test_net_chain_id
acc_addr = wallet.key.acc_address
mnemonic_key = wallet.key

# msg send
msg_send = MsgSend(wallet.key.acc_address, wallet_end.key.acc_address, amount = [Coin('uscrt', '100')])


# encrypt msg
sscrt_addr_testnet = 'secret18vd8fpwxzck93qlwghaj6arh4p7c5n8978vsyg'
sent_funds = [Coin('uscrt', '100')]
handle_msg = {'deposit': {}}
contract_code_hash = '9587D60B8E6B078ACE12014CEEEE089530B9FABCD76535D93666A6C127AD8813'
msg_str = json.dumps(handle_msg, separators=(",", ":"))
encrypted_msg = secret.encrypt_utils.encrypt(contract_code_hash, msg_str)
encrypted_msg = base64.b64encode(bytes(encrypted_msg))

msg = MsgExecuteContract(
        sender = address_to_bytes(acc_addr),
        contract = address_to_bytes(sscrt_addr_testnet),
        msg = encrypted_msg,
        sent_funds = sent_funds
        )

# create tx
def create_tx(msg, type_url):
    wrap_msg = Any_pb(type_url=type_url, value=bytes(msg))
    tx_body = TxBody([wrap_msg], memo='', timeout_height=0)
    # fee = Fee([Coin('uluna', '9480')], 63199, "", "")
    fee = Fee([Coin('uscrt', '94800')], gas_limit=163199, payer="", granter="")
    auth_info = AuthInfo([], fee)
    tx = Tx(tx_body, auth_info, signatures=[])
    return tx

def sign_tx(tx):
    account_number = wallet.account_number()
    # account_number = 159
    sequence = wallet.sequence()
    # sequence = 116
    si_backup = copy.deepcopy(tx.auth_info.signer_infos)
    # public_key = Any_pb(type_url='/cosmos.crypto.secp256k1.PubKey', value=bytes(PubKey(test1.key.public_key)))
    public_key = Any_pb(type_url='/cosmos.crypto.secp256k1.PubKey', value=bytes(PubKey(wallet.key.public_key)))
    mode_info = ModeInfo(
        single=ModeInfoSingle(mode=SignMode.SIGN_MODE_DIRECT)
    )
    tx.auth_info.signer_infos = [
        SignerInfo(
            public_key=public_key,
            sequence=sequence,
            mode_info=mode_info
        )
    ]

    signDoc = SignDoc(
                chain_id=chain_id,
                # chain_id="pisco-1",
            account_number=account_number,
                auth_info_bytes=bytes(tx.auth_info),
                body_bytes=bytes(tx.body),
            )
    signDoc_payload = bytes(signDoc)
    signed_signDoc = wallet.key.sign(signDoc_payload)
    # signed_signDoc = test1.key.sign(signDoc_payload)

    # tx.auth_info.signer_infos = si_backup
    tx.signatures.append(signed_signDoc)
    # tx.auth_info.signer_infos.append(
    #             SignerInfo(
    #                 public_key=public_key,
    #                 sequence=sequence,
    #                 mode_info=mode_info,
    #             )
    #         )


send_tx = create_tx(msg_send, type_url='/cosmos.bank.v1beta1.MsgSend')
sign_tx(send_tx)
send_tx_bytes = base64.b64encode(bytes(send_tx)).decode()
send_tx_res = requests.post(f"{secret.url}/cosmos/tx/v1beta1/txs", json= {'tx_bytes':send_tx_bytes, "mode":'BROADCAST_MODE_BLOCK'})

sscrt_tx = create_tx(msg, type_url='/secret.compute.v1beta1.MsgExecuteContract')
sign_tx(sscrt_tx)
sscrt_tx_bytes = base64.b64encode(bytes(sscrt_tx)).decode()
sscrt_tx_res = requests.post(f"{secret.url}/cosmos/tx/v1beta1/txs", json= {'tx_bytes':sscrt_tx_bytes, "mode":'BROADCAST_MODE_BLOCK'})
