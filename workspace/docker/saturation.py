from testlib.test_utils import init_connection, init_logs, get_orders_amount, check_saturation
import time
import pytest


def test_saturation():
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
    orders_broadcast_init = orders_broadcast = 15
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
        check_str = 'passed' if check else 'failed'  # bool can not be explicitly converted to str
        log.debug("Maker to Taker orders amount check: %s", str(check_str))
        check = check_saturation(orders_broadcast, taker_orders)
        check_str = 'passed' if check else 'failed'
        log.debug("Taker to Created orders amount check: %s", str(check_str))
        log.info("Test iteration finished")
        info_orders = orders_broadcast
        orders_broadcast += orders_broadcast_init
    log.info("Test result. Network saturated with orders broadcasted: %s", str(info_orders))
