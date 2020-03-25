FROM        komodoofficial/atomicdexapi:beta-2.0.1781
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

RUN         useradd -u 3003 -m swapper && \
            mkdir /log && \
            touch /log/log.txt && \
            chown -R 3003:3003 /log

COPY        docker /mmaker2

USER        root
RUN         chmod +x /mmaker2/start.sh && \
            cd /mmaker2
#    wget https://raw.githubusercontent.com/jl777/coins/master/coins
RUN         apt-get update && \
            apt-get install -y \
            dnsutils \
            curl

WORKDIR     /mmaker2

CMD ./start.sh