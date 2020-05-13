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

COPY ./init.bash /tmp/init.bash
COPY ./init_user.bash /tmp/init.bash

RUN bash -v /tmp/init.sh

# 多版本的libc
# COPY 

VOLUME ${DOCKER_SHARE}

# 切换至普通用户
CMD ["su", "-", "admin"]