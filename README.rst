expiringdict
------------

Caching objects with expiration; If objects haven't been retrieved for a
number of seconds, they get deleted. On each retrieval the expiry date gets
updated (this means retrieval becomes slower).

This is a Python caching library. The core of the library is ExpiringDict class which
is an ordered dictionary with auto-expiring values for caching purposes. Expiration happens on
any access, object is locked during cleanup from expired values. ExpiringDict can not store
more than `max_len` elements - the oldest will be deleted. Additionally, when time expires
they get deleted from memory.


Installation
------------

If you wish to install from PyPi:

.. code-block:: bash

    pip3 install git+https://github.com/benman1/expiringdict.git

If you wish to download the source and install from GitHub:

.. code-block:: bash

    git clone https://github.com/benman1/expiringdict.git
    python3 setup.py install

To run tests with coverage:

.. code-block:: bash

    nosetests --with-coverage --cover-package=expiringdict

Usage
-----

Create a dictionary with capacity for 100 elements and elements expiring in 10 seconds:

.. code-block:: py

    from expiringdict import ExpiringDict
    cache = ExpiringDict(max_len=100, max_age_seconds=10)

put and get a value there:

.. code-block:: py

     cache["key"] = "value"
     cache.get("key")
