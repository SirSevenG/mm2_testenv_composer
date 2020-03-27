FROM        komodoofficial/atomicdexapi:beta-2.0.1781
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

# get env vars from composer
ENV         SEED=$SEED \
            PASSPHRASE=$PASSPHRASE \
            MM_LOG=$MM_LOG

COPY        docker /mmaker2

RUN         apt-get update && \
            apt-get install -y \
            dnsutils \
            curl && \
            useradd -u 3003 -m swapper && \
            mkdir /log && \
            touch /log/log.txt && \
            chown -R 3003:3003 /log && \
            chmod +x /mmaker2/start.sh && \
            cd /mmaker2
#    wget https://raw.githubusercontent.com/jl777/coins/master/coins

WORKDIR     /mmaker2

CMD ./start.sh
