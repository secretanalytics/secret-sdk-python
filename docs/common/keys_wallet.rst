Keys & Wallets
==============

A **Key** is an object that provides an abstraction for the agency of signing transactions.

Key (abstract)
--------------

Implementers of Keys meant for signing should override :meth:`Key.sign()<secret_sdk.key.key.Key.sign>`
or :meth:`Key.create_signature()<secret_sdk.key.key.Key.create_signature>` methods. More details are
available in :ref:`guides/custom_key`.

Some properties such as :meth:`acc_address<secret_sdk.key.key.Key.acc_address>` and
:meth:`val_address<secret_sdk.key.key.Key.val_address>` are provided.

.. automodule:: secret_sdk.key.key
    :members:

RawKey
------

.. automodule:: secret_sdk.key.raw
    :members:


MnemonicKey
-----------

.. automodule:: secret_sdk.key.mnemonic
    :members:

Wallet
------

.. automodule:: secret_sdk.client.lcd.wallet
    :members: