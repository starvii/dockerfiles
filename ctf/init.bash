#!/bin/bash

DOCKER_USER="admin"
DOCKER_UID="1000"
DOCKER_PASSWD="123"
DOCKER_SHRC="/home/${DOCKER_USER}/.bashrc"
DOCKER_SHARE="/home/ctf"
DOCKER_PORT="1122"

cp /etc/apt/sources.list /etc/apt/sources.list~ \
&& echo "更新系统" \
&& sed -i "s@http://deb.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
&& sed -i "s@http://security.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
&& apt update \
&& apt install -y apt-transport-https ca-certificates \
&& sed -i 's@http://@https://@g' /etc/apt/sources.list \
&& apt update \
&& apt upgrade -y \
&& echo "安装基础组件" \
&& apt install -y git vim build-essential gdb cmake python-pip python3-pip curl wget netcat sudo net-tools zsh \
&& echo "安装ctf基础组件" \
&& apt install -y binwalk rlwrap socat libgmp-dev libmpc-dev libmpfr-dev rubygems \
&& echo "安装x86支持" \
&& dpkg --add-architecture i386 \
&& apt install -y gcc-multilib g++-multilib multiarch-support \
&& echo "安装sshd" \
&& apt install -y openssh-server \
&& systemctl enable ssh \
&& echo "建立常规用户" \
&& useradd -m -u ${DOCKER_UID} -G sudo -s /bin/bash ${DOCKER_USER} \
&& echo ${DOCKER_USER}:${DOCKER_PASSWD} | chpasswd \
&& bash -c 'echo -e "\numask 022\n" >> ${DOCKER_SHRC}' \
&& echo "建立应用程序目录与共享目录" \
&& mkdir -p ${DOCKER_SHARE} /home/app \
&& chown ${DOCKER_USER}:${DOCKER_USER} ${DOCKER_SHARE} /home/app \
&& echo "配置PIP源" \
&& mkdir -p /etc/pip \
&& bash -c "echo -e '[global]\nindex-url=https://mirrors.huaweicloud.com/repository/pypi/simple\ntrusted-host=mirrors.huaweicloud.com\ntimeout=120' > /etc/pip/pip.conf" \
&& ln -s /etc/pip ${HOME}/.pip \
&& ln -s /etc/pip ${DOCKER_HOME}/.pip \
&& echo "安装python模块" \
&& python2 -m pip uninstall -y pycrypto crypto \
&& python3 -m pip uninstall -y pycrypto crypto \
&& python2 -m pip install -U pip setuptools pwntools pycrypto gmpy gmpy2 \
&& python3 -m pip install -U pip setuptools pycrypto gmpy gmpy2 uncompyle6 \
# 配置ctf-tools
# dirsearch
&& su - admin -c "git clone https://github.com/zardus/ctf-tools.git /home/app/ctf-tools" \
&& su - admin -c "/home/app/ctf-tools/dirsearch/install" \
&& ln -s /home/app/ctf-tools/dirsearch/bin/dirsearch.py /usr/bin/dirsearch \
# one_gadget（rubygems）
&& su - admin -c "/home/app/ctf-tools/one_gadget/install" \
&& ln -s /home/admin/.gem/ruby/2.5.0/bin/one_gadget /usr/bin/one_gadget \
# peda
&& su - admin -c "/home/app/ctf-tools/peda/install" \
# pwndbg
&& su - admin -c "/home/app/ctf-tools/pwndbg/install"
# rp++
# yafu
# zsteg

    # # 其他一些工具
    # && su - admin -c "git clone --depth 1 https://github.com/inaz2/roputils.git /home/app/roputils" \
    # # TODO: 需要配置
    # && su - admin -c "git clone --depth 1 https://github.com/iagox86/hash_extender.git /home/app/hash_extender" \
    # # TODO: 需要编译
    # && su - admin -c "git clone --depth 1 https://github.com/livz/cloacked-pixel.git /home/app/cloacked-pixel" \
    # # TODO: 需要安装依赖
    # && su - admin -c "git clone --depth 1 https://github.com/theonlypwner/crc32.git /home/app/crc32" \
    # && su - admin -c "git clone --depth 1 https://github.com/lijiejie/GitHack.git /home/app/GitHack" \
    # && su - admin -c "git clone --depth 1 https://github.com/scwuaptx/Pwngdb.git /home/app/Pwngdb" \
    # # TODO: 需要配置
    # && su - admin -c "git clone --depth 1 https://github.com/lieanu/LibcSearcher.git /home/app/LibcSearcher" \
    # # TODO: 需要安装
    # && su - admin -c "git clone --depth 1 https://github.com/ius/rsatool.git /home/app/rsatool" \
    # && su - admin -c "git clone --depth 1 https://github.com/tarunkant/Gopherus.git /home/app/Gopherus" \
    # && su - admin -c "git clone --depth 1 https://github.com/pablocelayes/rsa-wiener-attack.git /home/app/rsa-wiener-attack" \
    # && su - admin -c "git clone --depth 1 https://github.com/yangyangwithgnu/bypass_disablefunc_via_LD_PRELOAD.git /home/app/bypass_disablefunc_via_LD_PRELOAD"