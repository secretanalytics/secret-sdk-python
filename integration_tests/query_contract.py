from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id, test_net_chain_id
from secret_sdk.core.coins import Coins

secret = LocalSecret(chain_id=main_net_chain_id)
contract = 'secret1rgky3ns9ua09rt059049yl0zqf3xjqxne7ezhp'
hash = '0dfd06c7c3c482c14d36ba9826b83d164003f2b0bb302f222db72361e0927490'
query = {"pool":{}}
height = 5589677
a = secret.wasm.contract_query(contract, query)
b = secret.wasm.contract_query(contract, query, height=height)
assert a['assets'][0]['amount'] != b['assets'][0]['amount']