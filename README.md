# Simualte a swap BlockSec API

Run a realtime simulation for a swap or any transaction, on Ethereum, through [BlockSec API](https://docs.blocksec.com/mopsus/pre-execution-api).

## Install
[Poetry](https://python-poetry.org/) is used to manage the project.

```bash
poetry install
```

## Setup
[BlockSec API](https://docs.blocksec.com/mopsus/pre-execution-api) is used for simulation. Please attain an access token and save it to `.env` in the format given in `.env.example`.

e.g.
```bash
export token=eyJ...-aU
```

then run
```bash
source .env
```
## Run simulation for a swap
Example 
```bash
poetry run simulate_swap/main.py --token_in 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 --token_out 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 --value 1000000000000000000
```

Simulation results are saved to `results` folder. [See example output](results/1673709882.json)

Options for swap simulations:

- `--token_in` - address of token to swap in
- `--token_out` - address of token to swap out
- `--value` - amount of eth to send in (default=0)
- `--amount_in` - amount of token in to swap  (default=0)
- `--sender` - address of sender / receiver of swap (default=heavy-eth-address)
- `--receiver` - address of router (default=open-mev-router)
- `--gas_limit` - first estimate of gas limit (default=1000000)
- `--amount_out_min` - min amount out required (default=0)

Use `--help` for reference.
```bash
poetry run simulate_swap/main.py --help
```