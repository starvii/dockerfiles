#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from os import path


class Actor(object):
    name = "TaskInstallRust"
    order = 10
    current_path = path.dirname(path.abspath(__file__))
    install_sh = path.join(current_path, "rustup-init.sh")
    script_copy = """
################################################################################
cp {} /tmp/rust.sh
################################################################################
    """.strip().format(install_sh)
    script_download = """
################################################################################
wget https://sh.rustup.rs -O /tmp/rust.sh
################################################################################
    """
    script_install = """
################################################################################
sh /tmp/rust.sh -y
source $HOME/.cargo/env
################################################################################
    """.strip()

    def do(self):
        os.environ["RUSTUP_DIST_SERVER"] = "https://mirrors.ustc.edu.cn/rust-static"
        os.environ["RUSTUP_UPDATE_ROOT"] = "https://mirrors.ustc.edu.cn/rust-static/rustup"
        scripts = []
        if not path.exists("rustup-init.sh"):
            scripts.append(Actor.script_copy)
        else:
            scripts.append(Actor.script_download)
        script = "\n".join(scripts)
        self.func.run(script)
        print("# Notice: In product mode, script will modify /home/admin/.zshrc")
        try:
            home = os.environ.get("HOME")
            rc = open("{}/.zshrc".format(home), "rb").read()
            if b"source $HOME/.cargo/env" not in rc:
                rc += b"\nsource $HOME/.cargo/env\n"
                open("{}/.zshrc".format(home), "wb").write(rc)
        except Exception as e:
            self.func.print_error(e)

    def __init__(self, func=None):
        self.func = func


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    ATask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask


    class ProductFunc(object):  # delegate task actor
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


    def init_func(self): self.actor = Actor(ProductFunc)


    # 动态创建类
    _ = type(Actor.name, (ATask,), dict(
        __init__=init_func,
        order=Actor.order,
    ))


def main():
    class DebugFunc(object):  # default actor
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

    Actor(DebugFunc).do()


if __name__ == "__main__":
    main()
