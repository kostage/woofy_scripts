from web3 import Web3
import requests
import datetime
import time
import json
import random
import sys
from tenacity import retry, stop_after_attempt, wait_random
from utils import sleeping, check_status_tx, add_gas_limit
from chain_utils import *
from chains_config import chains_config


base_url = f'https://api.1inch.io/v5.0/{}' # arg0 - chainId


@retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
def get_api_call_data(url):
    try:
        call_data = requests.get(url)
        api_data = call_data.json()
        return api_data
    except Exception as e:
        print(e)
        raise(e)


def api_1inch_is_stable(network):
    w3 = chains_config[network]['W3']
    _1inchurl = f'{base_url.format(w3.eth.chain_id)}/healthcheck'
    json_data = get_api_call_data(_1inchurl)

    if json_data['status'] == 'OK':
        return True

    print(f'\nAPI 1inch не доступно! Дальнейшая работа не возможна!', 'red')
    return False


def inch_swap(network, from_token, to_token, amount, private_key):

    if not api_1inch_is_stable():
        raise RuntimeError('1inch healthcheck failed')

    now = datetime.datetime.now()
    now_dt = now.strftime("%d-%m-%Y %H:%M")
    wallet = priv_key_to_address(network, private_key)

    chain_conf = chains_config[network]
    w3 = chain_conf['W3']

    from_token_addr = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    allowance = amount
    if from_token != '':
        from_token_addr = chain_conf['TOKEN_ADDRESSES'][from_token]
        allowance = inch_allowance(network, from_token_addr, wallet)

    to_token_addr = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    if to_token != '':
        to_token_addr = chain_conf['TOKEN_ADDRESSES'][to_token]
    slippage = '0.5'

    try:
        if int(allowance) <= amount:
            state = inch_approve(network, private_key, from_token, wallet)
            if not state:
                return state
            else:
                sleeping(15, 30)

        _1inchurl = f'{base_url}/swap?fromTokenAddress={from_token_addr}&toTokenAddress={to_token_addr}&amount={amount}&fromAddress={wallet}&slippage={slippage}'
        json_data = get_api_call_data(_1inchurl)

        tx = json_data['tx']
        tx['nonce'] = w3.eth.get_transaction_count(wallet)
        tx['to'] = w3.toChecksumAddress(tx['to'])
        tx['gasPrice'] = int(tx['gasPrice'])
        tx['value'] = int(tx['value'])
        signed_tx = w3.eth.account.signTransaction(tx, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_text = tx_hash.hex()

        print(f"\n{now_dt} {wallet} | УСПЕШНО обмен {amount} {from_token} на {to_token} tx {chain_conf['SCANNER_TX'].format(txn_text)}")
        return True

    except Exception as e:
        error_str = f'\n{now_dt} {wallet} | НЕУДАЧНО обмен {amount} {from_token} на {to_token} | {e}'
        if 'description' in json_data.keys():
            error_des = json_data['description']
            error_str += f'| {error_des}'

        print(error_str)
        return False


def inch_approve(network, private_key, from_token, wallet):

    now = datetime.datetime.now()
    now_dt = now.strftime("%d-%m-%Y %H:%M")

    chain_conf = chains_config[network]
    w3 = chain_conf['W3']

    from_token_addr = chain_conf['TOKEN_ADDRESSES'][from_token]

    try:
        _1inchurl = f'{base_url.format(w3.eth.chain_id)}/approve/transaction?tokenAddress={from_token_addr}'
        tx = get_api_call_data(_1inchurl)

        tx['gasPrice'] = int(tx['gasPrice'])
        tx['from'] = Web3.toChecksumAddress(wallet)
        tx['to'] = Web3.toChecksumAddress(tx['to'])
        tx['value'] = int(tx['value'])
        tx['nonce'] = w3.eth.get_transaction_count(wallet)

        # Если транза зафейлится, можно попробовать код ниже, увеличит на 25% объем газа который рекомендует сеть
        # можно применять в любой функции и контракте, оставляю здесь для заметки
        estimate = w3.eth.estimate_gas(tx)
        gas_limit = estimate
        # gas_limit = int(estimate + estimate * 0.25)
        tx['gas'] = gas_limit

        signed_tx = w3.eth.account.signTransaction(tx, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_text = tx_hash.hex()
        
        print(f"\n{now_dt} {wallet} | УСПЕШНО апрув на 1inch {from_token} tx {chain_conf['SCANNER_TX'].format(txn_text)}")
        return True

    except Exception as e:
        error_str = f'\n{now_dt} {wallet} | НЕУДАЧНО апрув на 1inch {from_token} | {e}'
        if 'description' in tx.keys():
            error_des = tx['description']
            error_str += f'| {error_des}'

        print(error_str, 'red')
        return False


def inch_allowance(network, from_token_addr, wallet):
    w3 = chains_config[network]['W3']
    _1inchurl = f'{base_url.format(w3.eth.chain_id)}/approve/allowance?tokenAddress={from_token_addr}&walletAddress={wallet}'
    json_data = get_api_call_data(_1inchurl)
    out_allowance = None

    if 'allowance' in json_data.keys():
        out_allowance = json_data['allowance']

    return out_allowance
