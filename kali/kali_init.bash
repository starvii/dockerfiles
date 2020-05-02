#!/bin/bash

# 添加用户
useradd -m -G sudo -s /bin/bash admin
echo admin:123 | chpasswd

# 命令行
systemctl set-default multi-user.target
# 允许ssh远程登录
systemctl enable ssh

# 默认使用中科大源。也可以去掉注释改为华为源
mv /etc/apt/sources.list /etc/apt/sources.list~
echo -e "#deb https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib\n#deb-src https://mirrors.huaweicloud.com/kali kali-rolling main non-free contrib\n#deb [arch=amd64] https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu disco stable\ndeb https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib\ndeb-src https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib" > /etc/apt/sources.list

# 更新系统
apt update && apt upgrade -y

# 安装lamp
apt install mariadb-server mariadb-client php php-mysql
systemctl disable mysql
systemctl disable apache2
# 修改mariadb用户与密码

# 安装Jdk与Maven


# 安装docker

