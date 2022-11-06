import datetime
import pytest
from secret_sdk.key.mnemonic import MnemonicKey
from secret_sdk.core import Coins, TxResultCode
from secret_sdk.client.lcd.api.gov import ProposalStatus
from secret_sdk.core.wasm.msgs import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract
from secret_sdk.util.tx import get_value_from_raw_log
from secret_sdk.protobuf.cosmos.tx.v1beta1 import BroadcastMode

@pytest.fixture
def mnemonics():
    # Initialize genesis accounts
    return [
        "grant rice replace explain federal release fix clever romance raise often wild taxi quarter soccer fiber love must tape steak together observe swap guitar",
        "jelly shadow frog dirt dragon use armed praise universe win jungle close inmate rain oil canvas beauty pioneer chef soccer icon dizzy thunder meadow",
        "chair love bleak wonder skirt permit say assist aunt credit roast size obtain minute throw sand usual age smart exact enough room shadow charge",
        "word twist toast cloth movie predict advance crumble escape whale sail such angry muffin balcony keen move employ cook valve hurt glimpse breeze brick",
    ]


def test_setup_accounts(mnemonics):
    secret = pytest.secret
    accounts = []

    for mnemonic in mnemonics:
        wallet = secret.wallet(MnemonicKey(mnemonic))
        accounts.append({
          'address': wallet.key.acc_address,
          'mnemonic': mnemonic,
          'wallet': wallet,
          'secret': secret
        })

    # Generate a bunch of accounts because tx.staking tests require creating a bunch of validators
    for i in range(4, 20):
        wallet = secret.wallet(MnemonicKey())
        accounts.append({
            'address': wallet.key.acc_address,
            'mnemonic': mnemonic,
            'wallet': wallet,
            'secret': secret
        })

    # Send 100k SCRT from account 0 to each of accounts 1 - 20
    for account in accounts:
        account['balances'], _ = account['wallet'].lcd.bank.balance(account['address'])

    transfer_amount = int(100 * 1e6)
    try:
        tx = accounts[0]['wallet'].send_tokens(
            recipient_addr=accounts[1]['address'],
            transfer_amount=Coins({'uscrt': transfer_amount})
        )
        print(tx)
    except Exception as e:
        raise Exception(f'MsgSend failed: {e}')
    if tx.code != 0:
        raise Exception(f'MsgSend failed: {tx.raw_log}')

    try:
        tx = accounts[0]['wallet'].multi_send_tokens(
            recipient_addrs=[account['address'] for account in accounts[2:]],
            transfer_amounts=[Coins({'uscrt': transfer_amount}) for _ in accounts[2:]]
        )
        print(tx)
    except Exception as e:
        raise Exception(f'MsgMultiSend failed: {e}')

    if tx.code != 0:
        raise Exception(f'MsgMultiSend failed: {tx.raw_log}')

    def update_balance(accounts):
        old = {i: account['balances'].to_dict().get('uscrt', 0) for i, account in enumerate(accounts)}
        for account in accounts:
            account['balances'], _ = account['wallet'].lcd.bank.balance(account['address'])
        new = {i: account['balances'].to_dict().get('uscrt', 0) for i, account in enumerate(accounts)}
        return {i: new[i]-old[i] for i, _ in enumerate(accounts)}

    balance_changes = update_balance(accounts)
    for i in range(1, 20):
        assert balance_changes[i] == transfer_amount

    pytest.accounts = accounts


def test_accounts():
    all_accounts, pagination = pytest.secret.auth.accounts()

    # 20 accounts with a balance and 7? module accounts - ordering of tests can affect this.
    #  it 's more robust to check eq&gt rather than flat equality
    assert len(all_accounts) >= 27
    assert len([acc for acc in all_accounts if acc.type_url == '/cosmos.auth.v1beta1.ModuleAccount']) >= 7
    addrs = [pytest.accounts[0]['address'], pytest.accounts[1]['address']]
    assert len([acc for acc in all_accounts if acc.type_url == '/cosmos.auth.v1beta1.BaseAccount' and acc.address in addrs]) == 2


