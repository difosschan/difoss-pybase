#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ------------------------------------------------------------
import ctypes, os, sys
# os.path.islink 在 windows 下有问题
def is_symlink(path):
    FILE_ATTRIBUTE_REPARSE_POINT = 0x0400
    return os.path.isdir(path) and (ctypes.windll.kernel32.GetFileAttributesW(str(path)) & FILE_ATTRIBUTE_REPARSE_POINT)

# ------------------------------------------------------------
from subprocess import Popen, PIPE, STDOUT
import platform
# -----------------------------------------
# @return returncode, stdout, stderr
def run_shell( cmd_str, cwd=None ):
    close_fds = not (platform.system() == 'Windows') # 妈逼的 windows 不支持 close_fds=True

    p = Popen( cmd_str, shell=True, stdout=PIPE, stderr=PIPE, close_fds=close_fds, cwd=cwd )

    p.wait()
    stdoutdata, stderrdata = p.communicate()

    from py3 import PY3
    if PY3: # process.communicate returns bytes in Python3
        stdoutdata = str(stdoutdata, 'utf-8')
        stderrdata = str(stderrdata, 'utf-8')
    else:
        stdoutdata = str(stdoutdata).decode('raw_unicode_escape')
        stderrdata = str(stderrdata).decode('raw_unicode_escape')

    stdoutdata = stdoutdata.rstrip('\n')
    stderrdata = stderrdata.rstrip('\n')
    returncode = p.returncode
    return (returncode, stdoutdata, stderrdata)

# ------------------------------------------------------------
# 用于处理从文件中读出的字符串处理类
# reference: https://blog.csdn.net/Foolishwolf_x/article/details/73177781
import re
class StringWithComment:
    def __init__(self, instr):
        self.instr = instr

    # 删除“//”标志后的注释
    def rm_comment(self):
        qtCnt = cmtPos = slashPos = 0
        rearLine = self.instr
        # rearline: 前一个“//”之后的字符串，
        # 双引号里的“//”不是注释标志，所以遇到这种情况，仍需继续查找后续的“//”
        while rearLine.find('//') >= 0: # 查找“//”
            slashPos = rearLine.find('//')
            cmtPos += slashPos
            headLine = rearLine[:slashPos]
            while headLine.find('"') >= 0: # 查找“//”前的双引号
                qtPos = headLine.find('"')
                if not self.is_escape_opr(headLine[:qtPos]): # 如果双引号没有被转义
                    qtCnt += 1 # 双引号的数量加1
                headLine = headLine[qtPos+1:]
            if qtCnt % 2 == 0: # 如果双引号的数量为偶数，则说明“//”是注释标志
                return self.instr[:cmtPos]
            rearLine = rearLine[slashPos+2:]
            cmtPos += 2
        return self.instr

    # 判断是否为转义字符
    def is_escape_opr(self, instr):
        if len(instr) <= 0:
            return False
        cnt = 0
        while instr[-1] == '\\':
            cnt += 1
            instr = instr[:-1]
        if cnt % 2 == 1:
            return True
        else:
            return False

# ------------------------------------------------------------
import os

def get_file_info(fullname):
    (filepath,tempfilename) = os.path.split(fullname)
    (shortname,extension) = os.path.splitext(tempfilename)
    return {'shortname':shortname, 'extension':extension, 'path':filepath}

def read_txt_2_list( filename ):
    r = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip() # 紧缩左右空字符
            if len( line ) > 0: # 跳过空行
                r.append(line)
    return r
# ------------------------------------------------------------
def print_utf8( utf8_str ):
    if sys.stdin.encoding:
        print(utf8_str.decode('utf8').encode(encoding=sys.stdin.encoding, errors='ignore'))
    else:
        print(utf8_str)

# 打印对象的所有属性值
def print_object(obj, indent=2):
    print('\n'.join( [ ' '*indent + '%s: %s' % item for item in list(obj.__dict__.items())] ))

