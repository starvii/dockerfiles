#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os import path
from multiprocessing import Process
import time

INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


class TaskAptInstallBase(SuperTask):
    def __init__(self):
        self.order = 8
        self.script = """
################################################################################
# wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O /tmp/omz.sh
su - admin -c "sh /tmp/omz.sh"
################################################################################
        """

    def do(self):
        ret = self.get_install_script()
        if ret != 0:
            return ret
        p = Process(target=self.run, args=(self.script,))
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
                print(lines)
                for line in lines:
                    ln = line.strip()
                    a = ln.split(b" ")
                    print(ln)
                    if a[1] == b"zsh":
                        print(a)
                        pid = int(a[0])
                        time.sleep(5)
                        wait_proc = 0
                        break
        os.kill(pid, 9)
        return 0

    def get_install_script(self):
        if path.exists("{}/_external_/oh_my_zsh.sh".format(self.BASE)):
            _c = "cp {}/_external_/oh_my_zsh.sh /tmp/omz.sh".format(self.BASE)
        else:
            _c = "wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O /tmp/omz.sh"
        return self.run(_c)
