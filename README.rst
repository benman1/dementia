dementia
------------

Caching objects with expiration; If objects haven't been retrieved for a
number of seconds, they get deleted. On each retrieval the expiry date gets
updated (this means retrieval becomes slightly slower). In this way, this
data structure works in accordance with the neuroscience principle "use it,
or lose it."

This is a Python caching library. The core of the library is the dementia class which
is an ordered dictionary with auto-expiring values for caching purposes. Expiration happens
in the background, object is locked during cleanup from expired values. A dementia structure
can not store more than `max_len` elements - the one that was used latest will be deleted.
Additionally, when time expires they get deleted from memory.

TODO: 
1. inherit from dict instead of OrderedList
2. pop takes the least used item
      * for this purpose a counter could be preserved
      * the counter can be used for checking if any retrieval has been made after last check

Installation
------------

If you wish to install from PyPi:

.. code-block:: bash

    pip3 install git+https://github.com/benman1/dementia.git

If you wish to download the source and install from GitHub:

.. code-block:: bash

    git clone https://github.com/benman1/dementia.git
    python3 setup.py install

To run tests with coverage:

.. code-block:: bash

    nosetests --with-coverage --cover-package=dementia

Usage
-----

Create a dictionary with capacity for 100 elements and elements expiring in 10 seconds:

.. code-block:: py

    from dementia import Dementia
    cache = Dementia(max_len=100, max_age_seconds=10)

put and get a value there:

.. code-block:: py

     cache["key"] = "value"
     cache.get("key")
