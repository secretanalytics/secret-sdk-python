from secret_sdk.core.bank import MsgMultiSend, MsgSend


def test_deserializes_msg_send(load_msg_examples):
    data = {
        "type": "cosmos-sdk/MsgSend",
        "value": {
            "from_address": "secret1y4umfuqfg76t8mfcff6zzx7elvy93jtp4xcdvw",
            "to_address": "secret1v9ku44wycfnsucez6fp085f5fsksp47u9x8jr4",
            "amount": [{"denom": "uscrt", "amount": "8102024952"}],
        },
    }

    assert MsgSend.from_data(data).to_data() == data


def test_msg_multi_send_io():

    multisend = MsgMultiSend(
        inputs=[
            {"address": "", "coins": "12000uusd,11000uscrt"},
            {"address": "", "coins": "11000ukrw,10000uscrt"},
        ],
        outputs=[
            {"address": "", "coins": "11000ukrw,10000uscrt"},
            {"address": "", "coins": "12000uusd,11000uscrt"},
        ],
    )


def test_deserializes_msg_multi_send(load_msg_examples):
    data = {
        "type": "bank/MsgMultiSend",
        "value": {
            "inputs": [
                {
                    "address": "secret1fex9f78reuwhfsnc8sun6mz8rl9zwqh03fhwf3",
                    "coins": [{"denom": "ukrw", "amount": "1"}],
                },
                {
                    "address": "secret1gg64sjt947atmh45ls45avdwd89ey4c4r72u9h",
                    "coins": [{"denom": "ukrw", "amount": "6900000000"}],
                },
                {
                    "address": "secret1yh9u2x8phrh2dan56nntgpmg7xnjrwtldhgmyu",
                    "coins": [{"denom": "ukrw", "amount": "1000000"}],
                },
                {
                    "address": "secret1c5a0njk9q6q6nheja8gp4ymt2c0qspd8ggpg49",
                    "coins": [{"denom": "ukrw", "amount": "16430000000"}],
                },
                {
                    "address": "secret1psswnm8mvy9qg5z4cxc2nvptc9dx62r4tvfrmh",
                    "coins": [{"denom": "ukrw", "amount": "9900000000"}],
                },
                {
                    "address": "secret10lgpfm8wjrl4d9datzw6r6dl83k977afzel4t5",
                    "coins": [{"denom": "ukrw", "amount": "15800000000"}],
                },
                {
                    "address": "secret13uj5qs3lcqtffqtu6aa089uf6a2pusgwndzzch",
                    "coins": [{"denom": "ukrw", "amount": "6900000000"}],
                },
            ],
            "outputs": [
                {
                    "address": "secret1fex9f78reuwhfsnc8sun6mz8rl9zwqh03fhwf3",
                    "coins": [{"denom": "ukrw", "amount": "1"}],
                },
                {
                    "address": "secret105rz2q5a4w7nv7239tl9c4px5cjy7axx3axf6p",
                    "coins": [{"denom": "ukrw", "amount": "6900000000"}],
                },
                {
                    "address": "secret1fex9f78reuwhfsnc8sun6mz8rl9zwqh03fhwf3",
                    "coins": [{"denom": "ukrw", "amount": "1000000"}],
                },
                {
                    "address": "secret105rz2q5a4w7nv7239tl9c4px5cjy7axx3axf6p",
                    "coins": [{"denom": "ukrw", "amount": "16430000000"}],
                },
                {
                    "address": "secret105rz2q5a4w7nv7239tl9c4px5cjy7axx3axf6p",
                    "coins": [{"denom": "ukrw", "amount": "9900000000"}],
                },
                {
                    "address": "secret105rz2q5a4w7nv7239tl9c4px5cjy7axx3axf6p",
                    "coins": [{"denom": "ukrw", "amount": "15800000000"}],
                },
                {
                    "address": "secret105rz2q5a4w7nv7239tl9c4px5cjy7axx3axf6p",
                    "coins": [{"denom": "ukrw", "amount": "6900000000"}],
                },
            ],
        },
    }

    assert MsgMultiSend.from_data(data).to_data() == data
