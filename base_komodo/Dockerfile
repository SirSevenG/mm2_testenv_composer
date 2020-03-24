FROM        komodoofficial/komodo
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

ARG         DEBIAN_FRONTEND=noninteractive

EXPOSE      8465/tcp
EXPOSE      11511/tcp

RUN         mkdir /.zcash-params && \
            useradd -u 3003 -m swapper && \
            chown -R swapper /komodo && \
            chown -R swapper /.zcash-params && \
            chown -R swapper /.ccach

# Configuration
COPY        docker/bootstrap /.komodo/

USER        swapper
WORKDIR     /komodo/src

CMD ["echo", "done"]
