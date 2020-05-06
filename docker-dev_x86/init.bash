DOCKER_USER="admin"
DOCKER_UID="1000"
DOCKER_PASSWD="123"
DOCKER_SHRC="/home/${DOCKER_USER}/.bashrc"
DOCKER_SHARE="/home/src"
DOCKER_HTTP_PROXY="http://10.0.0.1:57070"
RUSTUP_DIST_SERVER="https://mirrors.ustc.edu.cn/rust-static"
RUSTUP_UPDATE_ROOT="https://mirrors.ustc.edu.cn/rust-static/rustup"

echo "\$DOCKER_USER = ${DOCKER_USER}" \
&& echo "\$DOCKER_UID = ${DOCKER_UID}" \
&& echo "\$DOCKER_SHRC = ${DOCKER_SHRC}" \
&& echo "\$DOCKER_SHARE = ${DOCKER_SHARE}" \
&& echo "\$DOCKER_HTTP_PROXY = ${DOCKER_HTTP_PROXY}" \
&& echo "\$RUSTUP_DIST_SERVER = ${RUSTUP_DIST_SERVER}" \
&& echo "\$RUSTUP_UPDATE_ROOT = ${RUSTUP_UPDATE_ROOT}" \
&& cp /etc/apt/sources.list /etc/apt/sources.list~ \
&& sed -i "s@http://deb.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
&& sed -i "s@http://security.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
&& apt update \
&& apt install -y apt-transport-https ca-certificates \
&& sed -i 's@http://@https://@g' /etc/apt/sources.list \
&& apt update \
&& apt upgrade -y \
&& apt install -y git vim build-essential gdb cmake golang musl-tools musl-dev python-pip python3-pip curl wget netcat sudo \
libssl-dev pkg-config libtool \
&& useradd -m -u ${DOCKER_UID} -G sudo -s /bin/bash ${DOCKER_USER} \
&& echo ${DOCKER_USER}:${DOCKER_PASSWD} | chpasswd \
&& mkdir -p ${DOCKER_SHARE} \
&& chown ${DOCKER_USER}:${DOCKER_USER} ${DOCKER_SHARE} \
&& echo -e "\numask 022\nexport RUSTUP_UPDATE_ROOT=${RUSTUP_UPDATE_ROOT}\nexport RUSTUP_DIST_SERVER=${RUSTUP_DIST_SERVER}\nexport PATH=\${PATH}:\${HOME}/.cargo/bin\nexport GOPATH=/home/src/go\n" >> ${DOCKER_SHRC} \
&& su - ${DOCKER_USER} -c "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y" \
&& su - ${DOCKER_USER} -c "rustup -q target add i586-unknown-linux-musl i686-unknown-linux-musl" \
&& echo -e "\nexport HTTP_PROXY=${DOCKER_HTTP_PROXY}\nexport HTTPS_PROXY=\${HTTP_PROXY}\nexport http_proxy=\${HTTP_PROXY}\nexport https_proxy=\${HTTP_PROXY}\n" >> ${DOCKER_SHRC} \
&& git config --global http.proxy ${DOCKER_HTTP_PROXY} \
&& git config --global https.proxy ${DOCKER_HTTP_PROXY}