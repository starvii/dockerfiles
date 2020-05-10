#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path
import shutil

class DO(object):
    order = 6
    current_path = path.dirname(path.abspath(__file__))
    pip_conf = path.join(current_path, "pip.conf")
    script = """
################################################################################
cp {pip_conf} /root/.pip
################################################################################
apt install -y python python-pip
apt install -y python3 python3-pip
################################################################################
apt install -y libpython2-dev libpython3-all-dev libssl-dev libmpfr-dev libmpc-dev
python2 -m pip install -U pip setuptools -i {url}
python2 -m pip uninstall crypto pycrypto -i {url}
python2 -m pip install -U pycryptodome -i {url}
python2 -m pip install -U gmpy -i {url}
python2 -m pip install -U gmpy2 -i {url}
python2 -m pip install -U pwntools -i {url}
python3 -m pip install -U pip setuptools -i {url}
python3 -m pip uninstall crypto pycrypto -i {url}
python3 -m pip install -U pycryptodome -i {url}
python3 -m pip install -U gmpy -i {url}
python3 -m pip install -U gmpy2 -i {url}
python3 -m pip install -U uncompyle6 -i {url}
python3 -m pip install -U pwntools -i {url}
python3 -m pip install -U requests -i {url}
python3 -m pip install -U aiohttp -i {url}
python3 -m pip install -U lxml -i {url}
python3 -m pip install -U beautifulsoup4 -i {url}
python3 -m pip install -U tornado -i {url}
################################################################################
    """.format(url="https://mirrors.aliyun.com/pypi/simple", pip_conf=pip_conf)

    run = None
    print_notice = None
    print_error = None

    def __init__(self):
        pass

    @staticmethod
    def do(_):
        if not path.exists("/root/.pip"):
            try:
                os.makedirs("/root/.pip", 0o755)
            except Exception as e:
                DO.print_error(e)
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
