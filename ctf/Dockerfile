# 使用debian，常见的pwn环境，自带libc版本是2.28
# 安装常见ctf/pwn工具
# 外部挂载 /home/ctf 数据卷
# 端口映射 22 -> 1122

# 建立命令
#   docker build -t ctf:pwn .
# 首次启动命令
#   docker run -it -p 1122:22 -v /home/ctf:/home/ctf --name pwn ctf:pwn
# 后续启动命令
#   docker start -i pwn


FROM debian:buster

ARG DOCKER_USER="admin"
ARG DOCKER_UID="1000"
ARG DOCKER_PASSWD="123"
ARG DOCKER_SHRC="/home/${DOCKER_USER}/.bashrc"
ARG DOCKER_SHARE="/home/ctf"
ARG DOCKER_PORT="1122"

RUN cp /etc/apt/sources.list /etc/apt/sources.list~ \
    && echo "更新系统" \
    && sed -i "s@http://deb.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
    && sed -i "s@http://security.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
    && apt update &>/dev/null \
    && apt install -y apt-transport-https ca-certificates &>/dev/null \
    && sed -i 's@http://@https://@g' /etc/apt/sources.list \
    && apt update &>/dev/null \
    && apt upgrade -y &>/dev/null \
    && echo "安装基础组件" \
    && apt install -y git vim build-essential gdb cmake python-pip python3-pip curl wget netcat sudo net-tools &>/dev/null \
    && echo "安装ctf基础组件" \
    && apt install -y binwalk rlwrap socat libgmp-dev libmpc-dev libmpfr-dev rubygems &>/dev/null \
    && echo "安装x86支持" \
    && dpkg --add-architecture i386 &>/dev/null \
    && apt install -y gcc-multilib g++-multilib multiarch-support &>/dev/null \
    && echo "安装sshd" \
    && apt install -y openssh-server &>/dev/null \
    && systemctl enable ssh &>/dev/null \
    && echo "建立常规用户" \
    && useradd -m -u ${DOCKER_UID} -G sudo -s /bin/bash ${DOCKER_USER} \
    && echo ${DOCKER_USER}:${DOCKER_PASSWD} | chpasswd \
    && bash -c 'echo -e "\numask 022\nexport PATH=\${PATH}:/home/admin/.gem/ruby/2.5.0/bin\n" >> ${DOCKER_SHRC}' \
    && echo "建立应用程序目录与共享目录" \
    && mkdir -p ${DOCKER_SHARE} /home/app \
    && chown ${DOCKER_USER}:${DOCKER_USER} ${DOCKER_SHARE} /home/app \
    && echo "配置PIP源" \
    && mkdir -p /etc/pip \
    && bash -c "echo -e '[global]\nindex-url=https://mirrors.huaweicloud.com/repository/pypi/simple\ntrusted-host=mirrors.huaweicloud.com\ntimeout=120' > /etc/pip/pip.conf" \
    && ln -s /etc/pip ${HOME}/.pip \
    && ln -s /etc/pip ${DOCKER_HOME}/.pip \
    && echo "安装python模块" \
    && python2 -m pip uninstall -y pycrypto crypto &>/dev/null \
    && python3 -m pip uninstall -y pycrypto crypto &>/dev/null \
    && echo "安装pwntools pycrypto gmpy gmpy2到python2" \
    && python2 -m pip install -U pip setuptools pwntools pycrypto gmpy gmpy2 &>/dev/null \
    && echo "安装uncompyle6 pycrypto gmpy gmpy2到python3" \
    && python3 -m pip install -U pip setuptools pycrypto gmpy gmpy2 uncompyle6 &>/dev/null \
    && echo "安装ctf-tools" \
    && su - admin -c "git clone https://github.com/zardus/ctf-tools.git /home/app/ctf-tools" &>/dev/null \
    # one_gadget（rubygems）
    && su - admin -c "cd /home/app/ctf-tools/one_gadget && ./install" \
    && ln -s /home/admin/.gem/ruby/2.5.0/bin/one_gadget /usr/bin/one_gadget \
    # peda
    && su - admin -c "cd /home/app/ctf-tools/peda && ./install" \
    # pwndbg
    ## && su - admin -c "cd /home/app/ctf-tools/pwndbg && ./install"
    ## 由于pwndbg自动安装存在问题，故使用手动安装
    # rp++
    && su - admin -c "cd /home/app/ctf-tools/rp++ && ./install" \
    && ln -s /home/app/ctf-tools/rp++/bin/rp++ /usr/bin/rp++ \
    # yafu
    # yafu运行时报段错误，可能需要到当前目录下运行？

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

# 多版本的libc
# COPY 

VOLUME ${DOCKER_SHARE}

CMD ["su", "-", "admin"]