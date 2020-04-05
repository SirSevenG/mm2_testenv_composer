from .mm2proxy import MMProxy
from slickrpc import Proxy as KMDProxy
from pycurl import error as perror
import time
import os
import logging


def init_logs(logfile="/log/test.log") -> logging:
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
            proxy.electrum(coin=base, servers=servers_base)
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
    try:
        if vol2/vol1 >= acceptance:
            return True
        else:
            return False
    except ZeroDivisionError:
        return False


def komodo_setgenerate(kmd_nodes: list, user: str, passwd: str) -> bool:
    """Waits for komodod nodes to accept connection and enables mining"""
    i = 0
    attempt = 0
    rpc = []
    for node in kmd_nodes:
        node = "http://" + user + ":" + passwd + "@" + node + ":11511"
        rpc.append(KMDProxy(node))
        while attempt < 40:  # Check node is active
            try:
                rpc[i].getinfo()
                break
            except perror as e:
                attempt += 1
                print("Retrying connection %s\n error: %s", node, str(e))
                time.sleep(1)
        if attempt >= 40:
            return False
        rpc[i].setgenerate(True, 1)
    return True


def check_for_errors(resp: dict, uuid: str):  # resp - mm2proxy response dictionary
    """Prints error message and returns True if response is {"error": "error_message"}"""
    try:
        if resp.get("error"):
            print("\n error finding uuid: " + uuid + " response " + str(resp) + "resp.get(error)" +
                  str(resp.get("error")) + "\n")
            return True
        else:
            return False
    except AttributeError:
        return False


def check_swap_status(swaps_dict: dict, node_proxy: MMProxy) -> dict:
    """Iterates events in mm2 response to determine finished(failed or successful) swaps"""
    error_events = [
        "StartFailed",
        "NegotiateFailed",
        "TakerFeeValidateFailed",
        "MakerPaymentTransactionFailed",
        "MakerPaymentDataSendFailed",
        "TakerPaymentValidateFailed",
        "TakerPaymentSpendFailed",
        "MakerPaymentRefunded",
        "MakerPaymentRefundFailed",
        "MakerPaymentValidateFailed",
        "TakerFeeSendFailed"
    ]
    for uuid in swaps_dict:
        event_occur = []
        resp = node_proxy.my_swap_status(params={'uuid': uuid})
        if check_for_errors(resp, uuid):  # keeps swap status "unknown"
            time.sleep(5)  # prevents my_swap_status method spam
            pass
        else:
            events_list = resp.get("result").get("events")
            for single_event in events_list:
                event_type = single_event.get("event").get("type")
                event_occur.append(event_type)
                if event_type in error_events:
                    print("\nswap failed uuid: " + str(uuid))
                    swaps_dict.update({uuid: "failed"})
                    break
                elif event_type == "Finished":
                    print("\nswap success uuid: " + str(uuid))
                    swaps_dict.update({uuid: "success"})
                else:
                    pass
        print("\nuuid: " + str(uuid) + " event types: " + str(event_occur) + "\n\n")
    return swaps_dict


def swap_status_iterator(uuids_list: list, node_proxy: MMProxy) -> dict:
    """Builds swaps statuses dictionary"""
    swaps_d = dict.fromkeys(uuids_list, "unknown")
    while True:
        work_d = {}  # intermediate dictionary to iterate unfinished swaps
        values_list = []
        for key in swaps_d:  # find unfinished swaps
            if swaps_d.get(key) == "unknown":
                work_d.update({key: "unknown"})
        res = check_swap_status(work_d, node_proxy)
        for key in res:  # update values
            swaps_d.update({key: res.get(key)})
            values_list.append(res.get(key))
        if "unknown" not in values_list:  # stop iterator when all swaps are finished
            break
        time.sleep(20)  # check swap statuses trice per minute
    return swaps_d
