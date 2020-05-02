#!/usr/bin/env python
# usage:


from __future__ import print_function
import os
from os import path

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
# 01 apt install <base: net-tools open-vm-tools openssh-server>
# 02 apt install <c-base: vim git build-essential cmake automake pkg-config>
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

    @staticmethod
    def action00_set_default():
        script = """
################################################################################
echo "set default"
systemctl set-default multi-user.target
################################################################################
"""
        return script

    @staticmethod
    def action01_create_user_admin():
        """ 如果uid=1000的用户不是admin，则删除再新建 """
        script = """
################################################################################
echo "create user admin"
userdel {username}
rm -rf /home/{username}
useradd -m -s /bin/bash -G sudo admin
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
    def action02_change_apt_source():
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
        script = """
################################################################################
echo "change apt source and update"
apt update
apt upgrade -y --fix-missing
################################################################################
"""
        return script

    @staticmethod
    def action03_apt_install_base():
        script = """
################################################################################
apt install -y net-tools open-vm-tools openssh-server zsh vim git
################################################################################
"""
        return script

    @staticmethod
    def action04_apt_install_c_base():
        script = """
################################################################################
apt install -y build-essential cmake automake musl-tools gcc-multilib g++-multilib pkg-config
################################################################################
"""
        return script

    @staticmethod
    def action05_apt_install_jdk():
        script = """
################################################################################
apt install -y openjdk-14-jdk
################################################################################
"""
        return script

    @staticmethod
    def action06_apt_install_php():
        script = """
################################################################################
apt install -y mariadb-server php php-mysql apache2
################################################################################
"""
        return script

    @staticmethod
    def action07_apt_install_golang():
        script = """
################################################################################
apt install -y golang
################################################################################
"""
        return script

    @staticmethod
    def action08_install_python():
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
python2 ./get-pip.py
################################################################################
"""
        return script


    @staticmethod
    def change_apt_source():
        SOURCES_LIST = """
deb https://mirrors.aliyun.com/kali kali-rolling main non-free contrib
deb-src https://mirrors.aliyun.com/kali kali-rolling main non-free contrib

# deb https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib
# deb-src https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib

# deb https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
# deb-src https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
"""

        softwares = dict(
            base="net-tools open-vm-tools openssh-server",
            dev="vim git build-essential cmake* automake* musl-tools* multiarch-support## gcc-multilib* g++-multilib*",
            php="mariadb-server* php php-mysql",
            python="python python3 python3-pip",  # python-pip 已经无法安装，请使用`get-pip.py`
            golang="golang",
            jdk="openjdk-14-jdk",
        )
        softwares = """
net-tools open-vm-tools openssh-server
libssl-dev
vim git build-essential cmake automake musl-tools multiarch-support gcc-multilib g++-multilib
mariadb-server mariadb-client php php-mysql
python python-pip python3 python3-pip
golang openjdk
"""
        sources_list = SOURCES_LIST.strip().encode()
        open("/etc/apt/sources.list", "wb").write(sources_list)
        script = """
apt update
apt upgrade -y --fix-missing
apt install {softwares}
systemctl stop nginx
systemctl disable nginx
systemctl stop apache2
systemctl disable apache2
systemctl stop mysql
systemctl disable mysql
systemctl enable ssh
systemctl start ssh
systemctl set-default multi-user.target
"""
        softwares = " ".join(softwares.split("\n"))

    @staticmethod
    def install_docker():
        pass

    @staticmethod
    def install_python_lib():
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
python2 -m pip install -U pip setuptools
python2 -m pip install pwntools
python2 -m pip unistall crypto pycrypto
python2 -m pip install pycrypto gmpy gmpy2
python3 -m pip install -U pip setuptools
python3 -m pip unistall crypto pycrypto
python3 -m pip install pycrypto gmpy gmpy2 uncompyle6 requests aiohttp lxml beautifulsoup4
"""

    @staticmethod
    def install_zsh():
        pass

    @staticmethod
    def install_ctf_tools():
        pass

    @staticmethod
    def install_rust():
        pass


def main():
    """

    """
    pass


if __name__ == "__main__":
    main()
