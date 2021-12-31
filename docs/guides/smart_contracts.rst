.. smart_contracts:

Working with Smart Contracts
============================

Contract Deployment Example
---------------------------

.. code-block:: python

    import base64
    from secret_sdk.client.localterra import LocalTerra
    from secret_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract    
    from secret_sdk.core.auth.data.tx import StdFee
    
    terra = LocalTerra()
    test1 = terra.wallets["test1"]
    contract_file = open("./contract.wasm", "rb")
    file_bytes = base64.b64encode(contract_file.read()).decode()
    store_code = MsgStoreCode(test1.key.acc_address, file_bytes)
    store_code_tx = test1.create_and_sign_tx(msgs=[store_code], fee=StdFee(2100000, "60000uscrt"))
    store_code_tx_result = terra.tx.broadcast(store_code_tx)
    print(store_code_tx_result)

    code_id = store_code_tx_result.logs[0].events_by_type["store_code"]["code_id"][0]
    instantiate = MsgInstantiateContract(
        test1.key.acc_address,
        code_id,
        {"count": 0},
        {"uscrt": 10000000, "ukrw": 1000000},
        False,
    )
    instantiate_tx = test1.create_and_sign_tx(msgs=[instantiate])
    instantiate_tx_result = terra.tx.broadcast(instantiate_tx)
    print(instantiate_tx_result)

    contract_address = instantiate_tx_result.logs[0].events_by_type[
        "instantiate_contract"
    ]["contract_address"][0]

    execute = MsgExecuteContract(
        test1.key.acc_address,
        contract_address,
        {"increment": {}},
        {"uscrt": 100000},
    )

    execute_tx = test1.create_and_sign_tx(
        msgs=[execute], fee=StdFee(1000000, Coins(uscrt=1000000))
    )

    execute_tx_result = terra.tx.broadcast(execute_tx)
    print(execute_tx_result)

    result = terra.wasm.contract_query(contract_address, {"get_count": {}})
    print(result)
    
