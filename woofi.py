import random
from utils import sleeping, check_status_tx, add_gas_limit
from chains_config import chains_config
from swap_utils import allowance_swap, approve_swap
from bridge_utils import allowance_bridge, approve_bridge
from woofi_config import woofi_swap_config, woofi_bridge_config
from stargate_config import stargate_swap_config
from tenacity import retry, stop_after_attempt, wait_random


slippage = 0.95


def woofi_swap(privatekey, chain, from_token, to_token, amount):
    woofi_swap_contract = woofi_swap_config[chain]['CONTRACT']
    chain_conf = chains_config[chain]
    chain_w3 = chain_conf['W3']

    wallet = chain_w3.eth.account.from_key(privatekey).address

    if from_token != '':
        allowance_amount = allowance_swap('WOOFI', chain, from_token, wallet)
        if amount > allowance_amount:
            approve_swap('WOOFI', chain, from_token, amount, privatekey)
            sleeping(5, 10)
    to_token_address = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    from_token_address = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    value = amount
    if to_token != '' : to_token_address = chain_conf['TOKEN_ADDRESSES'][to_token]
    if from_token != '' :
        from_token_address = chain_conf['TOKEN_ADDRESSES'][from_token]
        value = 0
    minToAmount = woofi_get_min_swap_amount(chain, from_token_address, to_token_address, amount)

    transaction = {
        'from': wallet,
        'nonce': chain_w3.eth.get_transaction_count(wallet),
        'value': value,
        'gasPrice': chain_w3.eth.gas_price,
        'gas': 0,
    }

    contract_txn = woofi_swap_contract.functions.swap(
        from_token_address,
        to_token_address,
        amount,
        int(minToAmount * slippage),
        wallet,
        wallet
    ).build_transaction(transaction)

    add_gas_limit(chain_w3, contract_txn)

    signed_tx = chain_w3.eth.account.sign_transaction(contract_txn, privatekey)
    raw_tx_hash = chain_w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = chain_w3.to_hex(raw_tx_hash)

    print(chain_conf['SCANNER_TX'].format(tx_hash))
    print('polling status')
    status = check_status_tx(chain_w3, tx_hash)
    if status == 1:
        print('tx succeeded')
    else:
        print('tx failed')


@retry(stop=stop_after_attempt(2), wait=wait_random(min=60, max=120))
def woofi_bridge(privatekey, from_chain, to_chain, from_token, to_token, amount):
    woofi_bridge_contract = woofi_bridge_config[from_chain]['CONTRACT']
    from_chain_conf = chains_config[from_chain]
    from_chain_w3 = from_chain_conf['W3']

    to_chain_conf = chains_config[to_chain]

    wallet = from_chain_w3.eth.account.from_key(privatekey).address

    if from_token != '':
        allowance_amount = allowance_bridge('WOOFI', from_chain, from_token, wallet)
        if amount > allowance_amount:
            approve_bridge('WOOFI', from_chain, from_token, amount, privatekey)
            sleeping(5, 10)

    to_token_address = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    from_token_address = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    value = amount
    if to_token != '' : to_token_address = to_chain_conf['TOKEN_ADDRESSES'][to_token]
    if from_token != '' :
        from_token_address = from_chain_conf['TOKEN_ADDRESSES'][from_token]
        value = 0

    from_bridge_token_address = from_chain_conf['TOKEN_ADDRESSES']['USDC']
    min_from_bridge_amount = woofi_get_min_swap_amount(from_chain, from_token_address, from_bridge_token_address, amount)
    if min_from_bridge_amount is None:
        print('min_from_bridge_amount is set to zero')
        min_from_bridge_amount = 0

    print('min_from_bridge_amount', min_from_bridge_amount)

    srcInfos = [
        from_token_address,
        from_bridge_token_address,
        amount,
        int(min_from_bridge_amount * 0.7),
    ]

    to_bridge_token_address = to_chain_conf['TOKEN_ADDRESSES']['USDC']
    to_chain_id = stargate_swap_config[to_chain]['CHAIN_ID']
    min_to_bridge_amount = woofi_get_min_swap_amount(to_chain, to_bridge_token_address, to_token_address, amount)
    if min_to_bridge_amount is None:
        print('min_to_bridge_amount is set to zero')
        min_to_bridge_amount = 0
    print('min_to_bridge_amount', min_to_bridge_amount)

    dstInfos = [
        to_chain_id,
        to_token_address,
        to_bridge_token_address,
        int(min_to_bridge_amount * 0.7),
        0               # airdropNativeAmount
    ]

    fees = woofi_bridge_contract.functions.quoteLayerZeroFee(
        random.randint(112101680502565000, 712101680502565000), # refId
        wallet, # to
        srcInfos, 
        dstInfos
    ).call()
    print('fees', fees)
    value += int(fees[0])

    contract_txn = woofi_bridge_contract.functions.crossSwap(
        random.randint(112101680502565000, 712101680502565000), # refId
        wallet, # to
        srcInfos, 
        dstInfos
        ).build_transaction(
        {
            'from': wallet,
            'nonce': from_chain_w3.eth.get_transaction_count(wallet),
            'value': value,
            'gasPrice': from_chain_w3.eth.gas_price,
            'gas': 0,
        }
    )
    contract_txn = add_gas_limit(from_chain_w3, contract_txn)

    signed_tx = from_chain_w3.eth.account.sign_transaction(contract_txn, privatekey)
    raw_tx_hash = from_chain_w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = from_chain_w3.to_hex(raw_tx_hash)

    status = check_status_tx(from_chain_w3, tx_hash)
    if status == 1:
        print('tx succeeded')
    else:
        print('tx failed')
    tx_link = from_chain_conf['SCANNER_TX'].format(tx_hash)
    return tx_link


@retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
def do_woofi_get_min_swap_amount(chain, from_token_addr, to_token_addr, amount):
    if from_token_addr == to_token_addr:
        return amount
    woofi_contract = woofi_swap_config[chain]['CONTRACT']

    minToAmount = woofi_contract.functions.tryQuerySwap(
        from_token_addr, to_token_addr, amount,
    ).call()
    return minToAmount


def woofi_get_min_swap_amount(chain, from_token_addr, to_token_addr, amount):
    try:
        return do_woofi_get_min_swap_amount(chain, from_token_addr, to_token_addr, amount)
    except Exception as e:
        print(e)
        return None
