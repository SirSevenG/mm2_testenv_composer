# Run $MODE script for $CHAIN in base container komodo/local:latest (base_komodo)

FROM local/komodo:latest

USER        root
WORKDIR     /komodo/src

EXPOSE 11510
EXPOSE 8464

# Passed from compose:
#  -ac_name=${CHAIN} -ac_supply=${SUPPLY} -addnode=${NODE} -ac_cc=${CC} 

COPY        docker/connect.sh /komodo/src/start
COPY        docker/gencoin.sh /komodo/src/gencoin
# COPY docker/bootsrap /komodo/path/to/blocks

RUN         chmod +x /komodo/src/start && \
            chmod +x /komodo/src/gencoin && \
            chown -R swapper:swapper /komodo/src
USER        swapper

CMD ./start
