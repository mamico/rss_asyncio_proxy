=================
RSS Asyncio Proxy
=================


.. image:: https://img.shields.io/pypi/v/rss_asyncio_proxy.svg
        :target: https://pypi.python.org/pypi/rss_asyncio_proxy

.. image:: https://img.shields.io/travis/mamico/rss_asyncio_proxy.svg
        :target: https://travis-ci.com/mamico/rss_asyncio_proxy

.. image:: https://readthedocs.org/projects/rss-asyncio-proxy/badge/?version=latest
        :target: https://rss-asyncio-proxy.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Python Boilerplate contains all the boilerplate you need to create a Python package.


* Free software: MIT license
* Documentation: https://rss-asyncio-proxy.readthedocs.io.


Features
--------

Run:

```
% bin/rss_asyncio_proxy --port 8002 --redis redis://127.0.0.1:6379/?db=0
```

Test:

```
% wget -O - http://localhost:8000/rss-proxy?url=https://feedforall.com/sample-feed.xml
```

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
