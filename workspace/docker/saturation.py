from mm2rpclib import MMProxy
from pycurl import error as perror
import time
import os
import logging
import pytest

# TODO:
# 6. pytest implementation
# V7. Debug me
# V8. Log file check


def init_logs(logfile="/log/saturation.log"):
    if os.path.isfile(logfile):
        os.remove(logfile)
    with open(logfile, 'a') as f:
        pass  # creates empty file for logs

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(logfile)
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    log.addHandler(c_handler)
    log.addHandler(f_handler)
    return log


def init_connection(mm2userpass: str, mm_nodes: list, electrums_base: list, electrums_rel: list,
                    base: str, rel: str) -> dict:
    """Creates MM2 proxies, enables base and rel coins on each node"""
    mm_proxy = {}
    for node in mm_nodes:  # connect to all mm nodes
        node_params_dictionary = {
            'userpass': mm2userpass,  # userpass to be used in jsonrpc
            'rpchost': node,
            'rpcport': 7783
        }
        try:
            proxy = MMProxy(node_params_dictionary, timeout=120)
        except ConnectionAbortedError as e:
            raise Exception("Connection error! Probably no daemon on selected port. Error: ", e)
        mm_proxy.update({node: proxy})
        # check connections
        while True:
            attempt = 0
            try:
                res = proxy.version()
                print(res)
                break
            except perror as e:
                attempt += 1
                print('MM2 does not respond, retrying')
                if attempt >= 15:
                    raise Exception("Connection error ", e)
                else:
                    time.sleep(5)
    # enable coins
    servers_base = []
    servers_rel = []
    for electrum in electrums_base:
        servers_base.append({'url': electrum, 'protocol': 'TCP'})
    for electrum in electrums_rel:
        servers_rel.append({'url': electrum, 'protocol': 'TCP'})
    for node in mm_nodes:
        proxy = mm_proxy[node]
        attempt = 0
        while attempt < 40:
            res1 = proxy.electrum(coin=base, servers=servers_base)
            res2 = proxy.electrum(coin=rel, servers=servers_rel)
            if not res2.get('error'):
                break
            else:
                attempt += 1
                time.sleep(2)

    return mm_proxy


def get_orders_amount(proxy: MMProxy, base: str, rel: str) -> dict:
    """Get amount of orders from node"""
    res = proxy.orderbook(base=base, rel=rel)
    asks = res.get('numasks')
    bids = res.get('numbids')
    orders = {
        'numasks': asks,
        'numbids': bids,
        'amount': asks+bids
    }
    return orders


def check_saturation(vol1: int, vol2: int) -> bool:
    """Check if percentage of orders received is acceptable"""
    acceptance = 0.95
    # debug
    print(vol1)
    print(vol2)
    try:
        if vol2/vol1 >= acceptance:
            return True
        else:
            return False
    except ZeroDivisionError:
        return True


def main():
    log = init_logs()
    userpass = 'OHSHITHEREWEGOAGAIN'
    mm_nodes = ['mm_seed', 'mm_swapper_a', 'mm_swapper_b']
    electrums_a = ["electrum_aa:50001", "electrum_ab:50001"]
    electrums_b = ["electrum_ba:50001", "electrum_bb:50001"]
    coin_a = 'WSG'
    coin_b = 'BSG'
    log.info("Connecting to mm2 nodes")
    proxy_dict = init_connection(userpass, mm_nodes, electrums_a, electrums_b, coin_a, coin_b)
    log.info("mm2 nodes connected, coins enabled")
    maker = proxy_dict.get('mm_swapper_a')
    taker = proxy_dict.get('mm_swapper_b')
    orders_broadcast_init = orders_broadcast = 15  # also sep
    info_orders = orders_broadcast
    check = True  # init "pass" value
    log.info("Entering main test loop")
    while check:
        log.info("Clearing up previous orders in 30s")
        maker.cancel_all_orders(cancel_by={'type': 'All'})  # reset orders
        time.sleep(30)
        log.debug("New iteration, orders to broadcast: %s", str(orders_broadcast))
        for i in range(orders_broadcast):
            log.debug("Order placing num: %s", str(i + 1))
            res = maker.setprice(base=coin_a, rel=coin_b, price='0.1', volume='1', cancel_previous=False)
            log.debug("Response: %s", str(res))
            assert res.get('result').get('uuid')
            time.sleep(1)
        time.sleep(30)  # time to propagate orders
        maker_orders = get_orders_amount(maker, coin_a, coin_b).get('amount')
        log.debug("Maker node orders available: %s", str(maker_orders))
        taker_orders = get_orders_amount(taker, coin_a, coin_b).get('amount')
        log.debug("Taker node orders available: %s", str(taker_orders))
        check = check_saturation(maker_orders, taker_orders)
        check_str = 'passed' if check else 'failed'  # bool can not be explicitly converted
        log.debug("Maker to Taker orders amount check: %s", str(check_str))
        check = check_saturation(orders_broadcast, taker_orders)
        check_str = 'passed' if check else 'failed'
        log.debug("Taker to Created orders amount check passed: %s", str(check_str))
        log.info("Test iteration finished")
        info_orders = orders_broadcast
        orders_broadcast += orders_broadcast_init
    log.info("Test result. Network saturated with orders broadcasted: %s", str(info_orders))


if __name__ == '__main__':
    main()
