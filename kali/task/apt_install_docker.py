#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json

INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


class TaskAptInstallBase(SuperTask):
    def __init__(self):
        self.order = 9
        self.script = """
################################################################################
curl -fsSL https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu/gpg | apt-key add - 
add-apt-repository "deb [arch=amd64] https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu focal stable"
apt update
apt install -y docker-ce
systemctl enable docker
systemctl start docker
groupadd docker
usermod -aG docker admin
################################################################################
        """

    def do(self):
        ret = self.run(self.script)
        if ret != 0:
            return ret
        try:
            c = {
                "registry-mirrors": [
                    "https://dockerhub.azk8s.cn",
                    "https://reg-mirror.qiniu.com",
                ]
            }
            c = json.dumps(c)
            open("/etc/docker/daemon.json", "wb").write(c.encode())
        except Exception as e:
            self.print_error(e)
            return -1
