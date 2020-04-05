#!/bin/bash

useradd -u 3003 -m swapper
cd komodo/docker/bootstrap || return
unzip BSG.zip
unzip WSG.zip
cd ../../.. || return
chown -R 3003:3003 log
chown -R 3003:3003 komodo/docker/bootstrap
cp example-"$1".yml docker-compose.yml
cp example.env .env
docker-compose build
docker-compose run workspace
docker-compose down
