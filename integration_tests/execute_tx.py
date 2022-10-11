from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id, test_net_chain_id
from secret_sdk.core.coins import Coins

secret = LocalSecret(chain_id=test_net_chain_id)

w = secret.wallets['test1']
sscrt_addr_testnet = 'secret18vd8fpwxzck93qlwghaj6arh4p7c5n8978vsyg'
sent_funds = Coins('100uscrt')
handle_msg = {'deposit': {}}
t = w.execute_tx(sscrt_addr_testnet, [handle_msg], transfer_amount=sent_funds)

assert t.code == 0
