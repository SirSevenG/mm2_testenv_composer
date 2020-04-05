from testlib.test_utils import init_connection, init_logs, komodo_setgenerate, swap_status_iterator
import time
import pytest


def test_swaps():
    """Creates 6 swaps and logs swaps result"""
    log = init_logs()
    nodes = ["mm_seed_a", "mm_seed_b", "mm_seed_c", "mm_seed_d", "mm_swapper_a", "mm_swapper_b"]
    coin_a = "WSG"
    coin_b = "BSG"
    coins = [coin_a, coin_b]
    electrums_a = ["electrum_aa:50001", "electrum_ab:50001"]
    electrums_b = ["electrum_ba:50001", "electrum_bb:50001"]
    userpass = "OHSHITHEREWEGOAGAIN"
    kmd_a_nodes = ["komodo_aa:11511", "komodo_ab:11511"]
    kmd_b_nodes = ["komodo_ba:8465", "komodo_bb:8465"]
    kmd_a_user = "user4234174465"
    kmd_a_pass = "passd6cdd7a0a299fc16ce8431d624c845b3e21f95e06688b80cdad9377936978fdaf9"
    kmd_b_user = "user552075967"
    kmd_b_pass = "pass9ffce55d064e03d3bce1fa5f1aadb91da37805762ba7bc4cad52804b32839a590d"

    log.info("Checking connection to coin nodes")
    assert komodo_setgenerate(kmd_a_nodes, kmd_a_user, kmd_a_pass)
    assert komodo_setgenerate(kmd_b_nodes, kmd_b_user, kmd_b_pass)
    log.info("Coin nodes connected, mining enabled")

    log.info("Connecting MM2 nodes and enabling swap coins")
    proxy_dict = init_connection(userpass, nodes, electrums_a, electrums_b, coin_a, coin_b)
    log.info("MM2 nodes connected, preparing maker order")
    resp = proxy_dict.get('mm_swapper_a').setprice(base=coins[0], rel=coins[1], prcie='1', volume='100')
    time.sleep(30)  # time to propagate maker order
    log.debug("Maker order created: %s", str(resp))
    swap_uuids = []
    for i in range(6):
        resp = proxy_dict.get('mm_swapper_b').buy(base=coins[0], rel=coins[1], price='1', volume='0.1')
        log.debug("Create order, number: %s\n%s", str(i), str(resp))
        if resp.get("result"):
            swap_uuids.append((resp.get("result")).get("uuid"))
        else:
            swap_uuids.append((resp.get("error")))
        time.sleep(10)
    log.debug("uuids: %s", str(swap_uuids))
    time.sleep(10)
    log.info("Waiting for swaps to finish")
    result = swap_status_iterator(swap_uuids, proxy_dict.get('mm_swapper_b'))
    log.info("Test result: %s", str(result))
