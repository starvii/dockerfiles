#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path
import shutil


class DO(object):
    order = 0
    current_path = path.dirname(path.abspath(__file__))
    sources_list = path.join(current_path, "sources.list")
    script = """
################################################################################
cp {sources_list} /etc/apt/sources.list
apt update
apt upgrade -y --fix-missing
################################################################################
    """.format(sources_list=sources_list)

    run = None
    print_notice = None
    print_error = None

    def __init__(self):
        pass

    @staticmethod
    def do(_):
        try:
            assert path.exists(DO.sources_list) and path.isfile(DO.sources_list)
            if not path.exists("/etc/apt/sources.list.bak"):
                print("/etc/apt/sources.list.bak not exists. to backup ...")
                shutil.copy2("/etc/apt/sources.list", "/etc/apt/sources.list.bak")
            DO.run(DO.script)
        except Exception as e:
            DO.print_error(e)


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
    DO.run = SuperTask.run
    DO.print_notice = SuperTask.print_notice
    DO.print_error = SuperTask.print_error

    # 动态创建类
    TaskAptSourcesList = type("TaskAptSourcesList", (SuperTask,), dict(
        order=DO.order,
        do=DO.do,
    ))
else:
    DO.run = print
    DO.print_notice = print
    DO.print_error = print
    TaskAptSourcesList = type("TaskAptSourcesList", (object,), dict(
        order=DO.order,
        do=DO.do,
    ))


def main():
    task = TaskAptSourcesList()
    task.do()


if __name__ == "__main__":
    main()
