import time
from chains_config import chains_config
from stargate_config import stargate_swap_config


def swap(from_network, to_network, token, amount, min_amount, priv_key):
    from_bridge_chain_conf = stargate_swap_config[from_network]
    from_chain_conf = chains_config[from_network]
    from_chain_w3 = from_chain_conf['W3']
    from_bridge_chain_addr = from_bridge_chain_conf['CHAIN_ADDRESS']
    from_bridge_contract = from_bridge_chain_conf['CONTRACT']

    from_token_contract = from_chain_conf['TOKEN_CONTRACTS'][token]

    bridge_to_conf = stargate_swap_config[to_network]
    to_bridge_chain_id = bridge_to_conf['CHAIN_ID']

    account = from_chain_w3.eth.account.from_key(priv_key)
    address = account.address
    nonce = from_chain_w3.eth.get_transaction_count(address)
    gas_price = from_chain_w3.eth.gas_price
    fees = from_bridge_contract.functions.quoteLayerZeroFee(to_bridge_chain_id,
                                                       1,
                                                       "0x0000000000000000000000000000000000000001",
                                                       "0x",
                                                       [0, 0, "0x0000000000000000000000000000000000000001"]
                                                       ).call()
    fee = fees[0]
    print('fee', fee)

    # Check Allowance
    allowance = from_token_contract.functions.allowance(address, from_bridge_chain_addr).call()
    if allowance < amount:
        gas_estimate = from_token_contract.functions.approve(from_bridge_chain_addr, amount).estimate_gas({
            'from': address,
            'gasPrice': gas_price,
        })
        print('allowance gas estimate', gas_estimate)
        approve_txn = from_token_contract.functions.approve(from_bridge_chain_addr, amount).build_transaction({
                'from': address,
                'gas': int(gas_estimate),
                'gasPrice': gas_price,
                'nonce': nonce,
        })
        signed_approve_txn = from_chain_w3.eth.account.sign_transaction(approve_txn, priv_key)
        approve_txn_hash = from_chain_w3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)

        print(f"{from_network} | {token} APPROVED | {from_chain_conf['SCANNER_TX'].format(approve_txn_hash.hex())} ")
        nonce += 1
        time.sleep(5) # wait allowance tx

    token_balance = from_token_contract.functions.balanceOf(address).call()
    print(token, "balance", token_balance)

    if token_balance >= amount:
        # Stargate Swap
        source_pool_id = 1
        dest_pool_id = 1
        refund_address = account.address
        lzTxObj = [0, 0, '0x0000000000000000000000000000000000000001']
        to = account.address
        data = '0x'

        gas_estimate = from_bridge_contract.functions.swap(
            to_bridge_chain_id, source_pool_id, dest_pool_id, refund_address, amount, min_amount, lzTxObj, to, data
        ).estimate_gas({
            'from': address,
            'value': fee,
            'gasPrice': gas_price,
            'nonce': from_chain_w3.eth.get_transaction_count(address),
        })
        print('swap gas estimate', gas_estimate)

        swap_txn = from_bridge_contract.functions.swap(
            to_bridge_chain_id, source_pool_id, dest_pool_id, refund_address, amount, min_amount, lzTxObj, to, data
        ).build_transaction({
            'from': address,
            'value': fee,
            'gas': int(gas_estimate),
            'gasPrice': gas_price,
            'nonce': from_chain_w3.eth.get_transaction_count(address),
        })

        signed_swap_txn = from_chain_w3.eth.account.sign_transaction(swap_txn, priv_key)
        swap_txn_hash = from_chain_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        return from_chain_conf['SCANNER_TX'].format(swap_txn_hash.hex())

    else:
        raise RuntimeError(f"not enough funds, want {amount}, got {token_balance}")
