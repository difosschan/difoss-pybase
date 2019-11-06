difoss_pybase: Base library in python 3 with my own habit
===========================================================

![issues](https://img.shields.io/github/issues/difosschan/difoss-pybase)
![stars](https://img.shields.io/github/stars/difosschan/difoss-pybase)
![forks](https://img.shields.io/github/forks/difosschan/difoss-pybase)
![py2](https://img.shields.io/badge/python-2.7-blue)
![issues](https://img.shields.io/badge/python-3-blue)

This project collect the reusable function(s) and class(es) in my own habit.


Changes
-------

The modifications in this branch are minor fixes and cosmetic changes:

* v0.1.0 base version, includes: 

  * **common_utils**
  * **console_color**
  * **mysql_wrapper**
  * **sperated_database** (read/write in sperated mysql DB)

* v0.2.0 in `common_utils` : add class `StringWithComment`, function `load_json` can filter comment string with c++ style (`//` only by now ).

* v0.2.3 package as wheel/egg done.

* v0.2.4
  - in `common_utils`:
    - Change `Enum` into `NatureNumEnum`, and change `enum` into `FreeEnum`, in order to avoid confilcts with `enum` of Python 3.4.3.
    - Change implementation of print_error, print_warning.
    - Add print_info, print_debug, print_xxx.
  - in `setup.py`: use `__version__` which declared in `difoss_pybase/__init__.py`, so you can modify the one place when changes version.
  
* v0.2.5
  - in `common_utils`:
    - Add `run_shell` function.
  
* v0.3.0 Updated to support Python 3. ( So glad to do this because the setuptools improvements make the installation process very simple! )



## How to use -- build & install

```bash
cd difoss-pybase
python setup.py build
python setup.py install
```

## Testing

```bash
$ python
Python 3.7.4 (default, Sep 24 2019, 10:39:30)
[GCC 4.9.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from difoss_pybase.common_utils import load_json
>>> load_json('{"bless":"you"}')
{'bless': 'you'}
```

It works !

