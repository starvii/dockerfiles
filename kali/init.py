#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path
import sys

INIT_SCRIPT_BASE = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append("{}/-task-".format(INIT_SCRIPT_BASE))
os.environ["INIT_SCRIPT_BASE"] = INIT_SCRIPT_BASE
TASK = __import__("task".format(INIT_SCRIPT_BASE))


def main():
    lst = TASK.AbstractTask.import_sub_tasks("{}/kali/task".format(INIT_SCRIPT_BASE))
    for action in lst:
        action.do()


if __name__ == "__main__":
    main()
