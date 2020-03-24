FROM        komodoofficial/komodo:cd_release_f04f510_dev
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

ARG         DEBIAN_FRONTEND=noninteractive

EXPOSE      8465/tcp
EXPOSE      11511/tcp

RUN         mkdir /.zcash-params && \
            useradd -u 3003 -m swapper && \
            chown -R swapper /komodo && \
            chown -R swapper /.zcash-params

# Configuration
COPY        docker/bootstrap /.komodo/

USER        swapper
WORKDIR     /komodo/src

CMD ["echo", "done"]
