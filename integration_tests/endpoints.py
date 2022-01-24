from secret_sdk.client.lcd import LCDClient
from integration_tests.config import api_url

secret = LCDClient(
    chain_id="secret-4",
    url=api_url,
)

binance_account = 'secret1p3ucd3ptpw902fluyjzhq3ffgq4ntdda6qy5vv'
validator_address = 'secretvaloper18762353s6ulgla3efvf0hpe5rjjxp5ndfvl8z7'
delegator_address = 'secret18762353s6ulgla3efvf0hpe5rjjxp5ndct360h'

print('Auth')
res = secret.auth.account_info(binance_account)
print(res)
print('---------------------------')

print('Bank')
res = secret.bank.balance(binance_account)
print(res)
print('---------------------------')

print('Distribution')
res = secret.distribution.rewards(delegator_address)
print(res)

res = secret.distribution.validator_rewards(validator_address)
print(res)

res = secret.distribution.withdraw_address(delegator_address)
print(res)

res = secret.distribution.community_pool()
print(res)

res = secret.distribution.parameters()
print(res)
print('---------------------------')

print('Staking')
res = secret.staking.delegations(validator=validator_address)
print(res)
res = secret.staking.delegations(delegator=delegator_address)
print(res)

res = secret.staking.delegation(delegator=delegator_address, validator=validator_address)
print(res)

res = secret.staking.unbonding_delegations(validator=validator_address)
print(res)
res = secret.staking.unbonding_delegations(delegator=delegator_address)
print(res)

res = secret.staking.redelegations()
print(res)
res = secret.staking.redelegations(delegator=delegator_address)
print(res)
res = secret.staking.redelegations(validator_src=validator_address)
print(res)
res = secret.staking.redelegations(validator_dst=validator_address)
print(res)

res = secret.staking.bonded_validators(delegator=delegator_address)
print(res)

res = secret.staking.validators()
print(res)

res = secret.staking.validator(validator=validator_address)
print(res)

res = secret.staking.pool()
print(res)

res = secret.staking.parameters()
print(res)
print('---------------------------')

print('Tendermint')
res = secret.tendermint.node_info()
print(res)

res = secret.tendermint.syncing()
print(res)

res = secret.tendermint.syncing()
print(res)

res = secret.tendermint.block_info()
print(res)

last_block = int(secret.tendermint.block_info()['block']['header']['height'])

res = secret.tendermint.block_info(last_block-10)
print(res)


res = secret.tendermint.validator_set()
print(res)

res = secret.tendermint.validator_set(last_block-10)
print(res)
print('---------------------------')

print('Tx')
for tx_hash in [
    'E9557807CE4CE6E387059523D6ED716B0F59BFE0B5E4DD998B8BB026747C320C',
    '259DA3D4807CA31A8C2FFBD3F0D6DAFF6B5F1F914F10C3E52456B10D06BF3A96',
    '1DB6541E7047B0BAB52287FA5967D87BF188E36E66B15517CA89283180BB6797',
    '7CE39254CF20AE08D220D8B0D0627E9ABB5B688FFEFC6838B1E96B1182C442F8',
    '9195E398AB2B0BEEE9499594AC14431D898386ADFEFDF12BEC0E5114C360641B',
    '51E777E2A57CD61D15FEA1A63991E9A0E3D6613CA3A6BDDEEC4AC2C48B9B6844',
    'BE769AFDC968532903A3598816EFEC839E984F91DFAA99007F24B106B31F7146',
    '01E86971C548E05AB3B2239FB506C4818BC11EC769186E02BC67A068C91FFD98',
    '79F65CD9205327BD3F49951D53E5D9AF492D7FFB8A5EFABB662DDA7B4DC99559'
]:
    try:
       res = secret.tx.tx_info(tx_hash)
       print(res)
    except Exception as e:
       print(e)

    try:
        res = secret.tx.tx_by_id(tx_hash)
        print(res)
    except Exception as e:
        print(e)

# res = secret.tx.estimate_fee(
#         sender=delegator_address,
#         msgs=[],
#         memo=''
# )
# print(res)
# encode(tx: StdTx, options: BroadcastOptions = None)
# hash(tx: StdTx)
# _broadcast(tx: StdTx, mode: str, options: BroadcastOptions = None)
# broadcast_sync(tx: StdTx, options: BroadcastOptions = None)
# broadcast_async(tx: StdTx, options: BroadcastOptions = None)
# broadcast(tx: StdTx, options: BroadcastOptions = None)

secret.tx.search(options={'tx.height': 1781786})
print('---------------------------')

print('Wasm')
res = secret.wasm.code_info(code_id=5)
print(res)

res = secret.wasm.contract_info(contract_address='secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek')
print(res)

res = secret.wasm.contract_hash_by_code_id(code_id=5)
print(res)

res = secret.wasm.contract_hash('secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek')
print(res)

res = secret.wasm.contract_query(contract_address='secret1rgky3ns9ua09rt059049yl0zqf3xjqxne7ezhp', query={'pool': {}})
print(res)
res = secret.wasm.contract_query(contract_address='secret1rgky3ns9ua09rt059049yl0zqf3xjqxne7ezhp', query={"pool": {}}, height=last_block-10)
print(res)
# contract_execute_msg(sender_address: AccAddress, contract_address: AccAddress, handle_msg: dict, transfer_amount: Optional[Coins] = None)

res = secret.wasm.list_code_info()
print(res)

res = secret.wasm.list_contracts_by_code_id(code_id=5)
print(res)

print('---------------------------')