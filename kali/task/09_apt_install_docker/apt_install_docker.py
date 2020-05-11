#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path


class _Actor(object):
    name = "TaskAptInstallDocker"
    order = 9
    current_path = path.dirname(path.abspath(__file__))
    daemon_json = path.join(current_path, "daemon.json")
    script = """
################################################################################
# step 1: base software
apt -y update
apt -y install apt-transport-https ca-certificates curl software-properties-common
# step 2: install gpg
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
# Step 3: apt sources
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu eoan stable"
# Step 4: install 
apt -y update
apt -y install docker-ce
# Step 5: config
groupadd docker
usermod -aG docker admin
systemctl enable docker
systemctl start docker
cp {daemon_json} /etc/docker/daemon.json
################################################################################
    """.strip().format(daemon_json=daemon_json)

    def do(self):
        if not path.exists("/etc/docker"):
            os.makedirs("/etc/docker", 0o755)
        return self.func.run(_Actor.script, False)

    def __init__(self, func=None):
        self.func = func


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    ATask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


    class _RealFunc(object):  # delegate task actor
        def __init__(self):
            pass

        @staticmethod
        def run(script, stop=True):
            ATask.run(script, stop)

        @staticmethod
        def print_notice(out):
            ATask.print_notice(out)

        @staticmethod
        def print_error(out):
            ATask.print_error(out)


    def init_func(self): self.actor = _Actor(_RealFunc)


    # 动态创建类
    _ = type(_Actor.name, (ATask,), dict(
        __init__=init_func,
        order=_Actor.order,
    ))


def main():
    class _FakeFunc(object):  # default actor
        def __init__(self):
            pass

        @staticmethod
        def run(script, _=True):
            print(script)

        @staticmethod
        def print_notice(out):
            print(out)

        @staticmethod
        def print_error(out):
            print(out)

    _Actor(_FakeFunc).do()


if __name__ == "__main__":
    main()
























#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path


class _Do(object):
    order = 9

    @staticmethod
    def run(script, _=True): print(script)

    @staticmethod
    def print_notice(out): print(out)

    @staticmethod
    def print_error(out): print(out)

    def __init__(self):
        self.current_path = path.dirname(path.abspath(__file__))
        self.daemon_json = path.join(self.current_path, "daemon.json")
        self.script = """
################################################################################
# step 1: base software
apt -y update
apt -y install apt-transport-https ca-certificates curl software-properties-common
# step 2: install gpg
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
# Step 3: apt sources
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu eoan stable"
# Step 4: install 
apt -y update
apt -y install docker-ce
# Step 5: config
groupadd docker
usermod -aG docker admin
systemctl enable docker
systemctl start docker
cp {daemon_json} /etc/docker/daemon.json
################################################################################
        """.strip().format(daemon_json=self.daemon_json)

    def do(self):
        if not path.exists("/etc/docker"):
            os.makedirs("/etc/docker", 0o755)
        _Do.run(self.script, False)


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    mod = __import__("task".format(INIT_SCRIPT_BASE))
    SuperTask = mod.AbstractTask
    _Do.run = mod.run
    _Do.print_notice = mod.print_notice
    _Do.print_error = mod.print_error


    def init_func(self): self._action = _Do()

    # 动态创建类
    _ = type("TaskAptInstallDocker", (SuperTask,), dict(
        order=_Do.order,
        __init__=init_func
    ))


def main():
    action = _Do()
    action.do()


if __name__ == "__main__":
    main()
