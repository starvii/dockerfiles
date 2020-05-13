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
    script = r"""
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
git clone --depth 1 https://github.com/pwndbg/pwndbg /home/app/pwndbg
cd /home/app/pwndbg/ && bash /home/app/pwndbg/setup.sh && cd ~
git clone --depth 1 https://github.com/scwuaptx/Pwngdb.git /home/app/pwngdb
git clone --depth 1 https://github.com/longld/peda.git /home/app/peda
bash -c "echo -e 'source /home/app/pwndbg/gdbinit.py\nsource /home/app/peda/peda.py\nsource /home/app/pwngdb/pwngdb.py\nsource /home/app/pwngdb/angelheap/gdbinit.py\n\ndefine hook-run\npython\nimport angelheap\nangelheap.init_angelheap()\nend\nend'>/home/admin/.gdbinit"

git clone --depth 1 https://github.com/zardus/ctf-tools.git /home/app/ctf-tools
wget https://github.com/downloads/0vercl0k/rp/rp-lin-x64 -O /usr/bin/rp++

git clone --depth 1 https://github.com/lieanu/LibcSearcher.git /home/app/LibcSearcher
python3 /home/app/LibcSearcher/setup.py devleop
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
