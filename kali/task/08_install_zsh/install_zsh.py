#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os import path
from multiprocessing import Process
import time


class DO(object):
    order = 8
    current_path = path.dirname(path.abspath(__file__))
    install_sh = path.join(current_path, "install.sh")
    script_copy = """
################################################################################
cp {install_sh} /tmp/omz.sh
################################################################################
    """.format(install_sh=install_sh)
    script_download = """
################################################################################
wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O /tmp/omz.sh
################################################################################
    """
    script_install = """
################################################################################
su - admin -c "sh /tmp/omz.sh"
################################################################################
    """

    run = None
    print_notice = None
    print_error = None
    install_mode = False

    def __init__(self):
        pass

    @staticmethod
    def do(_):
        script = ""
        if path.exists(DO.install_sh) and path.isfile(DO.install_sh):
            script += DO.script_copy
        else:
            script += DO.script_download
        script += DO.script_install
        if DO.install_mode:
            DO.install(script)
        else:
            DO.run(script)

    @staticmethod
    def install(script):
        # 由于oh-my-zsh安装完成后会停在shell处，无法自动退出
        # 启动一个新进程安装，本进行进行监控，一旦有shell出现，则kill shell
        p = Process(target=DO.run, args=(script, False))
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
    DO.run = SuperTask.run
    DO.print_notice = SuperTask.print_notice
    DO.print_error = SuperTask.print_error
    DO.install_mode = True
    # 动态创建类
    TaskInstallZsh = type("TaskInstallZsh", (SuperTask,), dict(
        order=DO.order,
        do=DO.do,
    ))
else:
    DO.run = print
    DO.print_notice = print
    DO.print_error = print
    DO.install_mode = False
    TaskInstallZsh = type("TaskInstallZsh", (object,), dict(
        order=DO.order,
        do=DO.do,
    ))


def main():
    task = TaskInstallZsh()
    task.do()


if __name__ == "__main__":
    main()
