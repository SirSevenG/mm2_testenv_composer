from testlib.test_utils import init_connection, init_logs, komodo_setgenerate
import time
import requests
import os
import ast
from slickrpc import Proxy
import pytest

success_events = [
    "Started",
    "Negotiated",
    "TakerFeeSent",
    "MakerPaymentReceived",
    "MakerPaymentWaitConfirmStarted",
    "MakerPaymentValidatedAndConfirmed",
    "TakerPaymentSent",
    "TakerPaymentSpent",
    "MakerPaymentSpent",
    "Finished"
]

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


def swap_status_iterator(uuids_list, node_proxy):
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


def check_error(resp, uuid):  # resp - response dictionary
    """prints error message and returns True if response is {"error": "error_message"}"""
    try:
        if resp.get("error"):
            with open(log_path, "a") as log:
                log.write("\n error finding uuid: " + str(uuid) + " response " + str(resp) + "resp.get(error)" +
                          str(resp.get("error")) + "\n")
            time.sleep(5)  # kinda prevents my_swap_status method spam
            return True
        else:
            return False
    except AttributeError:
        return False


def check_swap_status(swaps_dict, node_proxy):
    """iterates events in mm2 response to determine finished(failed or successful) swaps"""
    for uuid in swaps_dict:
        event_occur = []
        try:
            resp = node_proxy.my_swap_status(uuid)
            if check_error(resp, uuid):  # keeps swap status "unknown"
                pass
            else:
                events_list = resp.get("result").get("events")
                for single_event in events_list:
                    event_type = single_event.get("event").get("type")
                    event_occur.append(event_type)
                    if event_type in error_events:
                        logs = ("\nswap failed uuid: " + str(uuid))
                        with open(log_path, "a") as log:
                            log.write(logs)
                        swaps_dict.update({uuid: "failed"})
                        break
                    elif event_type == "Finished":
                        logs = ("\nswap success uuid: " + str(uuid))
                        with open(log_path, "a") as log:
                            log.write(logs)
                        swaps_dict.update({uuid: "success"})
                    else:
                        pass
            logs = ("\nuuid: " + str(uuid) + " event types: " + str(event_occur) + "\n\n")
            with open(log_path, "a") as log:
                log.write(logs)
        except json.decoder.JSONDecodeError:
            logs = ("\nswap failed uuid: " + str(uuid))
            with open(log_path, "a") as log:
                log.write(logs)
            swaps_dict.update({uuid: "failed"})
    return swaps_dict


def test_swaps():
    log = init_logs(logfile="/log/swaps.log")
    nodes = ["mm_seed_a", "mm_seed_b", "mm_seed_c", "mm_seed_d", "mm_swapper_a", "mm_swapper_b"]
    coin_a = "WSG"
    coin_b = "BSG"
    coins = [coin_a, coin_b]
    electrums_a = ["electrum_aa:50001", "electrum_ab:50001"]
    electrums_b = ["electrum_ba:50001", "electrum_bb:50001"]
    userpass = "OHSHITHEREWEGOAGAIN"
    kmd_a_nodes = ["komodo_aa", "komodo_ab"]
    kmd_b_nodes = ["komodo_ba", "komodo_bb"]
    kmd_a_user = "user4234174465"
    kmd_a_pass = "passd6cdd7a0a299fc16ce8431d624c845b3e21f95e06688b80cdad9377936978fdaf9"
    kmd_b_user = "user552075967"
    kmd_b_pass = "pass9ffce55d064e03d3bce1fa5f1aadb91da37805762ba7bc4cad52804b32839a590d"

    log.info("Checking connection to coin nodes")
    komodo_setgenerate(kmd_a_nodes, kmd_a_user, kmd_a_pass)
    komodo_setgenerate(kmd_b_nodes, kmd_b_user, kmd_b_pass)
    log.info("Coin nodes connected, mining enabled")

    rpc = []
    i = 0
    # log.write("\n" + "\n" + "\n" + str(electrum_status_check("electrum_aa:50001")) + "\n" + "\n" + "\n")
    for node in nodes:
        node = "http://" + node + ":7783"
        rpc.append(MMtwo(node, userpass))
        while True:  # Check node is active
            try:
                rpc[i].version()
                break
            except Exception as e:
                logs = ("Retrying connection " + node + "\n error:" + str(e) + "\n")
                with open(log_path, "a") as log:
                    log.write(logs)
                time.sleep(2)
        i += 1
    # Enable BSG and WSG coins on all nodes
    rpc = []
    i = 0
    for node in nodes:
        node = "http://" + node + ":7783"
        rpc.append(MMtwo(node, userpass))
        resp = rpc[i].electrum(coin_a, electrums_a, servers_protocol="TCP", servers_disablecert=True)
        logs = ("pass " + str(i) + " : " + node + " electrum to activate: " + str(electrums_a)
                 + "\n" + "result: " + str(resp) + "\n")
        with open(log_path, "a") as log:
            log.write(logs)
        resp = rpc[i].electrum(coin_b, electrums_b, servers_protocol="TCP", servers_disablecert=True)
        logs = ("pass " + str(i) + " : " + node + " electrum to activate: " + str(electrums_b)
                 + "\n" + "result: " + str(resp) + "\n")
        with open(log_path, "a") as log:
            log.write(logs)
        i += 1
    resp = rpc[-2].setprice(coins[0], coins[1], 1, 100)  # set Alice node
    logs = ("\n" + "\n" + "*"*20 + "\n" + "\n" + "\n" + "Prepare maker" + "\n" + "result: " + str(resp) + "\n")
    with open(log_path, "a") as log:
        log.write(logs)
    time.sleep(10)
    swap_uuids = []
    for i in range(6):
        resp = rpc[-1].buy(coins[0], coins[1], 1, 0.1)
        logs = ("Create order, number: " + str(i) + "\n" + str(resp) + "\n")
        with open(log_path, "a") as log:
            log.write(logs)
        if resp.get("result"):
            swap_uuids.append((resp.get("result")).get("uuid"))
        else:
            swap_uuids.append((resp.get("error")))
        time.sleep(1)
    logs = ("uuids: " + str(swap_uuids) + "\n")
    with open(log_path, "a") as log:
        log.write(logs)
    time.sleep(10)
    with open(log_path, "a") as log:
        log.write("\n" + "\n" + "\n" + "Waiting for swaps to finish" + "\n" + "\n" + "\n")
    result = swap_status_iterator(swap_uuids, rpc[-1])
    with open(log_path, "a") as log:
        log.write("\n." + "\n." + "\n." + "result" + str(result) + "\n." + "\n." + "\n.")
