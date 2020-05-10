#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os import path

INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


class TaskAptInstallBase(SuperTask):
    def __init__(self):
        self.order = 6
        self.pip_conf = """
[global]
index-url = https://mirrors.huaweicloud.com/repository/pypi/simple
trusted-host = mirrors.huaweicloud.com
timeout = 120
        """
        self.script = """
################################################################################
apt install -y python python3 python3-pip
# because there is no python-pip in apt now
### wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
### python2 /tmp/get-pip.py
# python2 /tmp/get-pip.py
################################################################################
        """
        self.script_lib = """
################################################################################
apt install -y libpython2-dev libpython3-all-dev libssl-dev libmpfr-dev libmpc-dev
python2 -m pip install -U pip setuptools
# it seems some dependencies of python2 are deprecated.
### python2 -m pip install -U pwntools
python2 -m pip uninstall crypto pycrypto
python2 -m pip install -U pycryptodome
python2 -m pip install -U gmpy
python2 -m pip install -U gmpy2
python2 -m pip install -U pwntools
python3 -m pip install -U pip setuptools
python3 -m pip uninstall crypto pycrypto
python3 -m pip install -U pycryptodome
python3 -m pip install -U gmpy
python3 -m pip install -U gmpy2
python3 -m pip install -U uncompyle6
python3 -m pip install -U pwntools
python3 -m pip install -U requests
python3 -m pip install -U aiohttp
python3 -m pip install -U lxml
python3 -m pip install -U beautifulsoup4
python3 -m pip install -U tornado
################################################################################
        """

    def do(self):
        try:
            if not path.isdir("/root/.pip"):
                os.makedirs("/root/.pip", 0o755)
            open("/root/.pip/pip.conf", "wb").write(self.pip_conf.strip().encode())
        except Exception as e:
            self.print_error(e)
        ret = self.run(self.script)
        if ret == 0:
            return ret
        ret = self.check_python_pip()
        if ret == 0:
            return ret
        ret = self.check_get_pip()
        if ret == 0:
            return ret
        cmd = "python2 /tmp/get-pip.py\nrm -rf /tmp/get-pip.py\n"
        ret = self.run(cmd)
        if ret == 0:
            return ret
        return self.run(self.script_lib)

    def check_python_pip(self):
        return self.run("apt install python-pip")

    def check_get_pip(self):
        if path.exists("{BASE}/_external_/get-pip.tgz".format(BASE=INIT_SCRIPT_BASE)):
            _c = "tar zxf {BASE}/_external_/get-pip.tgz -C /tmp".format(BASE=INIT_SCRIPT_BASE)
        else:
            _c = "wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py"
        return self.run(_c)
