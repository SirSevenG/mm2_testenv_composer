import json
import time
import os
import ast
from mm2rpclib import MMProxy
from pycurl import error as Perror


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

log_path = "/log/log.txt"


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

MM2_USERPASS = 'OHSHITHEREWEGOAGAIN'

def main():
    mm_nodes = ["mm_seed_a", "mm_seed_b", "mm_seed_c", "mm_seed_d", "mm_swapper_a", "mm_swapper_b"]
    mm_proxy = {}

    for node in mm_nodes:  # connect to all mm nodes
        node_params_dictionary = {
            'userpass': MM2_USERPASS,  # userpass to be used in json
            'rpchost': node,
            'rpcport': 7783
        }

        try:
            proxy = MMProxy(node_params_dictionary, timeout=360)
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
            except Perror as e:
                attempt += 1
                print('MM2 does not respond, retrying')
                if attempt >= 15:
                    raise Exception("Connection error ", e)
                else:
                    time.sleep(5)

    # enable coins
    electrums_a = ["electrum_aa:50001", "electrum_ab:50001"]
    electrums_b = ["electrum_ba:50001", "electrum_bb:50001"]
    coin_a = "WSG"
    coin_b = "BSG"
    servers_a = []
    servers_b = []
    for electrum in electrums_a:
        servers_a.append({'url': electrum, 'protocol': 'TCP'})
    for electrum in electrums_b:
        servers_b.append({'url': electrum, 'protocol': 'TCP'})
    for node in mm_nodes:
        proxy = mm_proxy[node]
        res = proxy.electrum(coin=coin_a, servers=servers_a)
        print(res)
        res = proxy.electrum(coin=coin_b, servers=servers_b)
        print(res)
        res = proxy.my_balance(coin='WSG')
        print(res)
        res = proxy.my_balance(coin='BSG')
        print(res)

    # dummy loop to keep container up
    while True:
        pass


if __name__ == "__main__":
    main()