# 打印进度条
def view_bar(num, total, ndigits=0, fillwith='>'):
    rate = (num + 1) / float(total)
    rate_num = int(rate * 100)
    if ndigits==0:
        r = '\r[%s%s] %d%%' % (fillwith*rate_num, " "*(100-rate_num), rate_num )
    else:
        r = '\r[%s%s] %.{ndigits}f%%'.format(ndigits=ndigits) % (fillwith*rate_num, " "*(100-rate_num), round(rate * 100, ndigits))

    if num + 1 >= total:
        r += '\n'
    sys.stdout.write(r)
    sys.stdout.flush()

from .console_color import ConsoleColor

def print_comment(s):
    for line in s.splitlines():
        print('// %s' % line)

def print_xxx(s, level_str, color):
    # declare the global variable: g_color
    if 'g_color' not in globals():
        globals()['g_color'] = ConsoleColor()
    global g_color
    sys.stderr.write('%s: %s\n' % (getattr(g_color, color)(level_str), s))
    
def print_error(s, level_str='ERROR'):
    print_xxx(s, level_str, 'red')

def print_warning(s, level_str='WARING'):
    print_xxx(s, level_str, 'yellow')

def print_info(s, level_str='INFO'):
    print_xxx(s, level_str, 'cyan')
    
def print_debug(s, level_str='DEBUG'):
    print_xxx(s, level_str, 'magenta')

# 测试相关打印
def check_test( target_value, test_value, call_str='' ):
    # declare the global variable: g_color
    if 'g_color' not in globals():
        globals()['g_color'] = ConsoleColor()

    global g_color
    if test_value == target_value:
        print('[%s] %s => %s' % ( g_color.green('PASS') , call_str, test_value.__str__() ))
    else:
        print('[%s] %s => %s, target: %s' % (g_color.red('FAIL'), call_str,  test_value.__str__(), target_value.__str__()))
    return test_value == target_value

def unit_test( target_value, eval_str):
    f = sys._getframe(1) # 获取上一层堆栈
    test_value = eval(eval_str, f.f_globals, f.f_locals)
    return check_test( target_value, test_value, eval_str)

import types
def dir_and_type( obj, depth=0, lines=None, objstr='' ):
    if depth > 5 or not obj:
        return ''
    g = globals()
    if 'g_color' not in g:
        g['g_color'] = ConsoleColor()

    sub_objs_name = dir(obj)
    len_shown = 0

    if not lines:
        lines = []

    for j, sub_name in enumerate(sub_objs_name):
        if sub_name.startswith('__'):
            continue

        len_shown += 1
        sub_obj = getattr(obj, sub_name)
        sub_obj_detail = ''
        sub_obj_type = type(sub_obj)
        sub_obj_typename = str(sub_obj_type)[len("<type '") : -2]

        is_extend = sub_obj_type is type
        is_tuple = sub_obj_type is tuple
        is_show_detail = sub_obj_type is dict

        is_show_doc = sub_obj_type is types.BuiltinFunctionType \
          or sub_obj_type is types.BuiltinMethodType \
          or sub_obj_type is types.UnboundMethodType

        if is_show_doc:
            sub_obj_detail = (sub_obj.__doc__) if sub_obj.__doc__ else ''
        else:
            sub_obj_detail = str(sub_obj).decode(sys.stdin.encoding, 'ignore').encode('utf-8')

        sub_name_shown = ('|' if depth else '') + '--' * depth + sub_name
        # print(sub_name_shown, sub_obj_typename)

        lines.append( [depth, sub_name, g['g_color'].white_blue(sub_obj_typename) if is_extend else g['g_color'].green(sub_obj_typename), sub_obj_detail] )

        if is_extend:
            dir_and_type( sub_obj, depth + 1, lines, sub_name)

    return lines

# ------------------------------------------------------------

