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
    print_notice = print
    print_error = print

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
    SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
    def init_func(self): self._action = _Do()
    _Do.run = SuperTask.run
    _Do.print_notice = SuperTask.print_notice
    _Do.print_error = SuperTask.print_error

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
