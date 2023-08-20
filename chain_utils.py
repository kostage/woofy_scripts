from chains_config import chains_config


def balance_raw(network, token, wallet):
    from_conf = chains_config[network]
    from_token_contract = from_conf['TOKEN_CONTRACTS'][token]
    return from_token_contract.functions.balanceOf(wallet).call()


def balance(network, token, wallet):
    return balance_raw(network, token, wallet)


def gas_balance_raw(network, wallet):
    from_conf = chains_config[network]
    from_w3 = from_conf['W3']
    balance = from_w3.eth.get_balance(wallet)
    # Convert balance to Ether and print
    return balance


def allowance_native(network, wallet):
    from_conf = chains_config[network]
    from_w3 = from_conf['W3']
    allowance = from_w3.eth.allowance(wallet)
    # Convert balance to Ether and print
    return allowance
   

def gas_balance(network, wallet):
    from_conf = chains_config[network]
    from_w3 = from_conf['W3']
    # Convert balance to Ether and print
    raw_balance = gas_balance_raw(network, wallet)
    balance = float(from_w3.from_wei(raw_balance, 'ether'))
    return balance


def priv_key_to_address(network, priv_key):
    from_conf = chains_config[network]
    from_w3 = from_conf['W3']
    account = from_w3.eth.account.from_key(priv_key)
    return account.address