####################################
# For:
#   Enumeration types which values are declared automatically as natural-number.
#   The enumeration value will increase from 0 to one by one.
#
# Example:
# >>> Number = NatureNumEnum([ 'ZERO', 'ONE', 'THREE' ])
# >>> print(type(Number), Number.ONE)
# (<class '__main__.NatureNumEnum'>, 1)
#
class NatureNumEnum(tuple):
    __getattr__ = tuple.index

####################################
# For:
#   Enum declaration can be assigned to different types of its value.
#
# Exapmle:
# >>> Number = FreeEnum( ONE=1, TWO=2, THREE='three' )
# >>> print(Number.THREE == 3, Number.ONE == 1)
# (False, True)
#
def FreeEnum(**enums):
   return type(str('Enum'), (), enums)

class Locked(object):
    def __init__(self, lock):
        self._lock = lock
    def __enter__(self):
        self._lock.acquire()
    def __exit__(self, type, value, tb):
        self._lock.release()

# ------------------------------------------------------------
import multiprocessing, signal, time

class CtrlC(object):
    def __init__(self):
        self.__sem = multiprocessing.Semaphore(value=0)
        self.__exit_flag = False

        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)
        print("Had registered the signal processing function.")

    def is_exit(self):
        return self.__exit_flag

    def semaphore(self):
        return self.__sem

    def __del__(self):
        pass

    def quit(self, signum, frame):
        print("\nCtrlC.quit() is called.")
        self.__exit_flag = True
        self.__sem.release()

# ------------------------------------------------------------
import time

def sec_to_timestr(sec):
    (year, mon, mday, hour, min, sec, wday, yday, isdst) = time.localtime(sec)
    return '%04d-%02d-%02d %02d:%02d:%02d' % (year, mon, mday, hour, min, sec)

def sec_to_filename_str(sec):
    return time.strftime('%Y%m%d.%H%M%S', time.localtime(sec))

def sec_to_dict(sec):
    (year, mon, mday, hour, min, sec, wday, yday, isdst) = time.localtime(sec)
    return {'year':year, 'month':mon, 'day':mday, 'hour':hour, 'minute':min, 'second':sec}