def test_account():
    addr = pytest.accounts[1]['address']
    account = pytest.secret.auth.account_info(address=addr)
    if not account:
        raise Exception(f'Account {addr} should exist')

    assert account.type_url == '/cosmos.auth.v1beta1.BaseAccount'
    assert account.address == addr
    assert account.account_number == 1
    assert account.sequence == 0


def test_params():
    params = pytest.secret.auth.params()
    assert params.max_memo_characters == 256
    assert params.tx_sig_limit == 7
    assert params.sig_verify_cost_ed25519 == 590
    assert params.sig_verify_cost_secp256_k1 == 1000


def test_store_code():
    wallet = pytest.accounts[0]['wallet']

    with open(r'tests/data/snip20-ibc.wasm.gz', 'rb') as fl:
        wasm_byte_code = fl.read()

    msg_store_code = MsgStoreCode(
        sender=pytest.accounts[0]['address'],
        wasm_byte_code=wasm_byte_code,
        source='',
        builder=''
    )
    tx_store = wallet.create_and_broadcast_tx(
        [msg_store_code],
        gas='3000000',
        gas_prices=Coins('0.25uscrt')
    )
    if tx_store.code != TxResultCode.Success.value:
        raise Exception(f"Failed MsgStoreCode: {tx_store.raw_log}")
    assert tx_store.code == TxResultCode.Success.value

    code_id = int(get_value_from_raw_log(tx_store.rawlog, 'message.code_id'))

    code_info = pytest.secret.wasm.code_info(code_id)
    code_hash = code_info['code_info']['code_hash']
    pytest.sscrt_code_info = code_info
    pytest.sscrt_code_hash = code_hash

    msg_init = MsgInstantiateContract(
        sender=pytest.accounts[0]['address'],
        code_id=code_id,
        code_hash=code_hash,
        init_msg={
            "name": "Secret SCRT",
            "admin": pytest.accounts[0]['address'],
            "symbol": "SSCRT",
            "decimals": 6,
            "initial_balances": [{"address": pytest.accounts[0]['address'], "amount": "1"}],
            "prng_seed": "eW8=",
            "config": {
                "public_total_supply": True,
                "enable_deposit": True,
                "enable_redeem": True,
                "enable_mint": False,
                "enable_burn": False,
            },
            "supported_denoms": ["uscrt"],
        },
        label=f"Label {datetime.datetime.now()}",
        init_funds=[],
        encryption_utils=pytest.secret.encrypt_utils
    )
    tx_init = wallet.create_and_broadcast_tx(
        [msg_init],
        gas='5000000',
        gas_prices=Coins('0.25uscrt')
    )

    if tx_init.code != TxResultCode.Success.value:
        raise Exception(f"Failed MsgInstiateContract: {tx_init.raw_log}")
    assert tx_init.code == TxResultCode.Success.value
    assert get_value_from_raw_log(tx_init.rawlog, 'message.action') == "/secret.compute.v1beta1.MsgInstantiateContract"

    contract_adress = get_value_from_raw_log(tx_init.rawlog, 'message.contract_address')
    assert contract_adress == tx_init.data[0].address
    pytest.sscrt_contract_address = contract_adress

    msg_execute = MsgExecuteContract(
        sender=pytest.accounts[0]['address'],
        contract=contract_adress,
        msg={
            'create_viewing_key': {
                'entropy': 'bla bla'
            }
        },
        code_hash=code_hash,
        encryption_utils=pytest.secret.encrypt_utils
    )
    tx_execute = wallet.create_and_broadcast_tx(
        [msg_execute],
        gas='5000000',
        gas_prices=Coins('0.25uscrt')
    )
    if tx_execute.code != TxResultCode.Success.value:
        raise Exception(f"Failed MsgExecuteContract: {tx_execute.raw_log}")
    assert tx_execute.code == TxResultCode.Success.value
    assert '{"create_viewing_key":{"key":"' in tx_execute.data[0].data.decode('utf-8')

    tx = wallet.create_and_broadcast_tx(
        [msg_execute],
        gas='5000000',
        gas_prices=Coins('0.25uscrt'),
        broadcast_mode=BroadcastMode.BROADCAST_MODE_ASYNC
    )
    tx_hash = tx.txhash
    tx_execute = pytest.secret.tx.get_tx(tx_hash)
    while tx_execute is None:
        tx_execute = pytest.secret.tx.get_tx(tx_hash)
    if tx_execute.code != TxResultCode.Success.value:
        raise Exception(f"Failed MsgExecuteContract: {tx_execute.raw_log}")
    assert tx_execute.code == TxResultCode.Success.value
    assert '{"create_viewing_key":{"key":"' in tx_execute.data[0].data.decode('utf-8')


