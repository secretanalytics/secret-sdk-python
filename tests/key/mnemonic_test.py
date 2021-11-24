from secret_sdk.core.auth import StdFee, StdSignMsg
from secret_sdk.core.bank import MsgSend
from secret_sdk.key.mnemonic import MnemonicKey


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

    fee = StdFee(46467, dict(uscrt=698))

    stdsignmsg = StdSignMsg("holodeck-2", 45, 0, fee, [send], "")
    signature = mk.create_signature(stdsignmsg).signature
    assert (
        signature
        == "kQU4QYxIlMRL+441WJqHSbYKufctVeACi5bRjbxPZltqjdaKuxDVOsY/rDM3TKYqBFk7dueEXQmCle/D1K0puw=="
    )