def dict_to_sec(d):
    str_t = time.strptime('%4d-%02d-%02d %02d:%02d:%02d' % (d['year'], d['month'], d['day'], d['hour'], d['minute'], d['second']), "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(str_t))

def str_to_sec(str_t):
    return int(time.mktime(time.strptime(str_t, "%Y-%m-%d %H:%M:%S")))

def zero_sec( sec ):
    (year, mon, mday, hour, min, sec, wday, yday, isdst) = time.localtime(sec)
    return int(time.mktime( (year, mon, mday, 0, 0, 0, wday, yday, isdst)))

def month_1st_zero_sec( sec ):
    (year, mon, mday, hour, min, sec, wday, yday, isdst) = time.localtime(sec)
    return int(time.mktime( (year, mon, 1, 0, 0, 0, wday, yday, isdst)))

# ------------------------------------------------------------
def list_to_dict(fields_name_list, values_list):
    min_cnt = min( len(values_list), len(fields_name_list) )
    d = dict()
    for i, field_name in enumerate(fields_name_list[:min_cnt]):
        d[field_name] = values_list[i]
    return d

# 逐层进入 dict，并试图获得参数 key_list 所指引的子节点
def deep_into_dict( d, key_list, default=None ):
    if not isinstance(d, dict):
        return default

    k = key_list[0]
    if len(key_list) == 1:
        if k in d:
            return d[k]
        else:
            return default

    if k in d:
        return deep_into_dict( d[k], key_list[1:] )
    return default

CUT_UP_LENGTH = NatureNumEnum( ['LEFT', 'DURING', 'RIGHT'] )
# @return: length of 3 part (l, m, r) which cut by @parameter `basic_range`
def cut_up( target_range, basic_range ):
    # # FIXME: 目前用 None 代表【无穷小】，sys.maxint 表示【无穷大】，是否存在隐患。
    b0 = basic_range[0] if len(basic_range) else None           # 除了 None 任何值都比 None 大
    b1 = basic_range[1] if (len(basic_range) > 1 and basic_range[1] != None) else sys.maxsize
    if b0 > b1:
        b0, b1 = b1, b0

    t0 = target_range[0]
    t1 = target_range[1] if (len(target_range) > 1 and target_range[1] != None) else sys.maxsize
    if t0 > t1:
        t0, t1 = t1, t0

    l = m = r = 0

    list_sorted = [b0, b1, t0, t1]
    list_sorted.sort()

    if b0 >= t1:
        #  [t0 .. t1]
        #              [b0 ... b1]
        l = t1 - t0
    elif list_sorted == [t0, b0, t1, b1]:
        # [t0 ...... t1]
        #      [b0 ........... b1]
        l = b0 - t0
        m = t1 - b0
    elif list_sorted == [t0, b0, b1, t1]:
        # [t0 ........................ t1]
        #      [b0 ........... b1]
        l = b0 - t0
        m = b1 - b0
        r = t1 - b1
    elif list_sorted == [b0, t0, t1, b1]:
        #          [t0 ... t1]
        #      [b0 ........... b1]
        m = t1 - t0
    elif list_sorted == [b0, t0, b1, t1]:
        #              [t0 ........... t1]
        #      [b0 ........... b1]
        m = b1 - t0
        r = t1 - b1
    elif t0 >= b1:
        #                           [t0 .. t1]
        #      [b0 ........... b1]
        r = t1 - t0

    return (l, m, r)

# ------------------------------------------------------------
import logging

def init_logger(log_cfg, prefix='', sec=None):

    timestr = sec_to_filename_str(sec if sec else (int(time.time())))
    log_filename = '%s_%s.log' % (prefix, timestr)
    log_level = getattr(logging, log_cfg['level'].upper())
    logging.basicConfig(\
        level = log_level,
        format = '%(asctime)s [%(module)s:%(lineno)d] %(levelname)s: %(message)s',
        datefmt='%Y%m%d.%H%M%S',
        filename = log_cfg['dir'] + "/" + log_filename,
        filemode = 'w')

    if 'g_logger' not in globals():
        globals()['g_logger'] = logging.getLogger()
    return globals()['g_logger']

def log(level_str, msg, *args, **kwargs):
    print_stdout = False
    level_str = level_str.upper()
    level_arr = level_str.split()
    if 'IMPORTANT' in level_arr:
        level_arr.remove('IMPORTANT')
        if len(level_arr) > 0:
            level_str = level_arr[0]
        else:
            level_str = "NOTSET"

        print_stdout = True

    if deep_into_dict( globals(), ['g_logger'] ):
        # FIXME: 没有异常的时候，exc_info 都是假的
        globals()['g_logger'].log( getattr(logging, level_str), msg, *args, **kwargs)
    else:
        print_stdout = True # print into stdout when g_logger isn't set

    if print_stdout:
        print(("[%s] %s" % (level_str, msg))) # temporary print to stdout

# ------------------------------------------------------------
import json

def load_json_file( fn ):
    cfg = dict()
    with open(fn) as json_cfg:
        s = json_cfg.read()
        return load_json( s )


def load_json( s ):
    dstJsonStr = ''
    for line in s.splitlines():
        # 支持以 “//” 为注释，包括整行和一行结尾的注释
        if not re.match(r'\s*//', line) and not re.match(r'\s*\n', line):
            xline = StringWithComment(line)
            dstJsonStr += xline.rm_comment()

    dstJson = None
    try:
        dstJson = json.loads(dstJsonStr)
    except:
        print('load_json(str): found `str` is not a valid json file.')

    return dstJson

# ------------------------------------------------------------
