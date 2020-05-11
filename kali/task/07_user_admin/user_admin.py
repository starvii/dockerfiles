#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path


class _Actor(object):
    name = "TaskUserAdmin"
    order = 7
    script_create_admin = """
################################################################################
useradd -s /bin/zsh -G sudo admin
################################################################################
    """.strip()
    script_create_home = """
################################################################################
mkdir -p /home/admin
chmod 700 /home/admin
chown admin:admin /home/admin
################################################################################
    """.strip()
    script_modify_password = """
################################################################################
echo admin:123 | chpasswd
################################################################################
    """.strip()
    script_create_work_dir = """
################################################################################
mkdir /home/app /home/src /home/ctf /home/ml /home/docker
chown admin:admin /home/app /home/src /home/ctf /home/ml /home/docker
################################################################################
    """.strip()
    script = """
################################################################################
apt install -y mariadb-server php php-mysql apache2
systemctl stop nginx
systemctl disable nginx
systemctl stop apache2
systemctl disable apache2
systemctl stop mysql
systemctl disable mysql
# TODO: change mariadb password
################################################################################
    """.strip()

    def do(self):
        scripts = []
        temp_user = _Actor.user1000()
        if temp_user is None:
            scripts.append(_Actor.script_create_admin)
        elif temp_user != "admin":
            self.replace(temp_user)
        if not path.exists("/home/admin"):
            scripts.append(_Actor.script_create_home)
        scripts.append(_Actor.script_modify_password)
        scripts.append(_Actor.script_create_work_dir)
        script = "\n\n".join(scripts)
        return self.func.run(script, False)

    @staticmethod
    def user1000():
        """ uid == 1000 的用户的用户名 """
        lines = open("/etc/passwd", "rb").readlines()
        lines = [line.strip() for line in lines if b"x:1000:1000:" in line]
        if len(lines) == 0:
            return None
        username = lines[0].split(b":")[0].decode()
        return username

    def replace(self, temp_user):
        try:
            tu = temp_user.strip().encode()
            prefix = "{}:x:1000:1000:".format(temp_user.strip()).encode()
            lines = open("/etc/passwd", "rb").readlines()
            buffer = []
            for line in lines:
                pl = line
                if prefix in line:
                    pl = b"admin:x:1000:1000::/home/admin:/bin/zsh\n"
                buffer.append(pl)
            open("/etc/passwd", "wb").writelines(buffer)
            lines = open("/etc/group", "rb").readlines()
            buffer = []
            for line in lines:
                gl = line.strip()
                a = line.split(b":")
                if len(a) == 4:
                    if a[0].strip() == tu:
                        a[0] = b"admin"
                        gl = b":".join(a)
                    else:
                        b = a[3].split(b",")
                        bs = [x.strip() for x in b]
                        if tu in bs:
                            idx = bs.index(tu)
                            b[idx] = b"admin"
                            a[3] = b",".join(b)
                            gl = b":".join(a)
                buffer.append(gl + b"\n")
            open("/etc/group", "wb").writelines(buffer)
        except Exception as e:
            self.func.print_error(e)
            return -1
        return 0

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
