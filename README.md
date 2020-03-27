# MarketMaker2 test environment

Based on Docker containers

## How to build:

1. Install [Docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community-1)
2. Get docker-compose with pip 
```pip install docker-compose```
3. Unzip `coin_name.zip` archives in `komodo/docker/bootstrap` to the same folder to bootstrap test chains
4. Create user 3003, set log catalog ownership
```chown -R 3003:3003 log/```, bootstraps ownership ```chown -R 3003:3003 komodo/docker/bootstrap```
5. If needed, modify `example-compose.yml` and `example.env` files.
6. Execute in repo's root directory:
```bash
$ cp example-compose.yml docker-compose.yml
$ cp example.env .env
$ sudo docker-compose up --build  # with root privileges
```

## Usage and structure:

workspace - as name suggest, container to execute tests from, writes logs to ./log/workspace directory

wallets - contains two test chains WSG and BSG wallets information

After executing ```docker-compose up``` test.py in workspace container will run, test logs are written in realtime.
 
After tests it's suggested to stop containers ```docker-compose down``` (or ```ctrl+C```) and execute
 ```docker system prune``` to clear containers cache (docker networks) before next run.

[Ctop](https://github.com/bcicen/ctop) is a nice tool to manually monitor system resources usage during test run.

Network scheme: ```[placeholder]```

### TODOs

Use actual log module in test instead of current abomination

Wirte more tests
