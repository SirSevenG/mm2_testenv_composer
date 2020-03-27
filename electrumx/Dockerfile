FROM           local/electrumx:latest

# get env vars from composer
ENV         SERVICES=$SERVICES \
            COIN=$COIN \
            DAEMON_URL=$DAEMON_URL \
            DB_DIRECTORY=$DB_DIRECTORY \
            LOG_LEVEL=$LOG_LEVEL

CMD init
