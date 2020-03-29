FROM        ubuntu:bionic
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

ARG         DEBIAN_FRONTEND=noninteractive

COPY        docker/ /workdir

ENV         PACKS="python3.7 \
            wget \
            nano \
            python3-setuptools \
            python3-dev \
            python3-pip \
            python-pycurl \
            curl \
            libcurl4-openssl-dev \
            libssl-dev"

RUN         apt-get update && \
            apt-get -y install -q $PACKS && \
            mkdir /log && \
            touch /log/log.txt && \
            useradd -u 3003 -m swapper && \
            chown -R 3003:3003 /workdir && \
            chown -R 3003:3003 /log && \
            python3 -m pip install --upgrade pip && \
            python3 -m pip install -r /workdir/reqs.txt

USER        swapper
WORKDIR     /workdir

CMD ["python3", "test.py"]
