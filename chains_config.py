from web3 import Web3
import json


stg_abi = json.load(open('abi/stg_abi.json'))
usdc_abi = json.load(open('abi/usdc_abi.json'))


polygon_rpc_url = 'https://polygon-rpc.com/'
polygon_w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))
usdc_polygon_address = polygon_w3.to_checksum_address('0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174')
usdc_polygon_contract = polygon_w3.eth.contract(address=usdc_polygon_address, abi=usdc_abi)
stg_polygon_address = polygon_w3.to_checksum_address('0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590')
stg_polygon_contract = polygon_w3.eth.contract(address=stg_polygon_address, abi=stg_abi)


fantom_rpc_url = 'https://rpc.ftm.tools/'
fantom_w3 = Web3(Web3.HTTPProvider(fantom_rpc_url))
usdc_fantom_address = fantom_w3.to_checksum_address('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')
usdc_fantom_contract = fantom_w3.eth.contract(address=usdc_fantom_address, abi=usdc_abi)
stg_fantom_address = fantom_w3.to_checksum_address('0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590')
stg_fantom_contract = fantom_w3.eth.contract(address=stg_fantom_address, abi=stg_abi)


arbitrum_rpc_url = 'https://arb1.arbitrum.io/rpc'
arbitrum_w3 = Web3(Web3.HTTPProvider(arbitrum_rpc_url))
usdc_arbitrum_address = arbitrum_w3.to_checksum_address('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8')
usdc_arbitrum_contract = arbitrum_w3.eth.contract(address=usdc_arbitrum_address, abi=usdc_abi)
stg_arbitrum_address = arbitrum_w3.to_checksum_address('0x6694340fc020c5E6B96567843da2df01b2CE1eb6')
stg_arbitrum_contract = arbitrum_w3.eth.contract(address=stg_arbitrum_address, abi=stg_abi)

# optimism_rpc_url = 'https://optimism-mainnet.infura.io/v3/719eddd190804b75b4da25929ac34850'
optimism_rpc_url = 'https://opt-mainnet.g.alchemy.com/v2/s_qHGrSG99VckrTEDH12xYn0nPk3WAld'
optimism_w3 = Web3(Web3.HTTPProvider(optimism_rpc_url))
usdc_optimism_address = optimism_w3.to_checksum_address('0x7f5c764cbc14f9669b88837ca1490cca17c31607')
usdc_optimism_contract = optimism_w3.eth.contract(address=usdc_optimism_address, abi=usdc_abi)


avalanche_rpc_url = 'https://avalanche-mainnet.infura.io/v3/719eddd190804b75b4da25929ac34850'
avalanche_w3 = Web3(Web3.HTTPProvider(avalanche_rpc_url))
usdc_avalanche_address = avalanche_w3.to_checksum_address('0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E')
usdc_avalanche_contract = avalanche_w3.eth.contract(address=usdc_avalanche_address, abi=usdc_abi)


etherium_rpc_url = 'https://mainnet.infura.io/v3/719eddd190804b75b4da25929ac34850'
etherium_w3 = Web3(Web3.HTTPProvider(etherium_rpc_url))
usdc_etherium_address = etherium_w3.to_checksum_address('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')
usdc_etherium_contract = etherium_w3.eth.contract(address=usdc_etherium_address, abi=usdc_abi)


bsc_rpc_url = 'https://bsc-dataseed.binance.org/'
bsc_w3 = Web3(Web3.HTTPProvider(bsc_rpc_url))
usdc_bsc_address = bsc_w3.to_checksum_address('0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d')
usdc_bsc_contract = bsc_w3.eth.contract(address=usdc_bsc_address, abi=usdc_abi)


chains_config = {
    'ARBITRUM' : {
        'GAS': 'ETH',
        'SCANNER_TX': 'https://arbiscan.io/tx/{}',
        'RPC_URL': arbitrum_rpc_url,
        'W3': arbitrum_w3,
        'TOKEN_ADDRESSES' : {
            'USDC': usdc_arbitrum_address,
            'STG': stg_arbitrum_address,
        },
        'TOKEN_CONTRACTS' : {
            'USDC': usdc_arbitrum_contract,
            'STG': stg_arbitrum_contract,
        },
    },
    'POLYGON' : {
        'GAS': 'MATIC',
        'SCANNER_TX': 'https://polygonscan.com/tx/{}',
        'RPC_URL': polygon_rpc_url,
        'W3': polygon_w3,
        'TOKEN_ADDRESSES' : {
            'USDC': usdc_polygon_address,
            'STG': stg_polygon_address,
        },
        'TOKEN_CONTRACTS' : {
            'USDC': usdc_polygon_contract,
            'STG': stg_polygon_contract,
        },
    },
    'FANTOM' : {
        'GAS': 'FTM',
        'SCANNER_TX': 'https://ftmscan.com/tx/{}',
        'RPC_URL': fantom_rpc_url,
        'W3': fantom_w3,
        'TOKEN_ADDRESSES' : {
            'USDC': usdc_fantom_address,
            'STG': stg_fantom_address,
        },
        'TOKEN_CONTRACTS' : {
            'USDC': usdc_fantom_contract,
            'STG': stg_fantom_contract,
        },
    },
    'OPTIMISM' : {
        'GAS': 'ETH',
        'SCANNER_TX': 'https://optimistic.etherscan.io/tx/{}',
        'RPC_URL': optimism_rpc_url,
        'W3': optimism_w3,
        'TOKEN_ADDRESSES' : {
            'USDC': usdc_optimism_address,
        },
        'TOKEN_CONTRACTS' : {
            'USDC': usdc_optimism_contract,
        },
    },
    'AVALANCHE' : {
        'GAS': 'AVAX',
        'SCANNER_TX': 'https://snowtrace.io/tx/{}',
        'RPC_URL': avalanche_rpc_url,
        'W3': avalanche_w3,
        'TOKEN_ADDRESSES' : {
            'USDC': usdc_avalanche_address,
        },
        'TOKEN_CONTRACTS' : {
            'USDC': usdc_avalanche_contract,
        },
    },
    'ETHERIUM' : {
        'GAS': 'ETH',
        'SCANNER_TX': 'https://etherscan.io/tx/{}',
        'RPC_URL': etherium_rpc_url,
        'W3': etherium_w3,
        'TOKEN_ADDRESSES' : {
            'USDC': usdc_etherium_address,
        },
        'TOKEN_CONTRACTS' : {
            'USDC': usdc_etherium_contract,
        },
    },
    'BSC' : {
        'GAS': 'BNB',
        'SCANNER_TX': 'https://bscscan.com/tx/{}',
        'RPC_URL': bsc_rpc_url,
        'W3': bsc_w3,
        'TOKEN_ADDRESSES' : {
            'USDC': usdc_bsc_address,
        },
        'TOKEN_CONTRACTS' : {
            'USDC': usdc_bsc_contract,
        },
    },
}
