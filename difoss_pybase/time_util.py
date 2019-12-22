# -*- coding:utf-8 -*-
# author: difosschan
# 时间工具

from typing import Tuple, Union

Duration = int

Nanosecond: Duration = 1
Microsecond          = 1000 * Nanosecond
Millisecond          = 1000 * Microsecond
Second               = 1000 * Millisecond
Minute               = 60 * Second
Hour                 = 60 * Minute

__unit_map = {
    "ns": Nanosecond,
    "us": Microsecond,
    "µs": Microsecond,  # U+00B5 = micro symbol
    "μs": Microsecond,  # U+03BC = Greek letter mu
    "ms": Millisecond,
    "s": Second,
    "m": Minute,
    "h": Hour,
}


def __leading_int(s: str) -> Tuple[int, str, Union[str, None]]:
    x, rem, err = int(0), str(""), "time: bad [0-9]*"
    i = 0
    while i < len(s):
        c = s[i]
        if c < '0' or c > '9':
            break
        #print x
        if x > (1 << 63-1)/10:
            #print "x > (1 << 63-1)/10 => %s > %s" %(x, (1 << 63-1)/10)
            return 0, "", err
        x = x * 10 + int(c) - int('0')
        if x < 0:
            #print "x < 0 => %s < 0" %(x)
            return 0, "", err
        i+=1
    return x, s[i:], None

def __leadingFraction(s: str) -> Tuple[int, float, str]:
    x, scale, rem = int(0), float(1), ""
    i, overflow = 0, False
    while i < len(s):
        c = s[i]
        if c <'0' or c > '9':
            break
        if overflow:
            continue
        if x > (1<<63-1)/10 :
            overflow = True
            continue
        y = x*10 + int(c) - int('0')
        if y < 0:
            overflow = True
            continue
        x = y
        scale *= 10
        i += 1
    return x, scale, s[i:]


"""
将时间转成 Nanosecond (10**-9秒)
比如： 5m 转换为 300秒；5m20s 转换为320秒
time 单位支持："ns", "us" (or "μs"), "ms", "s", "m", "h"
"""
def ParseDuration(s: str) -> Duration:
    '''和 go 语言的 time.ParseDuration 提供同样的功能（和实现）'''
    if s == "" or len(s) < 1:
        return 0

    orig = s
    neg = False
    d = int(0)

    # Consume[-+]?
    if s != "":
        if s[0] == "-" or s[0] == "+":
            neg = s[0] == "-"
            s = s[1:]

    # Special case: if all that is left is "0", this is zero.
    if s == "0" or s == "":
        return 0

    while s != "":
        v, f, scale = int(0), int(0), float(1)

        # print("S: %s" %s)
        # the next character must be [0-9.]
        if not (s[0] == "." or '0' <= s[0] and s[0] <= '9'):
            raise Exception("time: invalid duration %s, s:%s" % (orig, s))

        # Consume [0-9]*
        pl = len(s)
        v, s, err = __leading_int(s)
        if err != None:
            raise Exception("time, invalid duration %s" % orig)

        pre = pl != len(s)

        # consume (\.[0-9]*)?
        post = False
        if s != "" and s[0] == ".":
            s = s[1:]
            pl = len(s)
            f, scale, s = __leadingFraction(s)
            post = pl != len(s)
        if not pre and not post:
            raise("time: invalid duration %s" % orig)

        # Consume unit.
        i = 0
        while i < len(s):
            c = s[i]
            if c == '.' or '0' <= c and c <= '9':
                break
            i+=1

        if i == 0:
            raise Exception("time: unknown unit in duration: %s" % orig)

        # print("s:%s, i:%s, s[:i]:%s" %(s, i, s[:i]))
        u = s[:i]
        s = s[i:]
        unit = __unit_map.get(u, None)
        if unit is None:
            raise Exception("time: unknown unit %s in duration %s" % (u, orig))

        if v > (1<<63-1)/unit:
            # overflow
            raise Exception("time: invalid duration %s" % orig)

        v *= unit
        if f > 0 :
            # float64 is needed to be nanosecond accurate for fractions of hours.
            # v >= 0 && (f*unit/scale) <= 3.6e+12 (ns/h, h is the largest unit)
            v += int(float(f) * (float(unit) / scale))
            if v < 0:
                raise Exception("time: invalid duration %s" % orig) # overflow

        d += v
        if d < 0 :
            # overflow
            raise Exception("time: invalid duration %s" % orig)

    if neg :
        d = -d
    return int(d)


__all__ = [
    'ParseDuration',
    'Duration',
    'Nanosecond',
    'Microsecond',
    'Millisecond',
    'Second',
    'Minute',
    'Hour',
]


# Unit test ------------------------------------------------------------
if __name__ == "__main__":
    import traceback
    import sys
    s = "1m20.123s"
    if len(sys.argv) > 1:
        s = sys.argv[1]
    try:
        print( ParseDuration(s) )
    except Exception as e:
        msg = traceback.format_exc()
        print(msg)

