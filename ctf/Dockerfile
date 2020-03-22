# 使用debian，常见的pwn环境，自带libc版本是2.28
# 安装常见ctf/pwn工具
# 外部挂载 /home/ctf 数据卷
# 端口映射 22 -> 1122

# 建立命令
#   docker build -t ctf:v1 .
# 首次启动命令
#   docker run -it -p 1122:22 -v /home/ctf:/home/ctf --name ctf ctf:v1
# 后续启动命令
#   docker start -i ctf


FROM debian:buster

COPY ./init.sh /tmp/init.sh

RUN bash /tmp/init.sh

# 多版本的libc
# COPY 

VOLUME ${DOCKER_SHARE}

CMD ["su", "-", "admin"]