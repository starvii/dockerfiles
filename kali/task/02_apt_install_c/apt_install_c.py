#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys


class _Actor(object):
    name = "TaskAptInstallC"
    order = 2
    script = """
################################################################################
apt install -y build-essential cmake automake gdb
apt install -y musl-tools gcc-multilib g++-multilib
################################################################################
    """.strip()

    def __init__(self, func=None):
        self.func = func

    def do(self):
        return self.func.run(_Actor.script)


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    ATask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


    class _RealFunc(object):  # delegate task actor
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


    def init_func(self): self.actor = _Actor(_RealFunc)


    # 动态创建类
    _ = type(_Actor.name, (ATask,), dict(
        __init__=init_func,
        order=_Actor.order,
    ))


def main():
    class _FakeFunc(object):  # default actor
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

    _Actor(_FakeFunc).do()


if __name__ == "__main__":
    main()
