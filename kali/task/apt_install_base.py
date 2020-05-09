#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


class TaskAptInstallBase(SuperTask):
    def __init__(self):
        self.order = 2
        self.script = """
################################################################################
apt install -y net-tools open-vm-tools openssh-server
apt install -y zsh vim git wget curl pkg-config aria2
systemctl enable ssh
systemctl restart ssh
################################################################################
        """

    def do(self):
        return self.run(self.script)
