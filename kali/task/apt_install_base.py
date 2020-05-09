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
        self.order = 2
        self.script = """
################################################################################
apt install -y net-tools open-vm-tools openssh-server
apt install -y zsh vim git wget curl pkg-config aria2
################################################################################
        """

    def do(self):
        return SuperTask.run(self.script)
