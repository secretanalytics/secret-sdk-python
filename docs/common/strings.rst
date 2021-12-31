.. strings:

Bech32 Strings
==============

To provide some clarity for arguments, some functions in the SDK are documented that
they take a type like :class:`AccAddress` where one may expect a ``str``. It is simply a
type alias annotation (equivalent to ``str``) that serves only to remind the developer
which format the string is expected to be in. 

Terra SDK also provides useful functions for checking and converting **addresses** and **pubkeys**.

Addresses
---------

AccAddress
^^^^^^^^^^

.. autoclass:: secret_sdk.core.strings.AccAddress
    :members:

.. autofunction:: secret_sdk.core.strings.is_acc_address

.. autofunction:: secret_sdk.core.strings.to_acc_address

ValAddress
^^^^^^^^^^

.. autoclass:: secret_sdk.core.strings.ValAddress
    :members:

.. autofunction:: secret_sdk.core.strings.is_val_address

.. autofunction:: secret_sdk.core.strings.to_val_address



PubKeys
-------

AccPubKey
^^^^^^^^^

.. autoclass:: secret_sdk.core.strings.AccPubKey
    :members:

.. autofunction:: secret_sdk.core.strings.is_acc_pubkey

.. autofunction:: secret_sdk.core.strings.to_acc_pubkey

ValPubKey
^^^^^^^^^

.. autoclass:: secret_sdk.core.strings.ValPubKey
    :members:

.. autofunction:: secret_sdk.core.strings.is_acc_pubkey

.. autofunction:: secret_sdk.core.strings.to_acc_pubkey

ValConsPubKey
^^^^^^^^^^^^^

.. autoclass:: secret_sdk.core.strings.ValConsPubKey
    :members: