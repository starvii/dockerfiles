#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path
import shutil


class _Do(object):
    order = 0

    @staticmethod
    def run(script, _=True): print(script)

    @staticmethod
    def print_notice(out): print(out)

    @staticmethod
    def print_error(out): print(out)

    def __init__(self):
        self.current_path = path.dirname(path.abspath(__file__))
        self.sources_list = path.join(self.current_path, "sources.list")
        self.script = """
################################################################################
cp {sources_list} /etc/apt/sources.list
apt update
apt upgrade -y --fix-missing
################################################################################
            """.format(sources_list=self.sources_list).strip()

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
    mod = __import__("task".format(INIT_SCRIPT_BASE))
    SuperTask = mod.AbstractTask
    _Do.run = mod.run
    _Do.print_notice = mod.print_notice
    _Do.print_error = mod.print_error
    def init_func(self): self._action = _Do()


    # 动态创建类
    _ = type("TaskAptSourcesList", (SuperTask,), dict(
        order=_Do.order,
        __init__=init_func
    ))


def main():
    action = _Do()
    action.do()


if __name__ == "__main__":
    main()
