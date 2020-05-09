#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os import path

INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
sys.path.append("{}/-task-".format(INIT_SCRIPT_BASE))
SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


class TaskAptInstallBase(SuperTask):
    def __init__(self):
        self.order = 5
        self.script = """
################################################################################
apt install -y mariadb-server php php-mysql apache2
systemctl stop nginx
systemctl disable nginx
systemctl stop apache2
systemctl disable apache2
systemctl stop mysql
systemctl disable mysql
# TODO: change mariadb password
################################################################################
        """

    def do(self):
        return SuperTask.run(self.script)
