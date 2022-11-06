# bip32utils
Bip 32 utils with custom ripemd160 implementation 

# The Problem

The old python bip32utils module on PyPi [(Look Here)](https://pypi.org/project/bip32utils/) relies on haslib's implementation of ripemd160 encryption which relies on opensssl. openssl deprecated ripemd160 in openssl 3.0. 

# The Solution: 

Use a custom implemetation of ripemd160 encryption. Copied from [here](https://github.com/bitcoin/bitcoin/pull/23716)
