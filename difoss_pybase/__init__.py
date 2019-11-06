# coding: UTF-8
#
# The Base Library in Python belongs to Difoss.
#
# Copyright (c) 2017 by Difoss Chan.
#

VERSION=(0, 3, 0)
__version__='.'.join([str(x) for x in VERSION])

from .common_utils import *
from .mysql_wrapper import *
from .console_color import *
from .sperated_database import *
