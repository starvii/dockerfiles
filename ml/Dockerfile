# 使用debian:buster
# 外部挂载 /home/ml 数据卷
# 对外映射开放 8888 端口

# 建立命令
#   docker build -t ml:v1 .
# 首次启动命令
#   docker run -it -v /home/ml:/home/ml -p 8888:8888 --name ml ml:v1
# 后续启动命令
#   docker start -i ml


FROM debian:latest

ENV DOCKER_USER="admin" \
    DOCKER_UID="1000" \
    DOCKER_SHRC="/home/${DOCKER_USER}/.bashrc" \
    DOCKER_SHARE="/home/ml"

EXPOSE 8888

RUN cp /etc/apt/sources.list /etc/apt/sources.list~ \
    && sed -i "s@http://deb.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
    && sed -i "s@http://security.debian.org@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list \
    && apt update \
    && apt install -y apt-transport-https ca-certificates \
    && sed -i 's@http://@https://@g' /etc/apt/sources.list \
    && apt update \
    && apt upgrade -y \
    && apt install -y python-pip python3-pip curl wget sudo \
    && useradd -m -u ${DOCKER_UID} -G sudo -s /bin/bash ${DOCKER_USER} \
    && echo ${DOCKER_USER}:123 | chpasswd \
    && mkdir -p ${DOCKER_SHARE} \
    && chown ${DOCKER_USER}:${DOCKER_USER} ${DOCKER_SHARE} \
    && echo -e "\numask 022\n" >> ${DOCKER_SHRC} \
    && mkdir -p /etc/pip \
    && echo -e "[global]\nindex-url=https://mirrors.huaweicloud.com/repository/pypi/simple\ntrusted-host=mirrors.huaweicloud.com\ntimeout=120" > /etc/pip/pip.conf \
    && ln -s /etc/pip ${HOME}/.pip \
    && ln -s /etc/pip ${DOCKER_HOME}/.pip \
    && python3 -m pip install -U pip setuptools jupyter numpy pandas sklearn

VOLUME /home/src

CMD ["su", "-", "admin", "-c", "jupyter notebook --no-browser --port=8888 --ip=0.0.0.0 /home/ml"]
