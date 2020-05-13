# 使用ubuntu 18.04，常见的pwn环境，自带libc版本是2.27
# 安装常见ctf/pwn工具
# 外部挂载 /home/ctf 数据卷
# 端口映射 22 -> 1122

# 建立命令
#   docker build -t ctf:v1 .
# 首次启动命令
#   docker run -it -p 1122:22 -v /home/ctf:/home/ctf --name ctf ctf:v1
# 后续启动命令
#   docker start -i ctf


FROM ubuntu:18.04

ARG DOCKER_SHARE="/home/ctf"

COPY init.py /tmp/init.py

RUN bash -c "echo -e 'deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse\n\ndeb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse\n\ndeb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse\n\ndeb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse\n\ndeb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse'>/etc/apt/sources.list" \
&& apt update -y \
&& apt install -y python3 \
&& python3 /tmp/init.py \
&& rm -rf /tmp/init.py \
&& mkdir /var/run/sshd

VOLUME ${DOCKER_SHARE}
EXPOSE 22

# 切换至普通用户
# CMD ["su", "-", "admin"]
CMD ["bash", "-c", "/usr/sbin/sshd -D&; su - admin"]
