.. quickstart:

Quickstart
==========


.. note:: All code starting with a ``$`` is meant to run on your terminal.
    All code starting with a ``>>>`` is meant to run in a python interpreter,
    like `ipython <https://pypi.org/project/ipython/>`_.

Installation
------------

Secret SDK can be installed (preferably in a :ref:`virtualenv <setup_environment>`)
using ``pip`` as follows:

.. code-block:: shell

   $ pip install secret_sdk 


.. note:: If you run into problems during installation, you might have a
    broken environment. See the troubleshooting guide to :ref:`setting up a
    clean environment <setup_environment>`.


Using Secret SDK
---------------

In order to interact with the Secret blockchain, you'll need a connection to a Secret node or an api endpoint - we've used the community api as an example below.
This can be done through setting up an LCDClient:


.. code-block:: python

    from secret_sdk.client.lcd import LCDClient

    client = LCDClient(chain_id="secret-4",
            url="https://api.scrt.network/")
    print(client.tendermint.node_info())


Getting Blockchain Info
-----------------------

It's time to start using Secret SDK! Once properly configured, the ``LCDClient`` instance will allow you
to interact with the Secret blockchain. Try getting the latest block height:

.. code-block:: python

    >>> client.tendermint.block_info()['block']['header']['height']
    '1687543'

Secret SDK can help you read block data, sign and send transactions, deploy and interact with contracts,
and a number of other features.
