from typing import List
import eth_abi
import time
from web3 import Web3

# constants
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"


def construct_input(func_selector: str, abi_encoded: bytes) -> str:
    call_hash = Web3.keccak(text=func_selector)
    call_hash_abr = call_hash[0:4].hex()
    input = call_hash_abr + abi_encoded.hex()
    return input


def encode_swap(
    tokenIn: str,
    tokenOut: str,
    amountIn: int,
    amountOutMin: int,
    router: str,
    recipient: str,
) -> List[str]:
    inputs: List[str] = list()
    deadline = int(time.time() + 120000)
    func_selector: str
    abi_encoded: str
    if tokenIn == WETH:
        func_selector = "swapExactETHForTokens(uint256,address[],address,uint256)"
        abi_encoded = eth_abi.encode_abi(
            ["uint256", "address[]", "address", "uint256"],
            [amountOutMin, [tokenIn, tokenOut], recipient, deadline],
        )
        inputs.append(construct_input(func_selector, abi_encoded))
    else:
        func_selector = "approve(address,uint256)"
        abi_encoded = eth_abi.encode_abi(["address", "uint256"], [router, amountIn])
        inputs.append(construct_input(func_selector, abi_encoded))
        if tokenOut == WETH:
            func_selector = "swapExactTokensForETH(uint256,address[],address,uint256)"
        else:
            func_selector = "swapExactTokensForTokens(uint256,address[],address,uint256)"
        abi_encoded = eth_abi.encode_abi(
            ["uint256", "uint256", "address[]", "address", "uint256"],
            [amountIn, amountOutMin, [tokenIn, tokenOut], recipient, deadline],
        )
        inputs.append(construct_input(func_selector, abi_encoded))
    return inputs
