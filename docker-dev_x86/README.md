使用debian:buster，编译环境版本比ubuntu:18.04要高

安装 musl-gcc / golang / rust x86编译环境

golang 建议从外部下载。自带的 golang 版本不高。debian:buster自带版本为1.11，ubuntu:18.04自带的版本为1.10

外部挂载 /home/src 数据卷

建立命令

```
docker build -t dev_x86:v1 .
```

首次启动命令

```
docker run -it -v /home/src:/home/src --name dev_x86 dev_x86:v1
```

后续启动命令

```
docker start -i dev_x86
```