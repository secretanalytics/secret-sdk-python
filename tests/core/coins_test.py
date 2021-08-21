import pytest

from terra_sdk.core import Coin, Coins


def test_clobbers_similar_denom():
    coins1 = Coins([Coin("ukrw", 1000), Coin("uscrt", 1000), Coin("uscrt", 1000)])

    coinKRW = coins1["ukrw"]
    coinLUNA = coins1["uscrt"]

    assert coinKRW.amount == 1000
    assert coinLUNA.amount == 2000


def test_converts_dec_coin():
    c1 = Coins(uscrt=1000, ukrw=1.234)
    c2 = Coins(uscrt=1000, ukrw=1234)

    assert all(c.is_dec_coin() for c in c1)
    assert not all(c.is_dec_coin() for c in c2)


def test_from_str():
    int_coins_string = "5ukrw,12uscrt"
    dec_coins_string = "2.3ukrw,1.45uscrt"
    neg_dec_coins_string = "-1.0ukrw,2.5uscrt"

    int_coins = Coins(ukrw=5, uscrt="12")
    dec_coins = Coins(
        ukrw=2.3,
        uscrt="1.45",
    )

    neg_dec_coins = Coins(
        ukrw="-1.0",
        uscrt=2.5,
    )

    assert Coins.from_str(int_coins_string) == int_coins
    assert Coins.from_str(dec_coins_string) == dec_coins
    assert Coins.from_str(neg_dec_coins_string) == neg_dec_coins
