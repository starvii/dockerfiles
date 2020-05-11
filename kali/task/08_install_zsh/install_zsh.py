#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path
from multiprocessing import Process
import time


class _Do(object):
    order = 8

    @staticmethod
    def run(script, _=True): print(script)

    @staticmethod
    def print_notice(out): print(out)

    @staticmethod
    def print_error(out): print(out)
    install_mode = False

    def __init__(self):
        self.current_path = path.dirname(path.abspath(__file__))
        self.install_sh = path.join(self.current_path, "install.sh")
        self.script_copy = """
################################################################################
cp {install_sh} /tmp/omz.sh
################################################################################
        """.format(install_sh=self.install_sh).strip()
        self.script_download = """
################################################################################
wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O /tmp/omz.sh
################################################################################
        """.strip()
        self.script_install = """
################################################################################
su - admin -c "sh /tmp/omz.sh"
################################################################################
        """.strip()

    def do(self):
        script = ""
        if path.exists(self.install_sh) and path.isfile(self.install_sh):
            script += self.script_copy
        else:
            script += self.script_download
        script += self.script_install
        if _Do.install_mode:
            _Do.proc_install(script)
        else:
            print(script)

    @staticmethod
    def proc_install(script):
        # 由于oh-my-zsh安装完成后会停在shell处，无法自动退出
        # 启动一个新进程安装，本进行进行监控，一旦有shell出现，则kill shell
        p = Process(target=_Do.run, args=(script, False))
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


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
    def init_func(self): self._action = _Do()
    _Do.run = SuperTask.run
    _Do.print_notice = SuperTask.print_notice
    _Do.print_error = SuperTask.print_error
    _Do.install_mode = True

    # 动态创建类
    _ = type("TaskInstallZsh", (SuperTask,), dict(
        order=_Do.order,
        __init__=init_func
    ))


def main():
    action = _Do()
    action.do()


if __name__ == "__main__":
    main()
