ARG         BUILD_TAG=komodoofficial/atomicdexapi:beta-2.0.2128

FROM        $BUILD_TAG
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

# get env vars from composer
ENV         SEED="False" \
            PASSPHRASE="" \
            MM_LOG="/log/mm.log"

COPY        docker /mmaker2

RUN         apt-get update && \
            apt-get install -y \
                dnsutils \
                curl \
                python3.7 \
                wget \
                nano \
                python3-setuptools \
                python3-dev \
                python3-pip \
                python-pycurl \
                curl \
                libcurl4-openssl-dev \
                libssl-dev && \
            useradd -u 3003 -m swapper && \
            mkdir /log && \
            touch /log/log.txt && \
            chown -R 3003:3003 /log && \
            chmod +x /mmaker2/start.sh && \
            cd /mmaker2 && \
            python3 -m pip install --upgrade pip && \
            python3 -m pip install -r /mmaker2/reqs.txt
#    wget https://raw.githubusercontent.com/jl777/coins/master/coins

WORKDIR     /mmaker2

CMD ./start_mock.sh
