#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path


class AbstractTask:
    def __init__(self):
        raise Exception("Cannot create object from an abstract class")

    def do(self):
        pass

    @staticmethod
    def import_sub_tasks(task_path):
        if not path.isdir(task_path):
            raise IOError("Cannot access task path [{}]".format(task_path))
        for root, _, files in os.walk(task_path):
            r = path.abspath(root)
            sys.path.append(r)
            for fn in files:
                a = path.splitext(fn)
                if a[1].lower() != ".py":
                    continue
                __import__(a[0])
        objs = [c() for c in AbstractTask.__subclasses__()]
        return sorted(objs, key=lambda x: x.order, reverse=False)

    @staticmethod
    def run(script, stop_if_error=True):
        lines = script.split("\n")
        buffer = []
        ret = 0
        for line in lines:
            ln = line.strip()
            if ln.startswith("#"):
                sys.stdout.write(line.rstrip() + "\n")
                continue
            if ln.endswith("\\") and not ln.endswith("\\\\"):
                buffer.append(line.rstrip())
            else:
                if len(buffer) == 0:
                    cmd = line.rstrip()
                else:
                    cmd = "\n".join(buffer)
                    buffer = []
                AbstractTask.print_notice(cmd)
                ret = os.system(cmd)
                ret = ret >> 8
                if ret != 0:
                    AbstractTask.print_error(cmd)
                    if stop_if_error:
                        break
        return ret

    @staticmethod
    def print_notice(out):
        tpl = "\033[1;33m{out}\033[0m\n".format(out=out)
        sys.stdout.write(tpl)

    @staticmethod
    def print_error(out):
        tpl = "\033[5;31m{err}\033[0m: Some error in:\n\033[4m{out}\033[0m\n".format(err="Error", out=out)
        sys.stderr.write(tpl)
