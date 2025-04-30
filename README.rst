|License| |Release| |Supported versions| |Docs|
|Code Coverage| |Build status Appveyor| |Build Status Travis CI|
|Contact| |Blog|

Sausage Link
=============

Implementation of the Sausage Link algorithm base Swinging Door in Python.

Example of usage
----------------

.. code:: python

    >>> from datetime import datetime
    >>> from pandas import read_csv, DataFrame

    >>> df = DataFrame(
    ...     [
    ...         {
    ...             "Date": datetime.strptime(date, "%Y-%m-%d"),
    ...             "Price": value
    ...         }
    ...         for date, value in read_csv(
    ...             "https://datahub.io/core/oil-prices/r/wti-daily.csv"
    ...         ).values.tolist()
    ...     ]
    ... )

    >>> print(len(df))
    9895

    >>> df.plot(x="Date", y="Price")

.. code:: python

    >>> from sausage_link import sausage_link

    >>> compress = DataFrame(
    ...      list(
    ...         {
    ...             "Date": datetime.fromtimestamp(date),
    ...             "Price": value
    ...         }
    ...         for date, value in sausage_link(
    ...             iter(
    ...                 (date.timestamp(), value)
    ...                 for date, value in df.values.tolist()
    ...             ), deviation=(1, .5), max_len=604_800,
    ...             auto_dev_factor=200_000, ema_alpha=0.5
    ...         )
    ...     )
    ... )

    >>> print(len(compress))
    4177

    >>> compress.plot(x="Date", y="Price")

.. |License| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target:  https://opensource.org/licenses/MIT
.. |Release| image:: https://img.shields.io/github/release/chelaxe/SausageLink.svg
   :target: https://github.com/chelaxe/SausageLink/releases
.. |Supported versions| image:: https://img.shields.io/pypi/pyversions/sausage_link.svg
   :target: https://pypi.org/project/sausage_link/
.. |Docs| image:: https://readthedocs.org/projects/sausagelink/badge/?version=latest&style=flat
   :target:  https://sausagelink.readthedocs.io/en/latest/
.. |Code Coverage| image:: https://codecov.io/gh/chelaxe/SausageLink/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/chelaxe/SausageLink
.. |Build status Appveyor| image:: https://ci.appveyor.com/api/projects/status/github/chelaxe/sausagelink?branch=main&svg=true
   :target: https://ci.appveyor.com/project/chelaxe/sausagelink
.. |Build Status Travis CI| image:: https://api.travis-ci.com/chelaxe/SausageLink.svg?branch=main
   :target: https://app.travis-ci.com/github/chelaxe/SausageLink
.. |Contact| image:: https://img.shields.io/badge/telegram-write%20me-blue.svg
   :target:  https://t.me/chelaxe
.. |Blog| image:: https://img.shields.io/badge/site-my%20blog-yellow.svg
   :target:  https://chelaxe.ru/
