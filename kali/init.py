#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from os import path
import sys
if sys.version_info < (3,):
    input = raw_input
    range = xrange

INIT_SCRIPT_BASE = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
os.environ["INIT_SCRIPT_BASE"] = INIT_SCRIPT_BASE
ATask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


def main():
    lst = ATask.import_sub_tasks("{}/kali/task".format(INIT_SCRIPT_BASE))
    for cls in lst:
        obj = cls()
        obj.do()


if __name__ == "__main__":
    main()
