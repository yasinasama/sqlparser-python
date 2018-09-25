sqlparser-python
================

Installation
------------

.. code-block:: bash

    $ git clone https://github.com/yasinasama/sqlparser-python.git
    $ cd sqlparser
    $ python setup.py install


Getting Started
---------------
.. code-block:: pycon

    >>> from sqlparser import parse
    >>> parse("select * from blog where name='zhangsan';")
    {
        'type':'SELECT',
        'column':[{'name':'*'}],
        'table':[{'name':'blog'}],
        'join': [],
        'where':[{'name': 'name', 'value': 'zhangsan', 'compare': '='}],
        'group':[],
        'having':[],
        'order':[],
        'limit':[]
    }

Detail
------

See test_parser.py for more information
