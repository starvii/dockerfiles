# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
# from __future__ import print_function
# import base64
# import json
# import os
# from os import path
#
# BASE = path.dirname(path.dirname(path.abspath(__file__)))
#
#
# class Detect:
#     @staticmethod
#     def bash():
#         """ 检测bash是否存在。已无必要，因为不需要使用echo -e功能 """
#         return path.exists("/bin/bash")
#
#     @staticmethod
#     def user_root():
#         """ 检测当前用户是否为root """
#         return 0 == os.getuid()
#
#     @staticmethod
#     def user1000():
#         """ uid == 1000 的用户的用户名 """
#         lines = open("/etc/passwd", "rb").readlines()
#         lines = [line.strip() for line in lines if b"x:1000:1000:" in line]
#         if len(lines) == 0:
#             return None
#         username = lines[0].split(b":")[0].decode()
#         return username
#
#
# class Script:
#     DATA_SOURCES_LIST = """
# deb https://mirrors.aliyun.com/kali kali-rolling main non-free contrib
# deb-src https://mirrors.aliyun.com/kali kali-rolling main non-free contrib
#
# # deb https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib
# # deb-src https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib
#
# # deb https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
# # deb-src https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
#     """
#     ACTION_CHANGE_APT_SOURCE = """
# ################################################################################
# echo "change apt source and update"
# apt update
# apt upgrade -y --fix-missing
# ################################################################################
#     """
#     ACTION_APT_INSTALL_BASE = """
# ################################################################################
# apt install -y net-tools open-vm-tools openssh-server
# apt install -y zsh vim git wget curl pkg-config aria2
# ################################################################################
#     """
#     ACTION_APT_INSTALL_C_BASE = """
# ################################################################################
# apt install -y build-essential cmake automake
# apt install -y musl-tools gcc-multilib g++-multilib
# ################################################################################
#     """
#     ACTION_APT_INSTALL_JDK = """
# ################################################################################
# apt install -y openjdk-14-jdk
# ################################################################################
#     """
#     ACTION_APT_INSTALL_PHP = """
# ################################################################################
# apt install -y mariadb-server php php-mysql apache2
# ################################################################################
#     """
#     ACTION_APT_INSTALL_GO = """
# ################################################################################
# apt install -y golang
# ################################################################################
#     """
#     DATA_PIP_CONF = """
# [global]
# index-url = https://mirrors.huaweicloud.com/repository/pypi/simple
# trusted-host = mirrors.huaweicloud.com
# timeout = 120
#     """
#     ACTION_INSTALL_PYTHON = """
# ################################################################################
# apt install -y python python3 python3-pip
# # because there is no python-pip in apt now
# ### wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
# ### python2 /tmp/get-pip.py
# python2 ../.external/get-pip.py
# ################################################################################
#     """
#     ACTION_PIP_INSTALL_PYTHON_LIB = """
# ################################################################################
# apt install -y libpython-dev libssl-dev libmpfr-dev libmpc-dev
# python2 -m pip install -U pip setuptools
# # it seems some dependencies of python2 are deprecated.
# ### python2 -m pip install -U pwntools
# python2 -m pip uninstall crypto pycrypto
# python2 -m pip install -U pycrypto gmpy
# python3 -m pip install -U pip setuptools
# python3 -m pip uninstall crypto pycrypto
# python3 -m pip install -U pycrypto gmpy2 uncompyle6 pwntools
# python3 -m pip install -U requests aiohttp lxml beautifulsoup4 tornado
# ################################################################################
#     """
#     ACTION_CREATE_ADMIN = """
# ################################################################################
# echo "create user admin"
# useradd -m -s /bin/zsh -G sudo admin
# ################################################################################
#     """
#     ACTION_MODIFY_ADMIN = """
# ################################################################################
# echo admin:123 | chpasswd
# ################################################################################
#     """
#     ACTION_CREATE_WORK_DIR = """
# ################################################################################
# mkdir /home/app /home/src /home/ctf /home/ml /home/docker
# chown admin:admin /home/app /home/src /home/ctf /home/ml /home/docker
# ################################################################################
#     """
#     ACTION_INSTALL_OH_MY_ZSH = """
# ################################################################################
# # wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O /tmp/omz.sh
# # su - admin -c "sh /tmp/omz.sh"
# su - admin -c "{BASE}/.external/oh_my_zsh.sh"
# ################################################################################
#     """
#     ACTION_CONFIG_SYSTEM = """
# ################################################################################
# systemctl stop nginx
# systemctl disable nginx
# systemctl stop apache2
# systemctl disable apache2
# systemctl stop mysql
# systemctl disable mysql
# systemctl enable ssh
# systemctl start ssh
# systemctl set-default multi-user.target
# ################################################################################
#     """
#     ACTION_INSTALL_DOCKER = """
# ################################################################################
# curl -fsSL https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu/gpg | apt-key add -
# add-apt-repository "deb [arch=amd64] https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu focal stable"
# apt update
# apt install -y docker-ce
# systemctl enable docker
# systemctl start docker
# groupadd docker
# usermod -aG docker admin
# ################################################################################
#     """
#     ACTION_INSTALL_CTF_TOOLS = """
# ################################################################################
# su - admin -c "python {BASE}/.external/ctf-tools-setup.py"
# ################################################################################
#     """
#     ACTION_INSTALL_RUST = """
# ################################################################################
# su - admin -c "python {BASE}/.external/rust-setup.py"
# ################################################################################
#     """
#     ACTION_INSTALL_IDA = """
# ################################################################################
# su - admin -c "mkdir /home/app/ida -p"
# su - admin -c "cp {BASE}/.external/ida/* /home/app/ida"
# su - admin -c "chmod 755 /home/app/ida/*"
# ################################################################################
#     """
#
#     @staticmethod
#     def run(script, filename=None):
#         lines = script.split("\n")
#         buffer = []
#         first = True
#         for line in lines:
#             ls = line.strip()
#             if len(ls) == 0:
#                 buffer.append("\n" + line)
#             elif ls.startswith("#"):
#                 buffer.append("\n" + line)
#             elif first:
#                 first = False
#                 buffer.append("\n" + line)
#             else:
#                 buffer.append(" \\\n&& " + line)
#         shell_script = "".join(buffer)
#         if filename is None:
#             filename = "/tmp/" + base64.b32encode(os.urandom(10)).decode().lower() + ".sh"
#         print(filename)
#         open(filename, "wb").write(shell_script.encode().strip() + b"\n\n")
#         os.system("cat {}".format(filename))
#         ret = os.system("sh {}".format(filename))
#         ### os.system("rm -rf {}".format(filename))
#         return ret
#
#
# class Action:
#     # 00 change apt source & apt update & apt upgrade -y
#     # 01 apt install <base: net-tools open-vm-tools openssh-server vim git pkg-config>
#     # 02 apt install <c-base: build-essential cmake automake>
#     # 03 apt install <jdk11>
#     # 04 apt install <php-base>
#     # 05 apt install <golang>
#     # 06 apt install <python: change pipy source and *python2-pip>
#     # 07 python lib:
#     # 08 apt install zsh and oh-my-zsh
#     # 09 create admin user
#     # 10 config system
#     # 11 docker
#     # 12 ctf-tools
#     # 13 rust
#     # 14 ida
#     # 15 other tools
#     #
#     # c00 config_zsh
#     # c01 config_docker
#
#     @staticmethod
#     def a00_change_apt_source():
#         try:
#             sources_list = Script.DATA_SOURCES_LIST.strip().encode()
#             open("/etc/apt/sources.list", "wb").write(sources_list)
#             return Script.run(Script.ACTION_CHANGE_APT_SOURCE)
#         except Exception as e:
#             print(e)
#             return -1
#
#     @staticmethod
#     def a01_apt_install_base():
#         return Script.run(Script.ACTION_APT_INSTALL_BASE)
#
#     @staticmethod
#     def a02_apt_install_c_base():
#         return Script.run(Script.ACTION_APT_INSTALL_C_BASE)
#
#     @staticmethod
#     def a03_apt_install_jdk():
#         return Script.run(Script.ACTION_APT_INSTALL_JDK)
#
#     @staticmethod
#     def a04_apt_install_php():
#         return Script.run(Script.ACTION_APT_INSTALL_PHP)
#
#     @staticmethod
#     def a05_apt_install_go():
#         return Script.run(Script.ACTION_APT_INSTALL_GO)
#
#     @staticmethod
#     def a06_install_python():
#         try:
#             os.makedirs("/root/.pip", 0o755)
#             open("/root/.pip/pip.conf", "wb").write(Script.DATA_PIP_CONF.strip().encode())
#         except Exception as e:
#             print(e)
#             return -1
#         try:
#             os.makedirs("/home/admin/.pip", 0o755)
#             os.chown("/home/admin/.pip", 1000, 1000)
#             open("/home/admin/.pip/pip.conf", "wb").write(Script.DATA_PIP_CONF.strip().encode())
#         except Exception as e:
#             print(e)
#             return -1
#         return Script.run(Script.ACTION_INSTALL_PYTHON)
#
#     @staticmethod
#     def a07_install_py_lib():
#         return Script.run(Script.ACTION_PIP_INSTALL_PYTHON_LIB)
#
#     @staticmethod
#     def a08_user_admin():
#         """ 如果uid=1000的用户不是admin，则直接替换用户名 """
#         def replace(old_name):
#             try:
#                 on = old_name.strip().encode()
#                 prefix = "{}:x:1000:1000:".format(old_name.strip()).encode()
#                 lines = open("/etc/passwd", "rb").readlines()
#                 buffer = []
#                 for line in lines:
#                     pl = line
#                     if prefix in line:
#                         pl = b"admin:x:1000:1000::/home/admin:/bin/zsh\n"
#                     buffer.append(pl)
#                 open("/etc/passwd", "wb").writelines(buffer)
#                 lines = open("/etc/group", "rb").readlines()
#                 buffer = []
#                 for line in lines:
#                     gl = line
#                     a = line.split(b":")
#                     if len(a) == 4:
#                         b = a[3].split(b",")
#                         bs = [x.strip() for x in b]
#                         if on in bs:
#                             idx = bs.index(on)
#                             b[idx] = b"admin"
#                             a[3] = b",".join(b)
#                             gl = b":".join(a)
#                     buffer.append(gl)
#                 open("/etc/group", "wb").writelines(buffer)
#             except Exception as e:
#                 print(e)
#                 return -1
#             return 1
#
#         username = Detect.user1000()
#         if username is None:
#             ret = Script.run(Script.ACTION_CREATE_ADMIN) >= 0
#             if ret <= 0:
#                 return ret
#         elif username != "admin":
#             ret = replace(username)
#             if ret <= 0:
#                 return ret
#         ret = Script.run(Script.ACTION_MODIFY_ADMIN)
#         if ret <= 0:
#             return ret
#         return Script.run(Script.ACTION_CREATE_WORK_DIR)
#
#     @staticmethod
#     def a09_install_oh_my_zsh():
#         rc = "/home/admin/.zshrc"
#         ret = Script.run(Script.ACTION_INSTALL_OH_MY_ZSH.format(BASE=BASE))
#         try:
#             if ret >= 0:
#                 z = open(rc, "rb").read().decode()
#                 if "umask 022" not in z:
#                     z += "\n\nunsetopt share_history\nunsetopt inc_append_history\numask 022\n"
#                 open(rc, "w").write(z)
#         except Exception as e:
#             print(e)
#             return -1
#         return ret
#
#     @staticmethod
#     def a10_config_system():
#         return Script.run(Script.ACTION_CONFIG_SYSTEM)
#
#     @staticmethod
#     def a11_install_docker():
#         ret = Script.run(Script.ACTION_INSTALL_DOCKER)
#         if ret >= 0:
#             try:
#                 c = {
#                     "registry-mirrors": [
#                         "https://dockerhub.azk8s.cn",
#                         "https://reg-mirror.qiniu.com",
#                     ]
#                 }
#                 c = json.dumps(c)
#                 open("/etc/docker/daemon.json", "wb").write(c.encode())
#             except Exception as e:
#                 print(e)
#                 return -1
#         return ret
#
#     @staticmethod
#     def a12_install_ctf_tools():
#         script = Script.ACTION_INSTALL_CTF_TOOLS.format(BASE=BASE)
#         return Script.run(script)
#
#     @staticmethod
#     def a13_install_rust():
#         script = Script.ACTION_INSTALL_RUST.format(BASE=BASE)
#         return Script.run(script)
#
#     @staticmethod
#     def a14_install_ida():
#         script = Script.ACTION_INSTALL_IDA.format(BASE=BASE)
#         return Script.run(script)
#
#     @staticmethod
#     def a15_install_other():
#         return 0
#
#
# def main():
#     actions = (
#         Action.a00_change_apt_source,
#         Action.a01_apt_install_base,
#         Action.a02_apt_install_c_base,
#         Action.a03_apt_install_jdk,
#         Action.a04_apt_install_php,
#         Action.a05_apt_install_go,
#         Action.a06_install_python,
#         Action.a07_install_py_lib,
#         Action.a08_user_admin,
#         Action.a09_install_oh_my_zsh,
#         Action.a10_config_system,
#         Action.a11_install_docker,
#         Action.a12_install_ctf_tools,
#         Action.a13_install_rust,
#         Action.a14_install_ida,
#         Action.a15_install_other,
#     )
#     # actions[0]()
#     # actions[1]()
#     actions[2]()
#
#
# if __name__ == "__main__":
#     main()
