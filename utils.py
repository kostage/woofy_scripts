import time
import random
from functools import partial
import random # producing random errors for this example
from tenacity import retry, stop_after_attempt, wait_random


def sleeping(min, max):
	sec = random.randrange(min, max)
	print(f'sleeping {sec} seconds ...')
	time.sleep(sec)


def add_gas_limit(web3, contract_txn):
    multiplier = random.uniform(1.2, 1.5)
    gasLimit = web3.eth.estimate_gas(contract_txn)
    contract_txn['gas'] = int(gasLimit * multiplier)
    return contract_txn


@retry(stop=stop_after_attempt(5), wait=wait_random(min=2, max=5))
def check_status_tx(web3, tx_hash):
    while True:
        status_receipt = web3.eth.get_transaction_receipt(tx_hash)
        status         = status_receipt["status"]
        if status in [0, 1]:
            return status
        time.sleep(1)
