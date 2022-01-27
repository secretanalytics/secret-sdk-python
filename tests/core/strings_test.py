from secret_sdk.core.strings import (
    is_acc_address,
    is_acc_pubkey,
    is_val_address,
    is_val_pubkey,
    is_valcons_pubkey,
    to_acc_address,
    to_acc_pubkey,
    to_val_address,
    to_val_pubkey,
)


def test_validates_acc_address():
    assert not is_acc_address("secretvaloper1xey4ymz4tmlgy6pp54e2ccj307ff6kx647p3hq")
    assert not is_acc_address(
        "secret1xey4ymz4tmlgy6pp54e2ccj307ff6kx6ye0v7f"
    )  # bad checksum
    assert not is_acc_address("cosmos176m2p8l3fps3dal7h8gf9jvrv98tu3rqfdht86")

    assert is_acc_address("secret1ljtckgv3gsgrnhf7f3ygquyse5urwkamx7ln27")


def test_convert_to_acc_address():
    assert (
        to_acc_address("secretvaloper1xey4ymz4tmlgy6pp54e2ccj307ff6kx647p3hq")
        == "secret1xey4ymz4tmlgy6pp54e2ccj307ff6kx6ye0v6f"
    )


def test_validates_val_address():
    assert not is_val_address("secret1xey4ymz4tmlgy6pp54e2ccj307ff6kx6ye0v6f")
    assert not is_val_address(
        "secretvaloper1xey4ymz4tmlgy6pp54e2ccj307ff6kx64rp3hq"
    )  # bad checksum
    assert is_val_address("secretvaloper1xey4ymz4tmlgy6pp54e2ccj307ff6kx647p3hq")


def test_convert_to_val_address():
    assert (
        to_val_address("secret1xey4ymz4tmlgy6pp54e2ccj307ff6kx6ye0v6f")
        == "secretvaloper1xey4ymz4tmlgy6pp54e2ccj307ff6kx647p3hq"
    )


def test_validates_acc_pubkey():
    assert not is_acc_pubkey(
        "secretvaloperpub1addwnpepqvfgz2syfyed50sp5yj4ltd503wkqrlxd2x5du0ukry4fkk3xv8svhuzz0n"
    )
    assert is_acc_pubkey(
        "secretpub1addwnpepqvfgz2syfyed50sp5yj4ltd503wkqrlxd2x5du0ukry4fkk3xv8svz2jphr"
    )


def test_converts_to_acc_pubkey():
    assert (
        to_acc_pubkey(
            "secretvaloperpub1addwnpepqvfgz2syfyed50sp5yj4ltd503wkqrlxd2x5du0ukry4fkk3xv8svhuzz0n"
        )
        == "secretpub1addwnpepqvfgz2syfyed50sp5yj4ltd503wkqrlxd2x5du0ukry4fkk3xv8svz2jphr"
    )


def test_validates_val_pubkey():
    assert not is_val_pubkey(
        "secretpub1addwnpepqvfgz2syfyed50sp5yj4ltd503wkqrlxd2x5du0ukry4fkk3xv8svz2jphr"
    )
    assert is_val_pubkey(
        "secretvaloperpub1addwnpepqvfgz2syfyed50sp5yj4ltd503wkqrlxd2x5du0ukry4fkk3xv8svhuzz0n"
    )


def test_converts_to_val_pubkey():
    assert (
        to_val_pubkey(
            "secretpub1addwnpepqvfgz2syfyed50sp5yj4ltd503wkqrlxd2x5du0ukry4fkk3xv8svz2jphr"
        )
        == "secretvaloperpub1addwnpepqvfgz2syfyed50sp5yj4ltd503wkqrlxd2x5du0ukry4fkk3xv8svhuzz0n"
    )


def test_validates_valcons_pubkey():
    assert not is_valcons_pubkey(
        "secretvaloperpub1addwnpepqvfgz2syfyed50sp5yj4ltd503wkqrlxd2x5du0ukry4fkk3xv8svhuzz0n"
    )
    assert is_valcons_pubkey(
        "secretvalconspub1zcjduepqsth37qgh8365d3m0t99fkuze9ldhnt2gjngg0ahfhlff7vsd0c5qjwwtcr"
    )
