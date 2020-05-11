#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path
import shutil


class _Actor(object):
    order = 0
    current_path = path.dirname(path.abspath(__file__))
    sources_list = path.join(current_path, "sources.list")
    script = """
################################################################################
cp {sources_list} /etc/apt/sources.list
apt update
apt upgrade -y --fix-missing
################################################################################
    """.format(sources_list=sources_list).strip()

    def __init__(self, func=None):
        self.func = func

    def do(self):
        try:
            assert path.exists(self.sources_list) and path.isfile(self.sources_list)
            if not path.exists("/etc/apt/sources.list.bak"):
                print("/etc/apt/sources.list.bak not exists. to backup ...")
                shutil.copy2("/etc/apt/sources.list", "/etc/apt/sources.list.bak")
            self.func.run(_Actor.script)
        except Exception as e:
            self.func.print_error(e)


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
    _ = type("TaskAptSourcesList", (ATask,), dict(
        __init__=init_func,
        order=_Actor.order,
    ))


def main():
    _Actor(_FakeFunc).do()


if __name__ == "__main__":
    main()
