#!/usr/bin/env python
# coding: utf-8
import argparse
from pathlib import Path
import json

from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy


def send_input(data: bytes):
    # Setup connection to the provider
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    acct_0 = w3.eth.account.from_key('0xac0974bec39a17e36ba4a6b4d238ff944bacb47'
                                     '8cbed5efcae784d7bf4f2ff80')

    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct_0))
    w3.eth.set_gas_price_strategy(fast_gas_price_strategy)

    # Setup the representation of the contract
    DEPLOYMENTS_DIR = Path('deployments/localhost/')

    with (DEPLOYMENTS_DIR / 'dapp.json').open('rt') as fin:
        dapp_info = json.load(fin)

    with (DEPLOYMENTS_DIR / 'InputFacet.json').open('rt') as fin:
        input_facet_info = json.load(fin)

    input_contract = w3.eth.contract(
        address=dapp_info['address'],
        abi=input_facet_info['abi'],
    )

    # Send the input
    tx = input_contract.functions.addInput(data).build_transaction(
        {
            'from': acct_0.address,
            'nonce': w3.eth.get_transaction_count(acct_0.address),
        }
    )

    sent = w3.eth.send_transaction(tx)
    print(repr(sent))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=argparse.FileType('rb'))

    args = parser.parse_args()
    input_data = args.input_file.read()

    send_input(input_data)


if __name__ == '__main__':
    main()
