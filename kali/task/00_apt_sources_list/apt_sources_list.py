#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path
import shutil


class _Do(object):
    order = 0
    run = print
    print_notice = print
    print_error = print

    def __init__(self):
        self.current_path = path.dirname(path.abspath(__file__))
        self.sources_list = path.join(self.current_path, "sources.list")
        self.script = """
################################################################################
cp {sources_list} /etc/apt/sources.list
apt update
apt upgrade -y --fix-missing
################################################################################
            """.format(sources_list=self.sources_list)

    def do(self):
        try:
            assert path.exists(self.sources_list) and path.isfile(self.sources_list)
            if not path.exists("/etc/apt/sources.list.bak"):
                print("/etc/apt/sources.list.bak not exists. to backup ...")
                shutil.copy2("/etc/apt/sources.list", "/etc/apt/sources.list.bak")
            _Do.run(self.script)
        except Exception as e:
            _Do.print_error(e)


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
    def init_func(self): self._action = _Do()
    _Do.run = SuperTask.run
    _Do.print_notice = SuperTask.print_notice
    _Do.print_error = SuperTask.print_error

    # 动态创建类
    TaskAptSourcesList = type("TaskAptSourcesList", (SuperTask,), dict(
        order=_Do.order,
        __init__= init_func
    ))


def main():
    action = _Do()
    action.do()


if __name__ == "__main__":
    main()
