from chains_config import chains_config
from bridges_config import bridges_config


def allowance_bridge(from_bridge, from_network, token, wallet):
    from_bridge_conf = bridges_config[from_bridge]
    from_bridge_chain_conf = from_bridge_conf[from_network]
    from_chain_conf = chains_config[from_network]
    from_bridge_chain_addr = from_bridge_chain_conf['CHAIN_ADDRESS']
    from_token_contract = from_chain_conf['TOKEN_CONTRACTS'][token]
    return from_token_contract.functions.allowance(wallet, from_bridge_chain_addr).call()


def approve_bridge(from_bridge, from_network, token, amount, priv_key):
    from_bridge_conf = bridges_config[from_bridge]
    from_bridge_chain_conf = from_bridge_conf[from_network]
    from_chain_conf = chains_config[from_network]
    from_chain_w3 = from_chain_conf['W3']
    from_bridge_chain_addr = from_bridge_chain_conf['CHAIN_ADDRESS']
    from_token_contract = from_chain_conf['TOKEN_CONTRACTS'][token]

    account = from_chain_w3.eth.account.from_key(priv_key)
    wallet = account.address
    nonce = from_chain_w3.eth.get_transaction_count(wallet)
    gas_price = from_chain_w3.eth.gas_price

    gas_estimate = from_token_contract.functions.approve(from_bridge_chain_addr, amount).estimate_gas({
        'from': wallet,
        'gasPrice': gas_price,
    })
    approve_txn = from_token_contract.functions.approve(from_bridge_chain_addr, amount).build_transaction({
            'from': wallet,
            'gas': int(gas_estimate),
            'gasPrice': gas_price,
            'nonce': nonce,
    })
    signed_approve_txn = from_chain_w3.eth.account.sign_transaction(approve_txn, priv_key)
    approve_txn_hash = from_chain_w3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)
    print(f"{from_network} | {token} APPROVED | {from_chain_conf['SCANNER_TX'].format(approve_txn_hash.hex())} ")

