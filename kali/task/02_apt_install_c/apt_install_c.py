#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys


class DO(object):
    order = 2
    script = """
################################################################################
apt install -y build-essential cmake automake
apt install -y musl-tools gcc-multilib g++-multilib
################################################################################
    """

    run = None
    print_notice = None
    print_error = None

    def __init__(self):
        pass

    @staticmethod
    def do(_):
        DO.run(DO.script)


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
    DO.run = SuperTask.run
    DO.print_notice = SuperTask.print_notice
    DO.print_error = SuperTask.print_error

    # 动态创建类
    TaskAptInstallC = type("TaskAptInstallC", (SuperTask,), dict(
        order=DO.order,
        do=DO.do,
    ))
else:
    DO.run = print
    DO.print_notice = print
    DO.print_error = print
    TaskAptInstallC = type("TaskAptInstallC", (object,), dict(
        order=DO.order,
        do=DO.do,
    ))


def main():
    task = TaskAptInstallC()
    task.do()


if __name__ == "__main__":
    main()
