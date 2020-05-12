#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path


class Actor(object):
    name = "TaskInstallCtfTools"
    order = 12
    current_path = path.dirname(path.abspath(__file__))
    script = """
################################################################################
git clone https://github.com/zardus/ctf-tools.git /home/app/ctf-tools
#dirsearch
#one_gadget
#peda
#pwndbg
#Pwngdb
#rp++
#seccomp-tools
#yafu
#peda
#pwn_debug
#LibcSearcher

################################################################################
    """.strip()

    def do(self):
        self.func.run(Actor.script, False)

    def __init__(self, func=None):
        self.func = func


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    ATask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


    class ProductFunc(object):  # delegate task actor
        def __init__(self):
            pass

        @staticmethod
        def run(script, stop=True):
            ATask.run(script, stop)

        @staticmethod
        def print_notice(out):
            ATask.print_notice(out)

        @staticmethod
        def print_error(out):
            ATask.print_error(out)


    def init_func(self): self.actor = Actor(ProductFunc)


    # 动态创建类
    _ = type(Actor.name, (ATask,), dict(
        __init__=init_func,
        order=Actor.order,
    ))


def main():
    class DebugFunc(object):  # default actor
        def __init__(self):
            pass

        @staticmethod
        def run(script, _=True):
            print(script)

        @staticmethod
        def print_notice(out):
            print(out)

        @staticmethod
        def print_error(out):
            print(out)

    Actor(DebugFunc).do()


if __name__ == "__main__":
    main()