def test_get_tx_error():
    msg_execute = MsgExecuteContract(
        sender=pytest.accounts[0]['address'],
        contract=pytest.sscrt_contract_address,
        code_hash=pytest.sscrt_code_hash,
        msg={
            'transfer': {
                'recipient': pytest.accounts[1]['address'],
                'amount': '2'
            }
        },
        encryption_utils=pytest.secret.encrypt_utils
    )
    tx_execute = pytest.accounts[0]['wallet'].create_and_broadcast_tx(
        [msg_execute],
        gas='5000000',
        gas_prices=Coins('0.25uscrt')
    )
    assert 'failed to execute message; message index: 0' in tx_execute.rawlog
    assert tx_execute.logs.log == {'generic_err': {'msg': 'insufficient funds: balance=1, required=2'}}


def test_query_compute():
    res = pytest.secret.wasm.contract_query(
        contract_address=pytest.sscrt_contract_address,
        query={'token_info': {}},
        contract_code_hash=pytest.sscrt_code_hash
    )
    assert res == {'token_info': {'name': 'Secret SCRT', 'symbol': 'SSCRT', 'decimals': 6, 'total_supply': '1'}}


def test_query_compute_without_code_hash():
    res = pytest.secret.wasm.contract_query(contract_address=pytest.sscrt_contract_address, query={'token_info': {}})
    assert res == {'token_info': {'name': 'Secret SCRT', 'symbol': 'SSCRT', 'decimals': 6, 'total_supply': '1'}}


def test_query_compute_std_error():
    res = pytest.secret.wasm.contract_query(
        contract_address=pytest.sscrt_contract_address,
        query={'balance': {'address': pytest.accounts[0]['address'], 'key': 'wrong'}}
    )
    assert res == {'viewing_key_error': {'msg': 'Wrong viewing key for this address or viewing key not set'}}


# raise LCDError and not decrypting error message
# <class 'dict'>: {'code': 3, 'message': 'encrypted: 8RyuV/YLcY9TccteFzCBB1i2YBj4r3wTfP/xa87SDpO9w++j1sUNQI6uF6jp4mX+zoNq0fl3RcILgwt+YkYgnUZmYGsyMbuF/fdsKeGJYzjUuuPORlRmI9kxfrXI47CNR1G58OXn34QBAKXUGDpiPkh4kcODlDZThclCiTKJDatVivnfS/HEt6AggaDKOMMZohvB/hCAX9MFrnqtQDEekV80+fWhbsSWgbEkXDpcLaLpwdgsJHDovDwDXg1u2MPtUHFQJrVNwmmbX0/5sopn3owEN4BobjMywlRcVAynJgusJS8ewfcNilonUHR3Ycw3fq4gvdOU6Yad6ZVhq2O4fdOTU1ukRU1XqJ9QOC1TrgbgdjI5y4AKqkRrIgXb/j5KxkyxGNeVFKEmmDw=: query contract failed: invalid request', 'details': []}
# def test_query_compute_vm_error():
#     res = pytest.secret.wasm.contract_query(
#         contract_address=pytest.sscrt_contract_address,
#         query={'non_existent_query': {}}
#     )
#     assert res == {"parse_err": {"msg": "unknown variant `non_existent_query`, expected one of `token_info`, `token_config`, `contract_status`, `exchange_rate`, `allowance`, `balance`, `transfer_history`, `transaction_history`, `minters`, `with_permit`", "target": "snip20_reference_impl::msg::QueryMsg"}}
