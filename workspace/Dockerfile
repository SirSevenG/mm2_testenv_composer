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
            useradd -u 3003 -m swapper && \
            chown -R swapper:swapper /workdir && \
            chown -R swapper:swapper /log && \
            pip3 install -r /workdir/reqs.txt

USER        swapper
WORKDIR     /workdir

CMD ["python3", "test.py"]
