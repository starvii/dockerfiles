#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 最近有段时间python-pip无法安装。2020-05-10 kali暂时没有这种情况了
# 使用 wget https://bootstrap.pypa.io/get-pip.py
# python2 get-pip.py 安装pip
# huawei pypi源有问题，很多库没有。aliyun 暂时没发现不能安装的库

from __future__ import print_function
import os
import sys


class _Actor(object):
    name = "TaskAptInstallPython"
    order = 6
    script = """
################################################################################
cp {pip_conf} /root/.pip
################################################################################
apt install -y python python-pip
apt install -y python3 python3-pip
################################################################################
apt install -y libpython2-dev libpython3-all-dev libssl-dev libmpfr-dev libmpc-dev
python2 -m pip install -U pip setuptools -i {url}
python2 -m pip uninstall -y pycrypto
python2 -m pip install -U pycryptodome -i {url}
python2 -m pip install -U gmpy -i {url}
python2 -m pip install -U gmpy2 -i {url}
python2 -m pip install -U pwntools -i {url}
python3 -m pip install -U pip setuptools -i {url}
python3 -m pip uninstall -y pycrypto
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
python3 -m pip install -U PIL -i {url}
################################################################################
    """.strip().format(url="https://mirrors.aliyun.com/pypi/simple")

    def __init__(self, func=None):
        self.func = func

    def do(self):
        return self.func.run(_Actor.script, False)


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
    _ = type(_Actor.name, (ATask,), dict(
        __init__=init_func,
        order=_Actor.order,
    ))


def main():
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

    _Actor(_FakeFunc).do()


if __name__ == "__main__":
    main()
