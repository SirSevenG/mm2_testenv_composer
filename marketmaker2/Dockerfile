FROM local/mm2:latest

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