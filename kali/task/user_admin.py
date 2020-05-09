#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


class TaskAptInstallBase(SuperTask):
    def __init__(self):
        self.order = 7
        self.script_create_admin = """
################################################################################
echo "create user admin"
useradd -m -s /bin/zsh -G sudo admin
################################################################################
        """
        self.script_modify_password = """
################################################################################
echo admin:123 | chpasswd
################################################################################
        """
        self.script_create_work_dir = """
################################################################################
mkdir /home/app /home/src /home/ctf /home/ml /home/docker
chown admin:admin /home/app /home/src /home/ctf /home/ml /home/docker
################################################################################
        """

    def do(self):
        temp_user = self.user1000()
        if temp_user is None:
            ret = self.run(self.script_create_admin)
            if ret != 0:
                return ret
        elif temp_user != "admin":
            ret = self.replace(temp_user)
            if ret != 0:
                return ret
            ret = self.run("mv /home/{} /home/admin".format(temp_user))
            if ret != 0:
                return ret
        ret = self.run(self.script_modify_password)
        if ret != 0:
            return ret
        return SuperTask.run(self.script_create_work_dir)

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
