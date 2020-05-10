#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path


class DO(object):
    order = 9
    current_path = path.dirname(path.abspath(__file__))
    daemon_json = path.join(current_path, "daemon.json")
    script = """
################################################################################
# step 1: 安装必要的一些系统工具
apt -y update
apt -y install apt-transport-https ca-certificates curl software-properties-common
# step 2: 安装GPG证书
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
# Step 3: 写入软件源信息
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu eoan stable"
# Step 4: 更新并安装Docker-CE
apt -y update
apt -y install docker-ce
# Step 5: 配置
groupadd docker
usermod -aG docker admin
systemctl enable docker
systemctl start docker
cp {daemon_json} /etc/docker/daemon.json
################################################################################
    """.format(daemon_json=daemon_json)

    run = None
    print_notice = None
    print_error = None

    def __init__(self):
        pass

    @staticmethod
    def do(_):
        if not path.exists("/etc/docker"):
            os.makedirs("/etc/docker", 0o755)
        DO.run(DO.script)


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
    DO.run = SuperTask.run
    DO.print_notice = SuperTask.print_notice
    DO.print_error = SuperTask.print_error

    # 动态创建类
    TaskAptInstallDocker = type("TaskAptInstallDocker", (SuperTask,), dict(
        order=DO.order,
        do=DO.do,
    ))
else:
    DO.run = print
    DO.print_notice = print
    DO.print_error = print
    TaskAptInstallDocker = type("TaskAptInstallDocker", (object,), dict(
        order=DO.order,
        do=DO.do,
    ))


def main():
    task = TaskAptInstallDocker()
    task.do()


if __name__ == "__main__":
    main()
