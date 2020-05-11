#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path
from multiprocessing import Process
import time


class _Actor(object):
    name = "TaskInstallZsh"
    order = 8
    install_mode = False  # 默认情况不安装。如果安装的时候，需要改为True
    current_path = path.dirname(path.abspath(__file__))
    install_sh = path.join(current_path, "install.sh")
    script_copy = """
################################################################################
cp {install_sh} /tmp/omz.sh
################################################################################
    """.format(install_sh=install_sh).strip()
    script_download = """
################################################################################
wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O /tmp/omz.sh
################################################################################
    """.strip()
    script_install = """
################################################################################
su - admin -c "sh /tmp/omz.sh"
################################################################################
    """.strip()

    def do(self):
        scripts = []
        if path.exists(_Actor.install_sh) and path.isfile(_Actor.install_sh):
            scripts.append(_Actor.script_copy)
        else:
            scripts.append(_Actor.script_download)
        scripts.append(_Actor.script_install)
        script = "\n".join(scripts)
        if _Actor.install_mode:
            return self.proc_install(script)
        else:
            print(script)
            return 0

    def proc_install(self, script):
        # 由于oh-my-zsh安装完成后会停在shell处，无法自动退出
        # 启动一个新进程安装，本进行进行监控，一旦有shell出现，则kill shell
        p = Process(target=self.func.run, args=(script, False))
        p.daemon = True
        p.start()
        pid = p.pid
        wait_proc = 1
        time.sleep(5)
        while wait_proc:
            time.sleep(1)
            os.system("ps -ef | grep -v grep | grep admin | grep zsh | awk '{print $2,$8}'>/tmp/detect_omz.log")
            if path.isfile("/tmp/detect_omz.log"):
                lines = open("/tmp/detect_omz.log", "rb").readlines()
                for line in lines:
                    ln = line.strip()
                    a = ln.split(b" ")
                    if a[1] == b"zsh":
                        pid = int(a[0])
                        time.sleep(5)
                        wait_proc = 0
                        break
        os.kill(pid, 9)
        return 0

    def __init__(self, func=None):
        self.func = func

if "INIT_SCRIPT_BASE" in os.environ:
    _Actor.install_mode = True
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
