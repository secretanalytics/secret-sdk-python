from secret_sdk.core.bank import MsgSend
from secret_sdk.key.mnemonic import MnemonicKey
from secret_sdk.core import SignDoc
import base64

from secret_sdk.core.tx import AuthInfo, TxBody
from secret_sdk.core.fee import Fee
from secret_sdk.core import Coins, Numeric


def test_derivation():
    mk = MnemonicKey(
        "wonder caution square unveil april art add hover spend smile proud admit modify old copper throw crew happy nature luggage reopen exhibit ordinary napkin"
    )
    assert mk.acc_address == "secret1xvgdr32t37euwk5s387w4l70vyg8pzkyvcln78"
    assert (
        mk.acc_pubkey
        == "secretpub1addwnpepqghtq0uj7v7p0fx3nryj8g3qt6nf23r53vcm0fx8pxqtlrnyeajmseam6ts"
    )
    assert mk.val_address == "secretvaloper1xvgdr32t37euwk5s387w4l70vyg8pzkyal3wnw"
    assert (
        mk.val_pubkey
        == "secretvaloperpub1addwnpepqghtq0uj7v7p0fx3nryj8g3qt6nf23r53vcm0fx8pxqtlrnyeajmsvttenq"
    )


def test_random():
    mk1 = MnemonicKey()
    mk2 = MnemonicKey()
    assert mk1.mnemonic != mk2.mnemonic


def test_signature():
    mk = MnemonicKey(
        "island relax shop such yellow opinion find know caught erode blue dolphin behind coach tattoo light focus snake common size analyst imitate employ walnut"
    )

    send = MsgSend(
        mk.acc_address,
        "secret1xvgdr32t37euwk5s387w4l70vyg8pzkyvcln78",
        dict(uscrt="1000000"),
    )

    tx_body = TxBody([send])

    auth_info = AuthInfo(signer_infos=[], fee=Fee(Numeric.parse(46467), Coins('698uscrt')))

    signDoc = SignDoc(
        chain_id="holodeck-2",
        account_number=45,
        sequence=0,
        auth_info=auth_info,
        tx_body=tx_body,
    )
    signature = mk.create_signature(signDoc)
    assert (
        base64.b64encode(signature.data.single.signature).decode('utf-8')
        == "67xBRB2QYsPYl4wPvlYYcOKoJaMHS08R1dfNJU5YIdcf8EFsEmRwpFSI6/LtUuk+r6uAiuWN6+sNF+LPeQdpUg=="
    )
