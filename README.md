# MarketMaker2 test environment

Based on Docker containers

## Run tests:

You need working installation of Docker-ce and docker-compose. (see instructions below)

In root dir execute:
```bash
$ sudo ./test_run.sh testname
```
Test results are logged in `log/workspace/test.log`. Currently available:

```dummy``` - starts test environment in idle mode,
to use test env in this mode execute: `$ docker exec -it mm2_testenv_composer_workspace_run_id /bin/bash`
after `$ sudo test_run.sh dummy`.
 
```swaps``` - Performs 6 atomic swaps concurrently.

```saturation``` - Propagates maker orders (via setprice method),
 until mm2 network is saturated (more than 5% orders loss).
 
 To run tests manually and/or modify testenv performance see instructions below.

## How to build:

1. Install [Docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community-1)
<<<<<<< HEAD
2. Get docker-compose with pip
=======
2. Get docker-compose with pip 
>>>>>>> master
```pip install docker-compose```
3. Unzip `coin_name.zip` archives in `komodo/docker/bootstrap` to the same folder to bootstrap test chains
4. Create user 3003, set log catalog ownership
```chown -R 3003:3003 log/```, bootstraps ownership ```chown -R 3003:3003 komodo/docker/bootstrap```
<<<<<<< HEAD
5. If needed, modify `example-testname.yml` and `example.env` files.
6. Execute in root directory:
```bash
$ cp example-testname.yml docker-compose.yml
=======
5. If needed, modify `example-compose.yml` and `example.env` files.
6. Execute in repo's root directory:
```bash
$ cp example-compose.yml docker-compose.yml
>>>>>>> master
$ cp example.env .env
$ sudo docker-compose up --build  # with root privileges
```

## Usage and structure:

Base containers are pulled from official Komodo repo: [Komodo](https://hub.docker.com/r/komodoofficial/komodo),
 [atomicdex_api](https://hub.docker.com/r/komodoofficial/atomicdexapi/). You can set container tag to pull in `.env`.
 (see [example.env](https://github.com/SirSevenG/mm2_testenv_composer/blob/master/example.env))

workspace - as name suggest, container to execute tests from, writes logs to ./log/workspace directory

wallets - contains two test chains WSG and BSG wallets information

After tests it's suggested to stop containers ```docker-compose down``` (or ```ctrl+C```) and execute
 ```docker system prune``` to clear containers cache (docker networks) before next run.

[Ctop](https://github.com/bcicen/ctop) is a nice tool to manually monitor system resources usage during test run.

[Network scheme](https://docs.google.com/drawings/d/1BOugSFhBnTUBYBvzkUinmjayKPhAmXcxWEKpqZFHCHE/edit?usp=sharing)
