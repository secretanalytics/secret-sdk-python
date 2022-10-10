from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id, test_net_chain_id
from secret_sdk.util.address_converter import address_to_bytes
import json
import base64
import requests
import copy

secret = LocalSecret(chain_id=test_net_chain_id)


wallet = secret.wallets['test1']
wallet_end = secret.wallets['test2']
chain_id = test_net_chain_id
acc_addr = wallet.key.acc_address
mnemonic_key = wallet.key

from secret_sdk.protobuf.secret.compute.v1beta1 import MsgExecuteContract
from secret_sdk.protobuf.cosmos.bank.v1beta1 import MsgSend
from secret_sdk.protobuf.cosmos.tx.v1beta1 import Tx, TxBody, AuthInfo, SignDoc, SignerInfo, ModeInfo, ModeInfoSingle, BroadcastTxRequest, BroadcastMode
from secret_sdk.protobuf.cosmos.tx.signing.v1beta1 import SignMode
from secret_sdk.protobuf.cosmos.tx.v1beta1 import Fee

from secret_sdk.protobuf.cosmos.base.v1beta1 import Coin
sscrt_addr_testnet = 'secret18vd8fpwxzck93qlwghaj6arh4p7c5n8978vsyg'
handle_msg = {'deposit': {}}
contract_code_hash = '9587D60B8E6B078ACE12014CEEEE089530B9FABCD76535D93666A6C127AD8813'
sent_funds = Coin('uscrt', '100')


# msg send
msg_send = MsgSend(wallet.key.acc_address, wallet_end.key.acc_address, sent_funds)
# encrypt msg
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
def create_tx(msg):
    tx_body = TxBody([msg])
    fee = Fee(Coin('uscrt', '1000000'), 250000, "", "")
    auth_info = AuthInfo([], fee)
    tx = Tx(tx_body, auth_info)
    return tx

tx = create_tx(msg)
# helps to have the object interface, becasue here we need to do this bytes stuff which is painful
def sign_tx(tx):
    account_number = wallet.account_number()
    sequence = wallet.sequence()
    si_backup = copy.deepcopy(tx.auth_info.signer_infos)
    tx.auth_info.signer_infos = [
        SignerInfo(
            public_key=wallet.key.public_key,
            sequence=sequence,
            mode_info=ModeInfo(
                single=ModeInfoSingle(mode=SignMode.SIGN_MODE_DIRECT)
            ),
        )
    ]

    signDoc = SignDoc(
                chain_id=test_net_chain_id,
                account_number=account_number,
                auth_info_bytes=bytes(tx.auth_info),
                body_bytes=bytes(tx.body),
            )
    signDoc_payload = bytes(signDoc)
    signed_signDoc = wallet.key.sign(signDoc_payload)
    tx.signatures.append(signed_signDoc)
    tx.auth_info.signer_infos.append(
                SignerInfo(
                    public_key=wallet.key.public_key,
                    sequence=sequence,
                    mode_info=ModeInfo(single=ModeInfoSingle(mode=SignMode.SIGN_MODE_DIRECT)),
                )
            )

broadcast_req = BroadcastTxRequest(tx_bytes=bytes(tx), mode=BroadcastMode.BROADCAST_MODE_BLOCK)


# tx_res = requests.post(f"{secret.url}/cosmos/tx/v1beta1/txs", data=broadcast_req.to_dict())
