#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys


class DO(object):
    order = 6
    script = """
################################################################################
apt install -y python python-pip
apt install -y python3 python3-pip
################################################################################
apt install -y libpython2-dev libpython3-all-dev libssl-dev libmpfr-dev libmpc-dev
python2 -m pip install -U pip setuptools
# it seems some dependencies of python2 are deprecated.
### python2 -m pip install -U pwntools
python2 -m pip uninstall crypto pycrypto
python2 -m pip install -U pycryptodome
python2 -m pip install -U gmpy
python2 -m pip install -U gmpy2
python2 -m pip install -U pwntools
python3 -m pip install -U pip setuptools
python3 -m pip uninstall crypto pycrypto
python3 -m pip install -U pycryptodome
python3 -m pip install -U gmpy
python3 -m pip install -U gmpy2
python3 -m pip install -U uncompyle6
python3 -m pip install -U pwntools
python3 -m pip install -U requests
python3 -m pip install -U aiohttp
python3 -m pip install -U lxml
python3 -m pip install -U beautifulsoup4
python3 -m pip install -U tornado
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
    TaskAptInstallPython = type("TaskAptInstallPython", (SuperTask,), dict(
        order=DO.order,
        do=DO.do,
    ))
else:
    DO.run = print
    DO.print_notice = print
    DO.print_error = print
    TaskAptInstallPython = type("TaskAptInstallPython", (object,), dict(
        order=DO.order,
        do=DO.do,
    ))


def main():
    task = TaskAptInstallPython()
    task.do()


if __name__ == "__main__":
    main()
