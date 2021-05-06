FROM ubuntu
USER root
RUN sed -i 's/archive.ubuntu.com/mirrors.tencentyun.com/g' /etc/apt/sources.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y python3 nodejs npm python3-pip \
    && echo "python3 install success" \
    && mkdir /data \
    && mkdir /data/node \
    && cd /data/node \
    && npm i puppeteer  --unsafe-perm=true \
    && npm i request  --unsafe-perm=true \
#    && cd /data/stock \
#    && pip3 install torch  -i http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com \
#    && pip3 install torchvision -i http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com \
#    && pip3 install pillow -i http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com \
#    && pip3 install flask -i http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com \
#    && pip3 install loguru -i http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com