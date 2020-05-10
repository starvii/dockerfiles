#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys


class _Do(object):
    order = 2

    @staticmethod
    def run(script, _=True): print(script)
    print_notice = print
    print_error = print

    def __init__(self):
        self.script = """
################################################################################
apt install -y build-essential cmake automake
apt install -y musl-tools gcc-multilib g++-multilib
################################################################################
        """.strip()

    def do(self):
        _Do.run(self.script)


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
    def init_func(self): self._action = _Do()
    _Do.run = SuperTask.run
    _Do.print_notice = SuperTask.print_notice
    _Do.print_error = SuperTask.print_error

    # 动态创建类
    _ = type("TaskAptInstallC", (SuperTask,), dict(
        order=_Do.order,
        __init__=init_func
    ))


def main():
    action = _Do()
    action.do()


if __name__ == "__main__":
    main()
