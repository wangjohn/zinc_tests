Zinc Tests
==========

Installation
============

The only thing that this test suite requires is to install nose:

```
pip install nose
```

If that doesn't work, read the documentation for nose: `http://nose.readthedocs.org/en/latest/`.

Running Tests
=============

You can run tests by going into the `tests` directory and running:

```
nosetests --nologcapture
```

The logging output of the tests will be written to the `logs/tests.log` file. Without the `--nologcapture` of the command, the logging output will not be written.

You can also run tests in a specific file by specifying the filename, like so:

```
nosetests --nologcapture test_variant_options.py
```
