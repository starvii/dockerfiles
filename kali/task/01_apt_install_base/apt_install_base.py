#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys


class Actor(object):
    name = "TaskAptInstallBase"
    order = 1
    script = """
################################################################################
apt install -y net-tools open-vm-tools openssh-server
apt install -y zsh vim git wget curl pkg-config aria2
apt install -y apt-transport-https ca-certificates gnupg2 lsb-release software-properties-common
systemctl enable ssh
systemctl restart ssh
systemctl set-default multi-user.target
################################################################################
    """.strip()

    def do(self):
        return self.func.run(Actor.script)

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
