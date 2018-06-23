difoss_pybase - Base library in python2.7 with my own habit
===========================================================

This project collect the reusable function(s) and class(es) in my own habit.


Changes
-------

The modifications in this branch are minor fixes and cosmetic changes:

* v0.1.0 base version, includes: common_utils, console_color, mysql_wrapper, sperated_database(read/write in sperated mysql DB).
* v0.2.0 in `common_utils` : add class `StringWithComment`, function `load_json` can filter comment string with c++ style (`//` only by now ).
* v0.2.3 package as wheel/egg done.
* v0.2.4
  - in `common_utils`:
    - Change `Enum` into `NatureNumEnum`, and change `enum` into `FreeEnum`, in order to avoid confilcts with `enum` of Python 4.3.
    - Change implementation of print_error, print_warning.
    - Add print_info, print_debug, print_xxx.
  - in `setup.py`: use `__version__` which declared in `difoss_pybase/__init__.py`, so you can modify the one place when changes version.
* v0.2.5
  - in `common_utils`:
    - Add `run_shell` function.