# MarketMaker2 test environment

Based on Docker containers

## How to build:

1. Install [Docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community-1)
1. Get docker-compose with pip 
```pip install docker-compose```
1. Create user 3003, set log catalog ownership
```chown -R 3003:3003 log/```
1. Unzip coin_name.tar.gz archives in base_kmd/docker/ to the same folder to bootstrap test chains
1. If needed, modify example-compose.yml and example.env files. Execute in repo's root directory
```
$ cp example-compose.yml docker-compose.yml
$ cp example.env .env
$ docker-compose up --build
```

## Usage and structure:

base_* catalogs contain basic Docker images for komodod, atomicdex-API and electrumx, all can be used separately

workspace - as name suggest, container to execute tests from, writes logs to ./log/workspace directory

wallets - contains two test chains WSG and BSG wallets information

After executing ```docker-compose up``` test.py in workspace container will run, test logs are written in realtime, after tests it's suggested to stop containers ```docker-compose down``` (or ```ctrl+C```) and execute ```docker system prune``` to clear containers cache before next run.

[Ctop](https://github.com/bcicen/ctop) is a nice tool to manually monitor system resources usage during test run

### TODOs

Use actual log module in test instead of current abomination

Set alternative mm2 container to run chains in native mode

Wirte more tests
