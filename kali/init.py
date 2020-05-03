#!/usr/bin/env python
# -*- coding: utf-8 -*-
# usage:


from __future__ import print_function
import os
from os import path
import json
import base64
import hashlib

class Check:
    @staticmethod
    def bash():
        """ 检测bash是否存在。已无必要，因为不需要使用echo -e功能 """
        return path.exists("/bin/bash")

    @staticmethod
    def user_root():
        """ 检测当前用户是否为root """
        return 0 == os.getuid()

    @staticmethod
    def user1000():
        """ uid == 1000 的用户的用户名 """
        lines = open("/etc/passwd", "rb").readlines()
        lines = [line.strip() for line in lines if b"x:1000:1000:" in line]
        assert len(lines) == 1
        username = lines[0].split(b":")[0].decode()
        return username


class Action:
# 00 change apt source & apt update & apt upgrade -y
# 01 apt install <base: net-tools open-vm-tools openssh-server vim git pkg-config>
# 02 apt install <c-base: build-essential cmake automake>
# 03 apt install <jdk11>
# 04 apt install <php-base>
# 05 apt install <golang>
# 06 apt install <python: change pipy source and *python2-pip>
# 07 python lib: 
# 08 apt install zsh and oh-my-zsh
# 09 create admin user
# 10 config system
# 11 docker
# 12 ctf-tools
# 13 rust
# 14 ida
# 15 other tools
# 
# c00 config_zsh
# c01 config_docker

    @staticmethod
    def a00_change_apt_source():
        try:
            SOURCES_LIST = """
    deb https://mirrors.aliyun.com/kali kali-rolling main non-free contrib
    deb-src https://mirrors.aliyun.com/kali kali-rolling main non-free contrib

    # deb https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib
    # deb-src https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib

    # deb https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
    # deb-src https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
    """
            sources_list = SOURCES_LIST.strip().encode()
            open("/etc/apt/sources.list", "wb").write(sources_list)
        except Exception as e:
            print(e)
        script = """
################################################################################
echo "change apt source and update"
apt update
apt upgrade -y --fix-missing
################################################################################
"""
        return script

    @staticmethod
    def a01_apt_install_base():
        script = """
################################################################################
apt install -y net-tools open-vm-tools openssh-server
apt install -y zsh vim git wget curl pkg-config aria2c
################################################################################
"""
        return script

    @staticmethod
    def a02_apt_install_c_base():
        script = """
################################################################################
apt install -y build-essential cmake automake
apt install -y musl-tools gcc-multilib g++-multilib
################################################################################
"""
        return script

    @staticmethod
    def a03_apt_install_jdk():
        script = """
################################################################################
apt install -y openjdk-14-jdk
################################################################################
"""
        return script

    @staticmethod
    def a04_apt_install_php():
        script = """
################################################################################
apt install -y mariadb-server php php-mysql apache2
################################################################################
"""
        return script

    @staticmethod
    def a05_apt_install_golang():
        script = """
################################################################################
apt install -y golang
################################################################################
"""
        return script

    @staticmethod
    def a06_install_python():
        pip_conf = """
[global]
index-url = https://mirrors.huaweicloud.com/repository/pypi/simple
trusted-host = mirrors.huaweicloud.com
timeout = 120
"""
        os.makedirs("/root/.pip", 0o755)
        os.makedirs("/home/admin/.pip", 0o755)
        os.chown("/home/admin/.pip", 1000, 1000)
        open("/root/.pip/pip.conf", "wb").write(pip_conf.strip().encode())
        open("/home/admin/.pip/pip.conf", "wb").write(pip_conf.strip().encode())
        script = """
################################################################################
apt install -y python python3 python3-pip
# wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
# python2 /tmp/get-pip.py
python2 ../.external/get-pip.py
################################################################################
"""
        return script

    @staticmethod
    def a07_install_py_lib():
        script = """
################################################################################
apt install -y libpython-dev libssl-dev libmpfr-dev libmpc-dev
python2 -m pip install -U pip setuptools
# python2 -m pip install -U pwntools
python2 -m pip uninstall crypto pycrypto
python2 -m pip install -U pycrypto gmpy
python3 -m pip install -U pip setuptools
python3 -m pip uninstall crypto pycrypto
python3 -m pip install -U pycrypto gmpy2 uncompyle6 pwntools
python3 -m pip install -U requests aiohttp lxml beautifulsoup4 tornado
################################################################################
"""
        return script

    @staticmethod
    def a08_create_user_admin():
        """ 如果uid=1000的用户不是admin，则删除再新建 """
        script = """
################################################################################
echo "create user admin"
userdel {username}
rm -rf /home/{username}
useradd -m -s /bin/zsh -G sudo admin
echo admin:123 | chpasswd
mkdir /home/app /home/src /home/ctf /home/ml /home/docker
chown admin:admin /home/app /home/src /home/ctf /home/ml /home/docker
################################################################################
"""
        username = Check.username()
        if username != "admin":
            return ""
        else:
            return script.format(username=username)

    @staticmethod
    def a09_install_oh_my_zsh():
        script = """
################################################################################
wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O /tmp/omz.sh
su - admin -c "sh /tmp/omz.sh"
################################################################################
"""
        # TODO: config ~/.zshrc
        return script

    @staticmethod
    def a10_config_system():
        script = """
################################################################################
systemctl stop nginx
systemctl disable nginx
systemctl stop apache2
systemctl disable apache2
systemctl stop mysql
systemctl disable mysql
systemctl enable ssh
systemctl start ssh
systemctl set-default multi-user.target
################################################################################
"""
        return script


    @staticmethod
    def a11_install_docker():
        script = """
################################################################################
curl -fsSL https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu/gpg | apt-key add - 
add-apt-repository "deb [arch=amd64] https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu focal stable"
systemctl enable docker
systemctl start docker
groupadd docker
usermod -aG docker admin
################################################################################
"""
        # TODO: config docker mirrors
        return script


    @staticmethod
    def a12_install_ctf_tools():
        script = """
################################################################################
su - admin -c "python ../.external/ctf-tools-setup.py"
################################################################################
"""
        return script


    @staticmethod
    def a13_install_rust():
        script = """
################################################################################
su - admin -c "python ../.external/rust-setup.py"
################################################################################
"""
        return script

    @staticmethod
    def a14_install_ida():
        script = """
################################################################################
su - admin -c "mkdir /home/app/ida -p"
su - admin -c "cp ../.external/ida/* /home/app/ida"
su - admin -c "chmod 755 /home/app/ida/*"
################################################################################
"""
        return script

    @staticmethod
    def a15_install_other():
        return ""


