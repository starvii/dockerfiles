#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


class TaskAptInstallBase(SuperTask):
    def __init__(self):
        self.order = 6
        self.script = """
################################################################################
apt install -y golang
################################################################################
        """

    def do(self):
        return self.run(self.script)
