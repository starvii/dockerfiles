# 使用debian:buster，编译环境版本比ubuntu:18.04要高
# 安装 musl-gcc / golang / rust x86编译环境
# golang 建议从外部下载。自带的 golang 版本不高。debian:buster自带版本为1.11，ubuntu:18.04自带的版本为1.10
# 外部挂载 /home/src 数据卷

# 建立命令
#   docker build -t dev_x86:v1 .
# 首次启动命令
#   docker run -it -v /home/src:/home/src --name dev_x86 dev_x86:v1
# 后续启动命令
#   docker start -i dev_x86


FROM i386/debian:latest

ARG DOCKER_USER="admin"
ARG DOCKER_UID="1000"
ARG DOCKER_SHRC="/home/${DOCKER_USER}/.bashrc"
ARG DOCKER_SHARE="/home/src"
ARG DOCKER_HTTP_PROXY="http://10.0.0.1:57070"
ARG RUSTUP_UPDATE_ROOT="https://mirrors.tuna.tsinghua.edu.cn/rustup"
ARG RUSTUP_DIST_SERVER="https://mirrors.ustc.edu.cn/rust-static/rustup"

ENV RUSTUP_UPDATE_ROOT="https://mirrors.tuna.tsinghua.edu.cn/rustup" \
    RUSTUP_DIST_SERVER="https://mirrors.ustc.edu.cn/rust-static/rustup"

RUN echo "\$DOCKER_USER = $DOCKER_USER" \
    && echo "\$DOCKER_UID = $DOCKER_UID" \
    && echo "\$DOCKER_SHRC = $DOCKER_SHRC" \
    && echo "\$DOCKER_SHARE = $DOCKER_SHARE" \
    && echo "\$DOCKER_HTTP_PROXY = $DOCKER_HTTP_PROXY" \
    && echo "\$RUSTUP_DIST_SERVER = $RUSTUP_DIST_SERVER" \
    && echo "\$RUSTUP_UPDATE_ROOT = $RUSTUP_UPDATE_ROOT" \
    && cp /etc/apt/sources.list /etc/apt/sources.list~ \
    && sed -i "s@http://deb.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
    && sed -i "s@http://security.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
    && apt update \
    && apt install -y apt-transport-https ca-certificates \
    && sed -i 's@http://@https://@g' /etc/apt/sources.list \
    && apt update \
    && apt upgrade -y \
    && apt install -y git vim build-essential gdb cmake golang musl-tools musl-dev python-pip python3-pip curl wget netcat sudo \
    libssl-dev \
    && useradd -m -u ${DOCKER_UID} -G sudo -s /bin/bash ${DOCKER_USER} \
    && echo ${DOCKER_USER}:123 | chpasswd \
    && mkdir -p ${DOCKER_SHARE} \
    && chown ${DOCKER_USER}:${DOCKER_USER} ${DOCKER_SHARE} \
    && bash -c 'echo -e "\numask 022\nexport RUSTUP_UPDATE_ROOT=${RUSTUP_UPDATE_ROOT}\nexport RUSTUP_DIST_SERVER=${RUSTUP_DIST_SERVER}\nexport PATH=\${PATH}:\${HOME}/.cargo/bin\nexport GOPATH=/home/src/go\n" >> ${DOCKER_SHRC}' \
    && su - ${DOCKER_USER} -c "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y" \
    && su - ${DOCKER_USER} -c "rustup -q target add i586-unknown-linux-musl i686-unknown-linux-musl" \
    && bash -c 'echo -e "\nexport HTTP_PROXY=${DOCKER_HTTP_PROXY}\nexport HTTPS_PROXY=\${HTTP_PROXY}\nexport http_proxy=\${HTTP_PROXY}\nexport https_proxy=\${HTTP_PROXY}\n" >> ${DOCKER_SHRC}' \
    && git config --global http.proxy ${DOCKER_HTTP_PROXY} \
    && git config --global https.proxy ${DOCKER_HTTP_PROXY}

VOLUME ${DOCKER_SHARE}

CMD ["su", "-", "admin"]
