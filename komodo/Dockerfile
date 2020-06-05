ARG         BUILD_TAG=komodoofficial/komodo:cd_release_318ec36_dev

FROM        $BUILD_TAG
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

ARG         DEBIAN_FRONTEND=noninteractive

# get ENV vars from composer
ENV         AC=$AC \
            NODE=$NODE \
            MODE=$MODE \
            GEN=$GEN \
            HOME=/

EXPOSE      8465/tcp
EXPOSE      8464/tcp
EXPOSE      11511/tcp
EXPOSE      11510/tcp

# cp configs and bootstrap
COPY        docker/bootstrap /.komodo/
COPY        docker/connect.sh /komodo/src/start
COPY        docker/gencoin.sh /komodo/src/gencoin

RUN         mkdir /.zcash-params && \
            useradd -u 3003 -m swapper && \
            chown -R swapper /.zcash-params && \
            ln -s /komodo/komodod /usr/bin/komodod  && \
            ln -s /komodo/komodo-cli /usr/bin/komodo-cli && \
            apt-get update && \
            apt-get install -y git wget && \
            chmod +x /komodo/src/start && \
            chmod +x /komodo/src/gencoin && \
            chown -R swapper:swapper /komodo && \
            chown -R swapper:swapper /.komodo

USER        swapper
WORKDIR     /komodo/src

# fetch params
RUN         cd /komodo && \
            git clone https://github.com/KomodoPlatform/komodo.git -b master -n fetch && cd fetch && \
            git checkout master -- ./zcutil/fetch-params.sh && \
            ./zcutil/fetch-params.sh

CMD ./start
