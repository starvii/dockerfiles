# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
# import os
# import sys
# from os import path
#
# INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
# sys.path.append("{}/-task-".format(INIT_SCRIPT_BASE))
# SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
#
#
# class TaskAptInstallBase(SuperTask):
#     def __init__(self):
#         self.order = 6
#         self.pip_conf = """
# [global]
# index-url = https://mirrors.huaweicloud.com/repository/pypi/simple
# trusted-host = mirrors.huaweicloud.com
# timeout = 120
#         """
#         self.script = """
# ################################################################################
# apt install -y python python3 python3-pip
# # because there is no python-pip in apt now
# ### wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
# ### python2 /tmp/get-pip.py
# # python2 /tmp/get-pip.py
# ################################################################################
#         """
#
#     def do(self):
#         return SuperTask.run(self.script)
