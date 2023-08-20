import json
from chains_config import chains_config


# Chain Ids
POLYGON_CHAIN_ID = 109
ARBITRUM_CHAIN_ID = 110
FANTOM_CHAIN_ID = 112
OPTIMISM_CHAIN_ID = 111
AVALANCHE_CHAIN_ID = 106


stargate_stargate_router_abi = json.load(open('abi/stargate_router_abi.json'))

stargate_polygon_address = chains_config['POLYGON']['W3'].to_checksum_address('0x45A01E4e04F14f7A4a6702c74187c5F6222033cd')
stargate_polygon_contract = chains_config['POLYGON']['W3'].eth.contract(address=stargate_polygon_address, abi=stargate_stargate_router_abi)

stargate_fantom_address = chains_config['FANTOM']['W3'].to_checksum_address('0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6')
stargate_fantom_contract = chains_config['FANTOM']['W3'].eth.contract(address=stargate_fantom_address, abi=stargate_stargate_router_abi)

stargate_arbitrum_address = chains_config['ARBITRUM']['W3'].to_checksum_address('0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614')
stargate_arbitrum_contract = chains_config['ARBITRUM']['W3'].eth.contract(address=stargate_arbitrum_address, abi=stargate_stargate_router_abi)

stargate_optimism_address = chains_config['OPTIMISM']['W3'].to_checksum_address('0xB0D502E938ed5f4df2E681fE6E419ff29631d62b')
stargate_optimism_contract = chains_config['OPTIMISM']['W3'].eth.contract(address=stargate_optimism_address, abi=stargate_stargate_router_abi)

stargate_avalanche_address = chains_config['AVALANCHE']['W3'].to_checksum_address('0x45A01E4e04F14f7A4a6702c74187c5F6222033cd')
stargate_avalanche_contract = chains_config['AVALANCHE']['W3'].eth.contract(address=stargate_avalanche_address, abi=stargate_stargate_router_abi)


stargate_swap_config = {
    'ARBITRUM' : {
        'CHAIN_ID': ARBITRUM_CHAIN_ID,
        'CHAIN_ADDRESS': stargate_arbitrum_address,
        'CONTRACT': stargate_arbitrum_contract,
    },
    'POLYGON' : {
        'CHAIN_ID' : POLYGON_CHAIN_ID,
        'CHAIN_ADDRESS': stargate_polygon_address,
        'CONTRACT': stargate_polygon_contract,
    },
    'FANTOM' : {
        'CHAIN_ID' : FANTOM_CHAIN_ID,
        'CHAIN_ADDRESS': stargate_fantom_address,
        'CONTRACT': stargate_fantom_contract,
    },
    'OPTIMISM' : {
        'CHAIN_ID' : OPTIMISM_CHAIN_ID,
        'CHAIN_ADDRESS': stargate_optimism_address,
        'CONTRACT': stargate_optimism_contract,
    },
    'AVALANCHE' : {
        'CHAIN_ID' : AVALANCHE_CHAIN_ID,
        'CHAIN_ADDRESS': stargate_avalanche_address,
        'CONTRACT': stargate_avalanche_contract,
    }
}