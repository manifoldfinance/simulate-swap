#!/usr/bin/env python

import argparse
from utils.encode_swap import encode_swap
from utils.simulate import Transaction, get_gas_price, simulate_bundle, GAS_LIMIT
from typing import List
import logging
import sys

logging.basicConfig(level=logging.DEBUG)

# input arguments
parser = argparse.ArgumentParser(description="Transaction details to simulate")
parser.add_argument(
    "--sender",
    type=str,
    nargs="?",
    help="Sender or list of sender address(es)",
    default="0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8",
)
parser.add_argument(
    "--receiver",
    type=str,
    nargs="?",
    help="Receiver or list of receiver address(es)",
    default="0x484Ec09481EFE676875490a97583e1bEa81379AD",
)
parser.add_argument("--input", type=str, nargs="?", help="Input or list of input data")
parser.add_argument("--value", type=int, nargs="?", help="Value or list of values (optional)", default=0)
parser.add_argument(
    "--gas_limit",
    type=int,
    nargs="?",
    help="Gas limit or list of gas limits (optional)",
    default=GAS_LIMIT,
)
parser.add_argument(
    "--token_in",
    type=str,
    nargs="?",
    help="TokenIn to swap (optional)",
)
parser.add_argument(
    "--token_out",
    type=str,
    nargs="?",
    help="TokenOut to swap (optional)",
)
parser.add_argument("--amount_in", type=int, nargs="?", help="Amount in to swap (optional)", default=0)
parser.add_argument(
    "--amount_out_min",
    type=int,
    nargs="?",
    help="Amount out min for swap (optional)",
    default=0,
)
args = parser.parse_args()

if __name__ == "__main__":
    logging.info("Parsing arguments")
    bundle: List[Transaction] = list()
    gas_price: str = str(get_gas_price())
    # either inputs are supplied or token in and token out
    if args.input:
        logging.info("Input given directly. Constructing bundle")
        bundle.append(
            Transaction(
                args.sender,
                args.receiver,
                args.gas_limit,
                gas_price,
                str(args.value),
                args.input,
            )
        )
        logging.debug("Bundle constructed")
    elif args.token_in and args.token_out:
        logging.info("Swap details given. Constructing bundle")
        inputs: List[str] = encode_swap(
            args.token_in,
            args.token_out,
            args.amount_in,
            args.amount_out_min,
            args.receiver,
            args.sender,
        )
        # print(inputs)
        inputs_len: int = len(inputs)
        if inputs_len == 2:
            # approve first
            bundle.append(
                Transaction(
                    args.sender,
                    args.token_in,
                    args.gas_limit,
                    gas_price,
                    "0",
                    inputs[0],
                )
            )
            bundle.append(
                Transaction(
                    args.sender,
                    args.receiver,
                    args.gas_limit,
                    gas_price,
                    str(args.value),
                    inputs[1],
                )
            )
        else:
            bundle.append(
                Transaction(
                    args.sender,
                    args.receiver,
                    args.gas_limit,
                    gas_price,
                    str(args.value),
                    inputs[0],
                )
            )

        logging.debug("Bundle constructed")
    else:
        logging.error("Unrecognized arguments given")
        sys.exit()

    print(simulate_bundle(bundle))
