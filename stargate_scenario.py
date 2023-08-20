import json
import yaml
import time
import random
from chain_utils import balance, gas_balance
from chains_config import chains_config
from stargate import *


DRY_RUN = True
SWAP_RETRIES = 2
SWAP_RETRY_DELAY_SEC = 15

swappable_tokens = ['USDC']

ACTIVE_NETWORKS = [
    'ARBITRUM',
    # 'POLYGON',
    # 'FANTOM',
    'OPTIMISM',
    # 'AVALANCHE',
]

active_stargate_conf = {net:conf for (net, conf) in stargate_swap_config.items() if net in ACTIVE_NETWORKS}
active_chains_conf = {net:conf for (net, conf) in chains_config.items() if net in ACTIVE_NETWORKS}


priv_keys = yaml.safe_load(open('priv_keys.yaml'))

def print_dict(d):
    print(json.dumps(d, sort_keys=True, indent=4))


def wallet_balances(wallet):
    return {net:{token:balance(net, token, wallet)
                for token in netconf['TOKEN_CONTRACTS'].keys()} 
                for (net,netconf) in active_chains_conf.items()}


def wallet_gas_balances(wallet):
        return {net:{netconf['GAS']:gas_balance(net, wallet)} 
               for (net,netconf) in active_chains_conf.items()}


def possible_swaps(priv_key, balances, gas):
    nonzero_tokens = {net:{token:token_bal
                for (token, token_bal) in token_balances.items() if token_bal > 0}
                for (net,token_balances) in balances.items()}

    nonzero_tokens = {net:token_balances for (net,token_balances) in nonzero_tokens.items() if len(token_balances) > 0}

    nonzero_tokens_swappable = {net:{token:token_bal
                for (token, token_bal) in token_balances.items() if token in swappable_tokens}
                for (net,token_balances) in nonzero_tokens.items()}
    
    def netgas(net):
        net_gas_name = active_chains_conf[net]['GAS']
        return gas[net][net_gas_name]

    swaps = []
    for net, tokens in nonzero_tokens_swappable.items():
        for token, balance in tokens.items():
            for dest_net in [dest_net for dest_net in active_chains_conf.keys() if dest_net != net]:
                swap = {}
                swap['WALLET'] = priv_key_to_address(priv_key)
                swap['NET'] = net
                swap['TOKEN'] = token
                swap['BALANCE'] = balance
                swap['GAS'] = netgas(net)
                swap['DEST_NET'] = dest_net
                if swap['GAS'] == 0:
                    print('not enough gas on', net)
                    continue
                swaps.append(swap)
    return swaps
    

def swap_decision(possible_swaps):
    if len(possible_swaps) == 0:
        return None
    return random.choice(possible_swaps)

def fulfill_swap(swap_args, key):
    def op():
        try:
            tx_scan = swap(
                    swap_args['NET'],
                    swap_args['DEST_NET'],
                    swap_args['TOKEN'], 
                    int(swap_args['BALANCE'] * 0.5), 
                    int(swap_args['BALANCE'] * 0.4), 
                    key,
                )
        except Exception as e:
            swap_args['ERROR'] = str(e)
            return swap_args

        swap_args['TX_SCAN'] = tx_scan
        return swap_args
    res = swap_args
    for i in range(SWAP_RETRIES):
        res = op()
        if res.get('ERROR') == None:
            break
        print('swap failed:', res['ERROR'])
        time.sleep(SWAP_RETRY_DELAY_SEC)

    return res


def priv_key_to_address(priv_key):
    from_conf = active_chains_conf[ACTIVE_NETWORKS[0]]
    from_w3 = from_conf['W3']
    account = from_w3.eth.account.from_key(priv_key)
    return account.address

def do_swap(key, dry_run):
    wallet = priv_key_to_address(key)
    print('<<<', wallet, '>>>')
    print('<<<', 'ACCOUNT BALANCES', '>>>')
    balances = wallet_balances(wallet)
    print_dict(balances)

    print('<<<', 'ACCOUNT GAS', '>>>')
    gas = wallet_gas_balances(wallet)
    print_dict(gas)
    all_swaps = possible_swaps(key, balances, gas)

    print('<<<', 'POSSIBLE SWAPS', '>>>')
    print_dict(all_swaps)

    print('<<<', 'SELECTING RANDOM SWAP', '>>>')
    swap = swap_decision(all_swaps)
    if swap is None:
        print('no swap found')
        return None
    print_dict(swap)
    if not dry_run:
        print('<<<', 'TRYING TO SWAP', '>>>')
        swapped = fulfill_swap(swap, key)
        return swapped
    print('')
    print('')


if __name__ == '__main__':
    sec = 0
    for key in priv_keys:
        swapped = do_swap(key, DRY_RUN)
        if swapped is not None:
            print_dict(swapped)
        else:
            print('nothing has been swapped')
            continue
        sec = random.randrange(120, 240)
        print(f'sleeping {sec} seconds ...')
        time.sleep(sec)
