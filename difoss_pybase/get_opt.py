# -*- coding:utf-8 -*-
# author: difosschan
#

import sys, os
from typing import *
import getopt

class FlagIdx:
    SHORT_OPT = 0
    LONG_OPT = 1
    HAS_ARG = 2
    DESC = 3
    ARG_DEFAULT_VALUE = 4

def _gen_params_desc(s: str, l: str) -> str:
    desc = []
    if s is not None and s != '':
        desc.append(f'-{s}')
    if l is not None and l != '':
        desc.append(f'--{l}')
    return '/'.join(desc)

def get_usage(FLAG_SPEC: List[Tuple[str, str, bool, str, Any]]):

    return '''Usage: python {file}
    {param_detail}''' \
    .format(
    file=sys.argv[0].split(os.path.sep)[-1],
    param_detail='\n    '.join([
        '[{params_desc} ...]  {detail} (Default: {default})'
            .format(params_desc=_gen_params_desc(x[FlagIdx.SHORT_OPT], x[FlagIdx.LONG_OPT]),
                    detail=x[FlagIdx.DESC], default=x[FlagIdx.ARG_DEFAULT_VALUE])
        if x[FlagIdx.HAS_ARG] else
        '[{params_desc}]  {detail}'
            .format(params_desc=_gen_params_desc(x[FlagIdx.SHORT_OPT], x[FlagIdx.LONG_OPT]),
                    detail=x[FlagIdx.DESC])
        for x in FLAG_SPEC]
    ))



def get_opt(
        FLAG_SPEC: List[Tuple[str, str, bool, str, Any]],
        ALLOW_ACTIONS: List[str]
) -> Tuple[ List[Dict[str, Any]], Dict[str, Any] ]:

    try:
        short_opts = "".join( [t[FlagIdx.SHORT_OPT]
             + (":" if t[FlagIdx.HAS_ARG] else "") for t in FLAG_SPEC if t[FlagIdx.SHORT_OPT] is not None])
        long_opts = [t[FlagIdx.LONG_OPT] \
             + ("=" if t[FlagIdx.HAS_ARG] else "") for t in FLAG_SPEC if t[FlagIdx.LONG_OPT] is not None]

        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
        kwargs = {}
        actions = []
        for t in FLAG_SPEC:
            # action 不加入 kwargs
            if t[FlagIdx.LONG_OPT] in ALLOW_ACTIONS:
                continue
            elif t[FlagIdx.HAS_ARG] is False:  # 不带参数的选项跳过，等后续再追加
                continue
            elif t[FlagIdx.ARG_DEFAULT_VALUE] is None:  # 要带参数的选项，如果默认参数为 None，则跳过
                continue

            # 以长参数名为 key，写入 ARG_DEFAULT_VALUE 值
            kwargs[ t[FlagIdx.LONG_OPT] ] = t[FlagIdx.ARG_DEFAULT_VALUE]

        for (opt, val) in opts:
            flag = opt.lstrip('-')
            is_long_opt = opt[:2] == '--'

            # print(f'[D]. opt={opt}, flag={flag}, val={val}')
            ok = -1
            for i, t in enumerate(FLAG_SPEC):
                if (is_long_opt and t[FlagIdx.LONG_OPT] == flag)\
                        or (not is_long_opt and t[FlagIdx.SHORT_OPT] == flag):
                    ok = i
                    break

            # print(f'is_long_opt={is_long_opt}, FLAG_SPEC[{ok}]={FLAG_SPEC[ok]}')
            if ok >= 0 and ok < len(FLAG_SPEC):
                default_value = FLAG_SPEC[ok][FlagIdx.ARG_DEFAULT_VALUE]
                action = FLAG_SPEC[ok][FlagIdx.LONG_OPT]
                value = default_value

                if FLAG_SPEC[ok][FlagIdx.HAS_ARG] == True:  # 需要带参数的，以 default_value 字段的类型转换紧跟着传入的值
                    if default_value is None:
                        value = None
                    if isinstance(default_value, int):
                        value = int(val)
                    elif isinstance(default_value, float):
                        value = float(val)
                    else:
                        value = val

                # 后面不带参数，也可以使用默认值
                if action in ALLOW_ACTIONS:
                    actions.append({action: value})
                else:
                    kwargs[action] = value

        if kwargs.get('help') is not None:
            raise getopt.error('')

        # print(f'kwargs={kwargs}', file=sys.stderr)
        # print(f'actions={actions}', file=sys.stderr)

        return actions, kwargs

    except getopt.error:
        print(get_usage(FLAG_SPEC), file=sys.stderr)
        sys.exit(1)

