# use request blockSec simulation api, save results to file
from dataclasses import dataclass
from typing import List
import json
import time
import requests
import os

# constants
GAS_LIMIT = 1000000
SIMULATE_URL: str = "https://api.blocksec.com/v1/mopsus/prerun/custom"
HEADERS: dict = {
    "Access-Token": os.environ["token"],
    "Content-Type": "application/json",
}  # requires env var token set as api access token

# types


@dataclass
class Transaction:
    """Transaction Data"""

    sender: str  # 20 byte checksummed address
    receiver: str  # 20 byte checksummed address
    gasLimit: int  # gas limit
    gasPrice: str  # gas price
    value: str  # eth value
    input: str  # input data


def unpack_transaction(trans: Transaction) -> dict:

    dTrans: dict = {
        "sender": trans.sender,
        "receiver": trans.receiver,
        "gasLimit": trans.gasLimit,
        "gasPrice": trans.gasPrice,
        "value": trans.value,
        "input": trans.input,
    }
    return dTrans


def simulate_bundle(bundle: List[Transaction]) -> dict:

    data: dict = {
        "chainID": 1,  # currently only working on eth
        "bundle": [unpack_transaction(trans) for trans in bundle],
    }
    print(data)
    resp = requests.post(SIMULATE_URL, json=data, headers=HEADERS)
    output: dict = resp.json()
    print(output)
    # Serializing json
    json_object = json.dumps(output, indent=4)
    # Writing to {$timestamp}.json
    with open(f"results/{str(int(time.time()))}.json", "w") as outfile:
        outfile.write(json_object)
    return output


def get_gas_price() -> int:
    req = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
    t = json.loads(req.content)
    return t["average"] * 10**9
