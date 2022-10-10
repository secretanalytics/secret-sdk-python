from typing import List
import bech32


def address_to_bytes(address: str) -> bytes:
    _prefix, b = bech32.bech32_decode(address)
    b = from_words(b)
    return bytes(b)


def bytes_to_address(b: bytes, prefix: str = "secret") -> str:
    b = to_words(b)
    res = bech32.bech32_encode(prefix, b)
    return res


def from_words(words: List[int]) -> List[int]:
    res = convert(words, 5, 8, False)
    if res is None:
        raise ValueError(res)

    return res


def to_words(bytes: List[int]) -> List[int]:
    return convert(bytes, 8, 5, True)


def convert(data: List[int], inBits: int, outBits: int, pad: bool = False) -> List[int]:
    value = 0
    bits = 0
    maxV = (1 << outBits) - 1

    result = []
    for i in range(len(data)):
        value = (value << inBits) | data[i]
        bits += inBits

        while bits >= outBits:
            bits -= outBits
            result.append((value >> bits) & maxV)

    if pad:
        if bits > 0:
            result.append((value << (outBits - bits)) & maxV)

    else:
        if bits >= inBits:
            raise ValueError("Excess Padding")
        if ((value << outBits - bits)) & maxV:
            raise ValueError("Non-zero padding")

    return result
