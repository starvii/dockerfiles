#!/bin/sh

mkdir -p /root/script/ubuntu
mkdir -p /root/script/.external
wget http://10.0.0.1/script/ubuntu/init.py -O /root/script/ubuntu/init.py \
&& wget http://10.0.0.1/script/.external/get-pip.tgz -O /root/script/.external/get-pip.tgz \
&& wget http://10.0.0.1/script/.external/oh_my_zsh.sh -O /root/script/.external/oh_my_zsh.sh \
&& python3 /root/script/ubuntu/init.py
