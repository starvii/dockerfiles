#!/bin/bash

git clone --depth 1 https://github.com/pwndbg/pwndbg /home/app/pwndbg \
&& bash /home/app/pwndbg/setup.sh \
&& git clone --depth 1 https://github.com/scwuaptx/Pwngdb.git /home/app/pwngdb \
&& cat /home/app/pwngdb/.gdbinit >> /home/admin/.gdbinit \
git clone --depth 1 https://github.com/niklasb/libc-database.git /home/app/libc-database
