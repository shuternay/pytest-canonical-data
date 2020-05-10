=====================
pytest-canonical-data
=====================

.. image:: https://img.shields.io/pypi/v/pytest-canonical-data.svg
    :target: https://pypi.org/project/pytest-canonical-data
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-canonical-data.svg
    :target: https://pypi.org/project/pytest-canonical-data
    :alt: Python versions

.. image:: https://travis-ci.org/shuternay/pytest-canonical-data.svg?branch=master
    :target: https://travis-ci.org/shuternay/pytest-canonical-data
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/shuternay/pytest-canonical-data?branch=master
    :target: https://ci.appveyor.com/project/shuternay/pytest-canonical-data/branch/master
    :alt: See Build Status on AppVeyor

A plugin which allows to compare results with canonical results, based on previous runs.

----

Inspired by `Yandex's canondata plugin`_, `pytest-needle`_ and `pytest-regtest`_.

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Installation
------------

You can install "pytest-canonical-data" via `pip`_ from `PyPI`_::

    $ pip install pytest-canonical-data


Usage
-----

Plugin provides ``canonical_data`` fixture, which allows to create canonical results::

    def test_sth(canonical_data):
        # In the default mode will compare the `result.txt` canonical result with `123` string using `str` driver
        # In the canonize mode will save `123` as the `result.txt` canonical result
        assert canonical_data('result.txt', 'text') == '123'

To run in canonize mode execute::

    pytest --canonize

It will create files with canonical results (if don't exist) and save actual results.

The plugin saves canonical results in ``canonical_data`` directory next to the test file. It also saves actual results
values in ``_output_data`` directory (for debug purposes).

Drivers
^^^^^^^

You need to use appropriate driver for each data type. Currently, there are the following drivers:

* ``bytes``: for comparing bytes sequences.
* ``str``: for comparing python strings.
* ``json``: for comparing objects which can be loaded from and dumped to json.

TODO
----

* Driver for images
* Driver for json
* HTML reports for images


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-canonical-data" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/shuternay/pytest-canonical-data/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`Yandex's canondata plugin`: https://github.com/catboost/catboost/blob/master/library/python/testing/yatest_common/yatest/common/canonical.py
.. _`pytest-needle`: https://github.com/jlane9/pytest-needle
.. _`pytest-regtest`: https://gitlab.com/uweschmitt/pytest-regtest