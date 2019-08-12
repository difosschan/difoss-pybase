## Aim of the document

- Record the method of packaging and publishing the library.
- Description installation method ( For Non-pythoner operation and maintenance personnel ).

## Packaging

### Make `wheel` package

```bash
cd difoss-pybase-master
python setup.py bdist_wheel --universal
```

The result should be create `difoss_pybase-0.2.7-py2.py3-none-any.whl` in the directory named `dist` ( The specific version number is determined by `__version__` in `difoss_pybase/__init__.py` ) .

## Installing

Copy the wheel file to target machine, and the use `pip` to install:

```bash
cd dist/
pip install difoss_pybase-0.2.7-py2.py3-none-any.whl
```

Testing:

```bash
$ python
Python 2.7.5 (default, Aug  4 2017, 00:39:18)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from difoss_pybase.common_utils import load_json
>>> load_json('{"bless":"you"}')
{u'bless': u'you'}
```

It works !

