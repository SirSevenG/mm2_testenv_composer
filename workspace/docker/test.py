import json
import time
import os
import ast
import ujson
from io import BytesIO as StringIO
from slickrpc.exc import RpcException
from itertools import count
from pycurl import Curl
from pycurl import error as Perror


# TODO: and logic for test
# 1. check slickrpc module with mm2
# 2. loggin module implementation
# 3. check new orders braodcast
# 4. calc outcoming and incoming orders
# 5. test flow:
#  250 times x:
#   - broadcast order
#   - validate order was braodcasted
#  sleep 30s
#   - get amount of orders recieved on 2nd node
#   - compare
#  if 95%+ orders were recieved - network not yet saturated, repeat till more than 5% of orders was lost
#  calculate amount of orders broadcasted / recieved till saturation


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


DEFAULT_HTTP_TIMEOUT = 120
DEFAULT_RPC_PORT = 7783
MM2_USERPASS = 'OHSHITHEREWEGOAGAIN'


class MMProxy(object):
    _ids = count(0)

    def __init__(self, conf_dict=None, timeout=DEFAULT_HTTP_TIMEOUT):
        self.config = conf_dict
        self.userpass = conf_dict.get('userpass')
        if not conf_dict.get('rpcport'):
            self.config['rpcport'] = DEFAULT_RPC_PORT
        self.conn = self.prepare_connection(self.config, timeout=timeout)

    def __getattr__(self, method):
        conn = self.conn
        id = next(self._ids)
        upass = self.userpass

        def call(**params):
            post_dict = {
                'jsonrpc': '2.0',
                'userpass': upass,
                'method': method,
                'id': id
            }
            for param, value in params.items():
                post_dict.update({param: value})
            postdata = ujson.dumps(post_dict)
            body = StringIO()
            conn.setopt(conn.WRITEFUNCTION, body.write)
            conn.setopt(conn.POSTFIELDS, postdata)
            print(postdata)
            conn.perform()
            try:
                resp = ujson.loads(body.getvalue())
                print('\n\n', type(resp), '\n\n')
            except ValueError:
                resp = str(body.getvalue().decode('utf=8'))
            return resp

        return call

    @classmethod
    def prepare_connection(cls, conf, timeout=DEFAULT_HTTP_TIMEOUT):
        url = 'http://%s:%s' % (conf['rpchost'], conf['rpcport'])
        conn = Curl()
        conn.setopt(conn.CONNECTTIMEOUT, timeout)
        conn.setopt(conn.TIMEOUT, timeout)
        conn.setopt(conn.URL, url)
        conn.setopt(conn.POST, 1)
        return conn


def main():

    node_params_dictionary = {
        'userpass': MM2_USERPASS,  # userpass to be used in json
        'rpchost': 'mm_swapper_a',
        'rpcport': 7783
    }

    try:
        proxy = MMProxy(node_params_dictionary, timeout=360)
    except ConnectionAbortedError as e:
        raise Exception("Connection error! Probably no daemon on selected port. Error: ", e)

    while True:
        try:
            res = proxy.help()
            print(res)
            break
        except Perror:
            print('MM2 does not respond yet')
    res = proxy.my_balance('WSG')
    print(res)
    res = proxy.my_balance('BSG')
    print(res)


if __name__ == "__main__":
    main()
