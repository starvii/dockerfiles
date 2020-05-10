#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys


class _Do(object):
    order = 7

    @staticmethod
    def run(script, _=True): print(script)
    print_notice = print
    print_error = print

    def __init__(self):
        self.script_create_admin = """
################################################################################
useradd -m -s /bin/zsh -G sudo admin
################################################################################
        """.strip()
        self.script_move_admin = """
################################################################################
mv /home/{temp_user} /home/admin
################################################################################
        """.strip()
        self.script_modify_password = """
################################################################################
echo admin:123 | chpasswd
################################################################################
        """.strip()
        self.script_create_work_dir = """
################################################################################
mkdir /home/app /home/src /home/ctf /home/ml /home/docker
chown admin:admin /home/app /home/src /home/ctf /home/ml /home/docker
################################################################################
        """.strip()


        self.script = """
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
        script = ""
        temp_user = _Do.user1000()
        if temp_user is None:
            script += self.script_create_admin
        elif temp_user != "admin":
            _Do.replace(temp_user)
            script += self.script_move_admin.format(temp_user=temp_user)
        script += self.script_modify_password
        script += self.script_create_work_dir
        _Do.run(script)

    @staticmethod
    def user1000():
        """ uid == 1000 的用户的用户名 """
        lines = open("/etc/passwd", "rb").readlines()
        lines = [line.strip() for line in lines if b"x:1000:1000:" in line]
        if len(lines) == 0:
            return None
        username = lines[0].split(b":")[0].decode()
        return username

    @staticmethod
    def replace(temp_user):
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
            SuperTask.print_error(e)
            return -1
        return 0


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
    def init_func(self): self._action = _Do()
    _Do.run = SuperTask.run
    _Do.print_notice = SuperTask.print_notice
    _Do.print_error = SuperTask.print_error

    # 动态创建类
    _ = type("TaskUserAdmin", (SuperTask,), dict(
        order=_Do.order,
        __init__=init_func
    ))


def main():
    action = _Do()
    action.do()


if __name__ == "__main__":
    main()