class Config:
    @staticmethod
    def c00_config_zsh():
        p = "/home/admin/.zshrc"
        c = open(p, "rb").read()
        if b"share_history" in c and b"inc_append_history" in c:
            return
        c += b"\n\nunsetopt share_history\nunsetopt inc_append_history\numask 022\n"
        open(p, "wb").write(c)


    @staticmethod
    def c01_config_docker():
        c = {
            "registry-mirrors": [
                "https://dockerhub.azk8s.cn",
                "https://reg-mirror.qiniu.com",
            ]
        }
        c = json.dumps(c)
        open("/etc/docker/daemon.json", "wb").write(c)


def to_shell_script(script, filename=None):
    lines = script.split("\n")
    buffer = []
    first = True
    for line in lines:
        l = line.strip()
        if len(l) == 0:
            buffer.append("\n" + line)
        elif l.startswith("#"):
            buffer.append("\n" + line)
        elif first:
            first = False
            buffer.append("\n" + line)
        else:
            buffer.append(" \\\n&& " + line)
    shell_script = "".join(buffer)
    if filename is None:
        filename = "/tmp/" + base64.b32encode(os.urandom(10)).decode().lower() + ".sh"
    print(filename)
    open(filename, "wb").write(shell_script.encode().strip())
    # os.system("sh {filename}".format(filename=filename))
    # os.system("rm -rf {filename}".format(filename=filename))

def main():
    actions = (
        Action.a00_change_apt_source,
        Action.a01_apt_install_base,
        Action.a02_apt_install_c_base,
        Action.a03_apt_install_jdk,
        Action.a04_apt_install_php,
        Action.a05_apt_install_golang,
        Action.a06_install_python,
        Action.a07_install_py_lib,
        Action.a08_create_user_admin,
        Action.a09_install_oh_my_zsh,
        Action.a10_config_system,
        Action.a11_install_docker,
        Action.a12_install_ctf_tools,
        Action.a13_install_rust,
        Action.a14_install_ida,
        Action.a15_install_other,
    )
    configs = (
        Config.c00_config_zsh,
        Config.c01_config_docker,
    )
    to_shell_script(Action.a00_change_apt_source())


if __name__ == "__main__":
    main()
