FROM        komodoofficial/komodo:cd_release_f04f510_dev
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

ARG         DEBIAN_FRONTEND=noninteractive

EXPOSE      8465/tcp
EXPOSE      11511/tcp

RUN         mkdir /.zcash-params && \
            useradd -u 3003 -m swapper && \
            chown -R swapper /komodo && \
            chown -R swapper /.zcash-params && \
            ln -s /komodo/komodod /usr/bin/komodod  && \
            ln -s /komodo/komodo-cli /usr/bin/komodo-cli && \
            apt-get update && \
            apt-get install -y git wget

# cp configs and bootstrap
COPY        docker/bootstrap /.komodo/

USER        swapper
WORKDIR     /komodo/src

# fetch params
RUN         cd /komodo && \
            git clone https://github.com/KomodoPlatform/komodo.git -b master -n fetch && cd fetch && \
            git checkout master -- ./zcutil/fetch-params.sh && \
            ./zcutil/fetch-params.sh

CMD ["echo", "done"]
