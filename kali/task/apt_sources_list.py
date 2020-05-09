#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os import path

INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
sys.path.append("{}/-task-".format(INIT_SCRIPT_BASE))
SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


class TaskAptSourcesList(SuperTask):
    def __init__(self):
        self.order = 1
        self.sources_list = """
deb https://mirrors.aliyun.com/kali kali-rolling main non-free contrib
deb-src https://mirrors.aliyun.com/kali kali-rolling main non-free contrib

# deb https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib
# deb-src https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib

# deb https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
# deb-src https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
        """
        self.script = """
################################################################################
apt update
apt upgrade -y --fix-missing
################################################################################
        """

    def do(self):
        try:
            if not path.exists("/etc/apt/sources.list.bak"):
                SuperTask.run("cp /etc/apt/sources.list /etc/apt/sources.list.bak")
            open("/etc/apt/sources.list", "wb").write(self.sources_list.encode())
            return SuperTask.run(self.script)
        except Exception as e:
            SuperTask.print_error(e)
