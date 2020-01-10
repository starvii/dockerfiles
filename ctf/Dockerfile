# 使用debian，常见的pwn环境，自带libc版本是2.28
# 安装常见ctf/pwn工具
# 外部挂载 /home/ctf 数据卷
# 端口映射 22 -> 1122

# 建立命令
#   docker build -t ctf:v1 .
# 首次启动命令
#   docker run -it -p 22:1122 -v /home/ctf:/home/ctf --name ctf ctf:v1
# 后续启动命令
#   docker start -i ctf


FROM debian:buster

ENV DOCKER_USER="admin" \
    DOCKER_UID="1000" \
    DOCKER_HOME="/home/${DOCKER_USER}" \
    DOCKER_SHRC="${DOCKER_HOME}/.bashrc" \
    DOCKER_SHARE="/home/ctf"
    

RUN cp /etc/apt/sources.list /etc/apt/sources.list~ \
    && sed -i "s@http://deb.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
    && sed -i "s@http://security.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
    && apt update \
    && apt install -y apt-transport-https ca-certificates \
    && sed -i 's@http://@https://@g' /etc/apt/sources.list \
    && apt update \
    && apt upgrade -y \
    && dpkg --add-architecture i386 \
    && apt install -y git vim build-essential gdb cmake python-pip python3-pip curl wget netcat sudo openssh-server net-tools zsh \
        gcc-multilib g++-multilib multiarch-support php php-mysql mariadb-server binwalk rlwrap socat \
        libgmp-dev libmpc-dev libmpfr-dev \
        rubygems \
    && systemctl enable ssh apache2 mysql \
    && useradd -m -u ${DOCKER_UID} -G sudo -s /bin/bash ${DOCKER_USER} \
    && echo ${DOCKER_USER}:123 | chpasswd \
    && mkdir -p ${DOCKER_SHARE} /home/app \
    && chown ${DOCKER_USER}:${DOCKER_USER} ${DOCKER_SHARE} /home/app \
    && mkdir -p /etc/pip \
    && echo -e "\[global\]\nindex-url=https://mirrors.huaweicloud.com/repository/pypi/simple\ntrusted-host=mirrors.huaweicloud.com\ntimeout=120" > /etc/pip/pip.conf \
    && ln -s /etc/pip ${HOME}/.pip \
    && ln -s /etc/pip ${DOCKER_HOME}/.pip \
    && python2 -m pip uninstall -y pycrypto crypto \
    && python3 -m pip uninstall -y pycrypto crypto \
    && python2 -m pip install -U pip setuptools pwntools pycrypto gmpy gmpy2 \
    && python3 -m pip install -U pip setuptools pycrypto gmpy gmpy2 uncompyle6 \
    && su - admin -c "git clone https://github.com/inaz2/roputils.git /home/app/roputils" \
    && su - admin -c "git clone https://github.com/zardus/ctf-tools.git /home/app/ctf-tools" \
    && 

VOLUME /home/ctf

CMD ["su", "-", "admin"]