FROM        komodoofficial/atomicdexapi:beta-2.0.1781
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

RUN         
            useradd -u 3003 -m swapper && \
            mkdir /log && \
            touch /log/log.txt && \
            chown -R 3003:3003 /log

CMD ["echo", "done"]
