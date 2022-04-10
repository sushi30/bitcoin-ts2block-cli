import math
import sys

import requests

GENESIS_BLOCK_TS = 1231006505
LATEST_BLOCK_LINK = "https://blockchain.info/latestblock?format=json"
BLOCK_LINK_TEMPLATE = "https://blockchain.info/block-height/{}?format=json"


def get_latest_block():
    return requests.get(LATEST_BLOCK_LINK).json()


def get_block(block_height: int):
    return requests.get(BLOCK_LINK_TEMPLATE.format(block_height)).json()["blocks"][0]


def sign(number):
    return 1 if number >= 0 else -1


def calculate_delta(reference_ts, current_ts, mining_rate=600):
    delta = (current_ts - reference_ts) / mining_rate
    return max(math.floor(abs(delta)), 1) * sign(delta)


def do_nothing(*args, **kwargs):
    pass


def ts2block(ts, debug=False):
    print_ = print if debug else do_nothing
    if ts < GENESIS_BLOCK_TS:
        raise IndexError("No block was created before the genesis block")
    latest_block = get_latest_block()
    calls = 1
    parent_block, child_block = latest_block, None
    avg_mining_rate = (latest_block["time"] - GENESIS_BLOCK_TS) / latest_block["height"]
    if parent_block["time"] <= ts:
        return latest_block["height"]
    while not parent_block["time"] <= ts < child_block["time"]:
        delta = calculate_delta(ts, parent_block["time"], avg_mining_rate)
        next_block_to_check = parent_block["height"] - delta
        parent_block = get_block(next_block_to_check)
        child_block = get_block(next_block_to_check + 1)
        calls += 2
        print_(f"{calls=},{parent_block['height']=},{child_block['height']=}")
    return parent_block["height"]


if __name__ == "__main__":
    timestamp = int(sys.argv[1])
    print(ts2block(timestamp))
