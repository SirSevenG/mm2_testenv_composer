FROM        ubuntu:bionic
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

ARG         DEBIAN_FRONTEND=noninteractive
ARG         KOMODO_BRANCH=beta

EXPOSE      8465/tcp
EXPOSE      11511/tcp

RUN         mkdir /komodo && \
            mkdir .komodo && \
            mkdir /.zcash-params
RUN         useradd -u 3003 -m swapper

ENV         PACKS="build-essential \
            pkg-config \
            libcurl3-gnutls-dev \
            libc6-dev libevent-dev \
            m4 g++-multilib \
            autoconf \
            libtool \
            ncurses-dev \
            unzip \
            git \
            python \
            zlib1g-dev \
            wget \
            bsdmainutils \
            automake \
            libboost-all-dev \
            libssl-dev \
            libprotobuf-dev \
            protobuf-compiler \
            libqt4-dev \
            libqrencode-dev \
            libdb++-dev \
            curl \
            libcurl3-gnutls-dev \
            libgomp1"

# Install komodo deps
RUN         apt-get update && \
            apt-get -y install -q $PACKS

# Build komodod
RUN         mkdir -p /.ccache/tmp
RUN         chown -R swapper /komodo && \
            chown -R swapper /.zcash-params && \
            chown -R swapper /.ccache
ENV         HOME=/
USER        swapper
WORKDIR     /
RUN         git clone https://github.com/jl777/komodo --branch $KOMODO_BRANCH --single-branch /komodo && \
            cd /komodo && \
            ./zcutil/fetch-params.sh && \
            ./zcutil/build.sh -j$(nproc)

USER        root

# Cleanup
RUN         apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
            rm -rf /var/lib/apt/lists/* && \
            rm -rf /komodo/depends

# Runtime packs
RUN         apt-get update && \
            apt-get install -y  -q \
            curl \
            libcurl3-gnutls-dev \
            libgomp1

# Configuration
COPY        docker/ /.komodo/

# Ownership
RUN         chown -R swapper /.komodo

USER        swapper
WORKDIR     /komodo/src

CMD ["echo", "done"]
