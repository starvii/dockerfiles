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
        self.order = 3
        self.script = """
################################################################################
apt install -y build-essential cmake automake
apt install -y musl-tools gcc-multilib g++-multilib
################################################################################
        """

    def do(self):
        return SuperTask.run(self.script)
