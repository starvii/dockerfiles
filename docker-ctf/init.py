#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os


class Init(object):
    script = r"""
mkdir -p /root/.pip
bash -c "echo -e '[global]\nindex-url=https://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted-host=mirrors.aliyun.com'>/root/.pip/pip.conf"
dpkg --add-architecture i386
apt update -y
apt upgrade -y
apt install -y --fix-missing libc6:i386 libc6-dbg:i386 libc6-dbg lib32stdc++6 g++-multilib gcc-multilib multiarch-support cmake ipython3 vim net-tools iputils-ping libffi-dev libssl-dev python-pip python3-dev python3-pip python3-distutils build-essential ruby ruby-dev tmux strace ltrace nasm wget radare2 gdb gdb-multiarch netcat socat git patchelf gawk file bison curl wget netcat sudo zsh openssh-server
rm -rf /var/lib/apt/list/*
python3 -m pip install -U pip setuptools -i https://mirrors.aliyun.com/pypi/simple
python3 -m pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple ropgadget pwntools z3-solver smmap2 apscheduler ropper unicorn keystone-engine capstone angr pebble
gem install one_gadget seccomp-tools
rm -rf /var/lib/gems/2.*/cache/*
useradd -m -u 1000 -G sudo -s /bin/bash admin
echo admin:123 | chpasswd
bash -c "echo -e '\numask 022\n'>>/home/admin/.bashrc"
mkdir -p /home/ctf /home/app
chown admin:admin /home/ctf /home/app

git clone --depth 1 https://github.com/pwndbg/pwndbg /home/app/pwndbg
cd /home/app/pwndbg/ && bash /home/app/pwndbg/setup.sh && cd ~
git clone --depth 1 https://github.com/scwuaptx/Pwngdb.git /home/app/pwngdb
cat /home/app/pwngdb/.gdbinit >> /home/admin/.gdbinit
git clone --depth 1 https://github.com/niklasb/libc-database.git /home/app/libc-database
    """.strip()

    @staticmethod
    def init():
        scripts = Init.script.split("\n")
        for script in scripts:
            ln = script.strip()
            print(ln)
            if len(ln) > 0 and not ln.startswith("#"):
                ret = os.system(ln)
                if ret != 0:
                    print("ret = {}".format(ret))
                    print(ln)
                    print("press any key to continue ...")
                    _ = input()


if __name__ == "__main__":
    Init.init()
