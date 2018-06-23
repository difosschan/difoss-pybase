#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals


# -----------------Normal variables in colorama----------------------
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
#
# More reference at colorama: https://pypi.python.org/pypi/colorama


from colorama import init, Fore, Back, Style

# ------------------------------------------------------------------
# @reference: http://blog.csdn.net/qianghaohao/article/details/52117082
# @author: CodeNutter
#          DifossChan modified@2018/03/13: add 'light_xxx' to enhance this.
# ------------------------------------------------------------------
class ConsoleColor(object):
    def __init__(self, autoreset=True):
        init(autoreset=autoreset)

    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.RED + s + Fore.RESET

    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.GREEN + s + Fore.RESET

    #  前景色:黄色  背景色:默认
    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET

    #  前景色:蓝色  背景色:默认
    def blue(self, s):
        return Fore.BLUE + s + Fore.RESET

    #  前景色:洋红色  背景色:默认
    def magenta(self, s):
        return Fore.MAGENTA + s + Fore.RESET

    #  前景色:青色  背景色:默认
    def cyan(self, s):
        return Fore.CYAN + s + Fore.RESET

    #  前景色:白色  背景色:默认
    def white(self, s):
        return Fore.WHITE + s + Fore.RESET

    #  前景色:黑色  背景色:默认
    def black(self, s):
        return Fore.BLACK + s + Fore.RESET

    def light_black(self, s):
        return Fore.LIGHTBLACK_EX + s + Fore.RESET

    def light_red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET

    def light_green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    def light_yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    def light_blue(self, s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET

    def light_magenta(self, s):
        return Fore.LIGHTMAGENTA_EX + s + Fore.RESET

    def light_cyan(self, s):
        return Fore.LIGHTCYAN_EX + s + Fore.RESET

    def light_white(self, s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    ################################################
    #  前景色:白色  背景色:绿色
    def white_green(self, s):
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET

    #  前景色:蓝色  背景色:白色
    def white_blue(self, s):
        return Fore.BLUE + Back.WHITE + s + Fore.RESET + Back.RESET

    # TODO: More free foreground-background scenery to wait for you to explore !
    ################################################

    def clear_screen(self):
        return "\033[2J"

    def cursor_set_position(self, x, y):
        return "\033[%d;%dH" % (y,x)
