# based on lukechilds/docker-electrumx, github link: https://github.com/lukechilds/docker-electrumx/

FROM        python:3.7-alpine3.10
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

COPY         ./docker /usr/local/bin
ENV          VERSION=master

RUN         chmod a+x /usr/local/bin/* && \
            apk add --no-cache git build-base openssl && \
            apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/community leveldb-dev && \
            apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing rocksdb-dev && \
            pip install aiohttp pylru plyvel websockets python-rocksdb && \
            git clone -b master https://github.com/cipig/electrumx.git && \
            cd electrumx && \
            python setup.py install && \
            apk del git build-base

VOLUME      ["/data"]
ENV         HOME /data
ENV         ALLOW_ROOT 1
ENV         DB_DIRECTORY /data
ENV         SERVICES=tcp://:50001,ssl://:50002,wss://:50004,rpc://0.0.0.0:8000
ENV         SSL_CERTFILE ${DB_DIRECTORY}/electrumx.crt
ENV         SSL_KEYFILE ${DB_DIRECTORY}/electrumx.key
ENV         HOST ""
ENV         PEER_DISCOVERY = self
WORKDIR     /data

EXPOSE 50001 50002 50004 8000

CMD ["echo", "done"]
