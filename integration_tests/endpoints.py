from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id

secret = LocalSecret(chain_id=main_net_chain_id)

binance_account = "secret1p3ucd3ptpw902fluyjzhq3ffgq4ntdda6qy5vv"
validator_address = "secretvaloper18762353s6ulgla3efvf0hpe5rjjxp5ndfvl8z7"
delegator_address = "secret18762353s6ulgla3efvf0hpe5rjjxp5ndct360h"

print("Auth")
res = secret.auth.account_info(binance_account)
print(res)
print("---------------------------")

print("Bank")
res = secret.bank.balance(binance_account)
print(res)
print("---------------------------")

print("Distribution")
res = secret.distribution.rewards(delegator_address)
print(res)

res = secret.distribution.validator_outstanding_rewards(validator_address)
print(res)

res = secret.distribution.withdraw_address(delegator_address)
print(res)

res = secret.distribution.community_pool()
print(res)

res = secret.distribution.parameters()
print(res)
print("---------------------------")

print("Staking")
res = secret.staking.delegations(validator=validator_address)
print(res)
res = secret.staking.delegations(delegator=delegator_address)
print(res)

res = secret.staking.delegation(
    delegator=delegator_address, validator=validator_address
)
print(res)

res, pagination = secret.staking.unbonding_delegations(validator=validator_address)
print(res, pagination)
res, pagination = secret.staking.unbonding_delegations(delegator=delegator_address)
print(res, pagination)

res = secret.staking.redelegations()
print(res)
res = secret.staking.redelegations(delegator=delegator_address)
print(res)
res = secret.staking.redelegations(delegator=delegator_address, validator_src=validator_address)
print(res)
res = secret.staking.redelegations(delegator=delegator_address, validator_dst=validator_address)
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
print("---------------------------")

print("Tendermint")
res = secret.tendermint.node_info()
print(res)

res = secret.tendermint.syncing()
print(res)

res = secret.tendermint.block_info()
print(res)

last_block = int(secret.tendermint.block_info()["block"]["header"]["height"])

# res = secret.tendermint.block_info(last_block - 10)
# print(res)

res = secret.tendermint.validator_set()
print(res)

res = secret.tendermint.validator_set(last_block - 10)
print(res)
print("---------------------------")

print("Tx")
for tx_hash in [
    # withdrew rewards
    "ADB467AC82074C9C62C78160FED9D27ACAD9EAF268A6EFEFF11B317D9EA24D53",
    # IBC Transfer
    "ADB467AC82074C9C62C78160FED9D27ACAD9EAF268A6EFEFF11B317D9EA24D53",
    # Vote Yes
    "B0B1E71BEC2C936AF8AF4050A4985662D980698355ED17C1E3209562F4DA571C",
    # Execute contract
    "64CA905571B619BE6DF3560978E599A8850ADC6ADF941AD79E83CB7A22798BF8",
    # Delegate
    "2F2712E4D811F8B518E28CC36E2C2684CEF3447B63712E608F5C8FEAA5B431DE",
    # Execute contract
    "EB9AF0ED433ED638BC7048E11F7B07EF7AFE14B6672D066DB26235628BB88692",
    # Execute contract
    "A59E9E6335E7F07268B866358EB81E129D904A66BF9C5D8BA6B7494BBC0A76A2",
    # IBC Update client
    "C16E1FD7CAC31FBBDD4FCD214651946DA87610DEAE8CFC978DA8601EA71772A2",
    # Unbond
    "171E61D11615374977738E85AD6AAF5DD7CA0E55216DA9B12571B85539B08566",
    # Delegate
    "E83672197CCF91516C4E672212424A0B7BB941F4581DE86150C716DA12F99E3C",
    # Send
    "F5D2D87769EF8AB0590F0CBA173A155005ABAE9ADACE57A7E92CE122C5331392"
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

res = secret.tx.estimate_fee(
        sender=delegator_address,
        msgs=[],
        memo=''
)
print(res)


res = secret.tx.search(
    events = [
        ["tx.height", 42508],
    ])

print(res)

print("---------------------------")

print("Wasm")
res = secret.wasm.code_info(code_id=5)
print(res)

res = secret.wasm.contract_info(
    contract_address="secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek"
)
print(res)

res = secret.wasm.contract_hash_by_code_id(code_id=5)
print(res)

res = secret.wasm.contract_hash("secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek")
print(res)

res = secret.wasm.contract_query(
    contract_address="secret1rgky3ns9ua09rt059049yl0zqf3xjqxne7ezhp", query={"pool": {}}
)
print(res)

isFullNode = False
if isFullNode:
    last_block = int(secret.tendermint.block_info()["block"]["header"]["height"])
    res = secret.wasm.contract_query(
        contract_address="secret1rgky3ns9ua09rt059049yl0zqf3xjqxne7ezhp",
        query={"pool": {}},
        height=last_block - 10,
    )
    print(res)
# contract_execute_msg(sender_address: AccAddress, contract_address: AccAddress, handle_msg: dict, transfer_amount: Optional[Coins] = None)

res = secret.wasm.list_code_info()
print(res)

res = secret.wasm.list_contracts_by_code_id(code_id=5)
print(res)

print("---------------------------")
