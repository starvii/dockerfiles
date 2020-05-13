#!/bin/bash

cp /etc/apt/sources.list /etc/apt/sources.list~


echo -e "deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse\n\ndeb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse\n\ndeb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse\n\ndeb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse\n\ndeb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse">/etc/apt/sources.list \
&& dpkg --add-architecture i386 \
&& apt update -y \
&& apt upgrade -y \
&& apt install -y  --fix-missing \
    libc6:i386 \
    libc6-dbg:i386 \
    libc6-dbg \
    lib32stdc++6 \
    g++-multilib \
    gcc-multilib \
    multiarch-support \
    cmake \
    ipython3 \
    vim \
    net-tools \
    iputils-ping \
    libffi-dev \
    libssl-dev \
    python-pip \
    python3-dev \
    python3-pip \
    python3-distutils \
    build-essential \
    ruby \
    ruby-dev \
    tmux \
    strace \
    ltrace \
    nasm \
    wget \
    radare2 \
    gdb \
    gdb-multiarch \
    netcat \
    socat \
    git \
    patchelf \
    gawk \
    file \
    bison \
    curl \
    wget \
    netcat \
    sudo \
    zsh \
    openssh-server \
&& rm -rf /var/lib/apt/list/* \
&& mkdir -p ${HOME}/.pip \
&& echo -e "[global]\nindex-url = https://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted-host=mirrors.aliyun.com">${HOME}/.pip/pip.conf \
&& python3 -m pip install -U pip \
&& python3 -m pip install --no-cache-dir \
    ropgadget \
    pwntools \
    z3-solver \
    smmap2 \
    apscheduler \
    ropper \
    unicorn \
    keystone-engine \
    capstone \
    angr \
    pebble \
&& gem install one_gadget seccomp-tools \
&& rm -rf /var/lib/gems/2.*/cache/* \
&& useradd -m -u 1000 -G sudo -s /bin/bash admin \
&& echo admin:123 | chpasswd \
&& echo -e "\numask 022\n">>/home/admin/.bashrc \
&& mkdir -p /home/ctf /home/app \
&& chown admin:admin /home/ctf /home/app \
&& cp /root/init_user.bash /tmp/init_user.bash \
&& su - admin - c "bash /tmp/init_user.bash" 


# LibcSearcher
# pwn_debug
