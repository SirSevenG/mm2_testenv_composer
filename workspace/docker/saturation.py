from mm2rpclib import MMProxy
from pycurl import error as perror
import time
import logging
import pytest

# TODO: and logic for test
# V1. check slickrpc module with mm2 -- rewrritten
# V2. logging module implementation
# V3. check new orders braodcast
# V4. calc outcoming and incoming orders
# V5. test flow:
#  250 times x:
#   - broadcast order
#   - validate order was braodcasted
#  sleep 30s
#   - get amount of orders recieved on 2nd node
#   - compare
#  if 95%+ orders were recieved - network not yet saturated, repeat till more than 5% of orders was lost
#  calculate amount of orders broadcasted / recieved till saturation
# 6. pytest implementation
# 7. Debug me


def init_logs():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler("/log/saturation.log")
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
        res = proxy.electrum(coin=base, servers=servers_base)
        print(res)
        res = proxy.electrum(coin=rel, servers=servers_rel)
        print(res)

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
    if vol2/vol1 >= acceptance:
        return True
    else:
        return False


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
    orders_broadcast = 15  # also sep
    check = True  # init "pass" value
    log.info("Entering main test loop")
    while check:
        log.debug("New iteration, orders to broadcast: %s", str(orders_broadcast))
        for i in range(orders_broadcast):
            log.debug("Order placing num: %s", str(i))
            res = maker.setprice(base=coin_a, rel=coin_b, price='0.1', volume='1')
            log.debug("Response: ", str(res))
            assert res.get('uuid')
        maker_orders = get_orders_amount(maker, coin_a, coin_b).get('amount')
        log.debug("Maker node orders available: ", str(maker_orders))
        # assert maker_orders == orders_broadcast
        taker_orders = get_orders_amount(taker, coin_a, coin_b).get('amount')
        log.debug("Taker node orders available: ", str(taker_orders))
        check = check_saturation(maker_orders, taker_orders)
        log.info("Test iteration finished")
        orders_broadcast += orders_broadcast
    log.info("Test result. Network saturated with orders broadcasted: ", orders_broadcast)


if __name__ == '__main__':
    main()
