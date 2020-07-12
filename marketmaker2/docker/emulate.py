from mm2proxy import MMProxy
from pycurl import error as perror
import time
import ujson


def enable_coins(proxy: MMProxy, conffile: str) -> list:
    coins_enabled = []
    with open(conffile) as f:
        coinsconf = ujson.load(f)
        for item in coinsconf:
            coin = item.get('name')
            cointype = item.get('type')
            if cointype != 'erc':
                servers = []
                electrums = item.get('serverList')
                for electrum in electrums:
                    servers.append({'url': electrum})
                proxy.electrum(coin=coin, servers=servers, tx_history=True, mm2=1)
            else:
                urls = []
                contract = item.get('swap_contract_address')
                servers = item.get('serverList')
                for server in servers:
                    urls.append(str(server))
                proxy.enable(coin=coin, urls=urls, tx_history=True, mm2=1, swap_contract_address=contract)
            coins_enabled.append(coin)
    return coins_enabled


def mock():
    node_params_dictionary = {
        'userpass': 'OHSHITHEREWEGOAGAIN',
        'rpchost': '127.0.0.1',
        'rpcport': 7783
    }
    try:
        mm_node = MMProxy(node_params_dictionary, timeout=120)
    except ConnectionAbortedError as e:
        raise Exception("Connection error! Probably no daemon on selected port. Error: ", e)
    # check connections
    while True:
        attempt = 0
        try:
            res = mm_node.version()
            print(res)
            break
        except perror as e:
            attempt += 1
            print('MM2 does not respond, retrying\nError: ', e)
            if attempt > 15:
                raise Exception("Connection error ", e)
            else:
                time.sleep(5)
    time.sleep(10)
    coins = enable_coins(mm_node, "coinconf.json")
    time.sleep(5)
    count = 0
    while True:
        if count >= 20:
            mm_node.metrics()
            count = 0
        for coin in coins:
            mm_node.my_balance(coin)
        time.sleep(30)
        count += 1


if __name__ == '__main__':
    mock()
