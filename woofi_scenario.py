import yaml
from chain_utils import *
from woofi import *


DRY_RUN = True
SWAP_RETRIES = 2
SWAP_RETRY_DELAY_SEC = 15


def usdc_to_ftm():
    privatekey = '0xa85bd409b09bdd77ddab81e632fb2323f0747720f1ffe35afae78a87bf67b70c'
    from_chain = 'FANTOM'
    from_token = 'USDC'
    to_token = ''
    wallet = priv_key_to_address(from_chain, privatekey)
    usdc_balance = balance_raw(from_chain, from_token, wallet)
    print('Raw USDC balance', usdc_balance)
    amount = int(usdc_balance * 0.1)
    woofi_swap(privatekey, from_chain, from_token, to_token, amount)


priv_keys = yaml.safe_load(open('priv_keys.yaml'))


if __name__ == '__main__':
    from_chain = 'ARBITRUM'
    to_chain = 'AVALANCHE'
    from_token = 'USDC'
    to_token = ''
    for key in priv_keys:
        wallet = priv_key_to_address(from_chain, key)
        print('WALLET', wallet)
        gas = gas_balance(from_chain, wallet)
        print(f'Raw GAS balance', gas)
        print(f'USDC balance', balance_raw(from_chain, 'USDC', wallet))
        
        if gas > 0.003:
            continue
        try:
            # tx_link = woofi_bridge(key, from_chain, to_chain, from_token, to_token, int(from_token_balance))
            #woofi_swap(privatekey, chain, from_token, to_token, amount)
            tx_link = woofi_swap(key, from_chain, from_token, to_token, 4000000)
            print(tx_link)
        except:
            print('tx failed')

        sleeping(200, 400)
