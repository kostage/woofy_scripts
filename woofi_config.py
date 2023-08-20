from web3 import Web3
from chains_config import chains_config
from abi.woofi_abi import ABI_WOOFI_BRIDGE, ABI_WOOFI_SWAP


# BRIDGE
woofi_fantom_bridge_address = chains_config['FANTOM']['W3'].to_checksum_address('0x72dc7fa5eeb901a34173C874A7333c8d1b34bca9')
woofi_fantom_bridge_contract = chains_config['FANTOM']['W3'].eth.contract(address=woofi_fantom_bridge_address, abi=ABI_WOOFI_BRIDGE)

woofi_polygon_bridge_address = chains_config['POLYGON']['W3'].to_checksum_address('0x45A01E4e04F14f7A4a6702c74187c5F6222033cd')
woofi_polygon_bridge_contract = chains_config['POLYGON']['W3'].eth.contract(address=woofi_polygon_bridge_address, abi=ABI_WOOFI_BRIDGE)

woofi_avalanche_bridge_address = chains_config['AVALANCHE']['W3'].to_checksum_address('0x51AF494f1B4d3f77835951FA827D66fc4A18Dae8')
woofi_avalanche_bridge_contract = chains_config['AVALANCHE']['W3'].eth.contract(address=woofi_avalanche_bridge_address, abi=ABI_WOOFI_BRIDGE)

woofi_ethereum_bridge_address = chains_config['ETHERIUM']['W3'].to_checksum_address('0x9D1A92e601db0901e69bd810029F2C14bCCA3128')
woofi_etherium_bridge_contract = chains_config['ETHERIUM']['W3'].eth.contract(address=woofi_ethereum_bridge_address, abi=ABI_WOOFI_BRIDGE)

woofi_bsc_bridge_address = chains_config['BSC']['W3'].to_checksum_address('0x81004C9b697857fD54E137075b51506c739EF439')
woofi_bsc_bridge_contract = chains_config['BSC']['W3'].eth.contract(address=woofi_bsc_bridge_address, abi=ABI_WOOFI_BRIDGE)

woofi_arbitrum_bridge_address = chains_config['ARBITRUM']['W3'].to_checksum_address('0x4AB421de52b3112D02442b040dd3DC73e8Af63b5')
woofi_arbitrum_bridge_contract = chains_config['ARBITRUM']['W3'].eth.contract(address=woofi_arbitrum_bridge_address, abi=ABI_WOOFI_BRIDGE)

woofi_optimism_bridge_address = chains_config['OPTIMISM']['W3'].to_checksum_address('0xbeae1b06949d033da628ba3e5af267c3e740494b')
woofi_optimism_bridge_contract = chains_config['OPTIMISM']['W3'].eth.contract(address=woofi_optimism_bridge_address, abi=ABI_WOOFI_BRIDGE)


# SWAP
woofi_avalanche_swap_address = chains_config['AVALANCHE']['W3'].to_checksum_address('0xC22FBb3133dF781E6C25ea6acebe2D2Bb8CeA2f9')
woofi_avalanche_swap_contract = chains_config['AVALANCHE']['W3'].eth.contract(address=woofi_avalanche_swap_address, abi=ABI_WOOFI_SWAP)

woofi_polygon_swap_address = chains_config['POLYGON']['W3'].to_checksum_address('0x817Eb46D60762442Da3D931Ff51a30334CA39B74')
woofi_polygon_swap_contract = chains_config['POLYGON']['W3'].eth.contract(address=woofi_polygon_swap_address, abi=ABI_WOOFI_SWAP)

woofi_ethereum_swap_address = chains_config['ETHERIUM']['W3'].to_checksum_address('0x9D1A92e601db0901e69bd810029F2C14bCCA3128')
woofi_etherium_swap_contract = chains_config['ETHERIUM']['W3'].eth.contract(address=woofi_ethereum_swap_address, abi=ABI_WOOFI_SWAP)

woofi_bsc_swap_address = chains_config['BSC']['W3'].to_checksum_address('0x4f4Fd4290c9bB49764701803AF6445c5b03E8f06')
woofi_bsc_swap_contract = chains_config['BSC']['W3'].eth.contract(address=woofi_bsc_swap_address, abi=ABI_WOOFI_SWAP)

woofi_arbitrum_swap_address = chains_config['ARBITRUM']['W3'].to_checksum_address('0x9aed3a8896a85fe9a8cac52c9b402d092b629a30')
woofi_arbitrum_swap_contract = chains_config['ARBITRUM']['W3'].eth.contract(address=woofi_arbitrum_swap_address, abi=ABI_WOOFI_SWAP)

woofi_optimism_swap_address = chains_config['OPTIMISM']['W3'].to_checksum_address('0xEAf1Ac8E89EA0aE13E0f03634A4FF23502527024')
woofi_optimism_swap_contract = chains_config['OPTIMISM']['W3'].eth.contract(address=woofi_optimism_swap_address, abi=ABI_WOOFI_SWAP)

woofi_fantom_swap_address = chains_config['FANTOM']['W3'].to_checksum_address('0x382A9b0bC5D29e96c3a0b81cE9c64d6C8F150Efb')
woofi_fantom_swap_contract = chains_config['FANTOM']['W3'].eth.contract(address=woofi_fantom_swap_address, abi=ABI_WOOFI_SWAP)


# через что бриджим на woofi (usdc / usdt)
WOOFI_PATH = {
    'avalanche'     : '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
    'polygon'       : '0x2791bca1f2de4661ed88a30c99a7a9449aa84174',
    'ethereum'      : '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    'bsc'           : '0x55d398326f99059ff775485246999027b3197955',
    'arbitrum'      : '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
    'optimism'      : '0x7f5c764cbc14f9669b88837ca1490cca17c31607',
    'fantom'        : '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75',
}


woofi_bridge_config = {
    'ARBITRUM' : {
        'CHAIN_ADDRESS': woofi_arbitrum_bridge_address,
        'CONTRACT': woofi_arbitrum_bridge_contract,
    },
    'POLYGON' : {
        'CHAIN_ADDRESS': woofi_polygon_bridge_address,
        'CONTRACT': woofi_polygon_bridge_contract,
    },
    'FANTOM' : {
        'CHAIN_ADDRESS': woofi_fantom_bridge_address,
        'CONTRACT': woofi_fantom_bridge_contract,
    },
    'OPTIMISM' : {
        'CHAIN_ADDRESS': woofi_optimism_bridge_address,
        'CONTRACT': woofi_optimism_bridge_contract,
    },
    'AVALANCHE' : {
        'CHAIN_ADDRESS': woofi_avalanche_bridge_address,
        'CONTRACT': woofi_avalanche_bridge_contract,
    }
}

woofi_swap_config = {
    'ARBITRUM' : {
        'CHAIN_ADDRESS': woofi_arbitrum_swap_address,
        'CONTRACT': woofi_arbitrum_swap_contract,
    },
    'POLYGON' : {
        'CHAIN_ADDRESS': woofi_polygon_swap_address,
        'CONTRACT': woofi_polygon_swap_contract,
    },
    'FANTOM' : {
        'CHAIN_ADDRESS': woofi_fantom_swap_address,
        'CONTRACT': woofi_fantom_swap_contract,
    },
    'OPTIMISM' : {
        'CHAIN_ADDRESS': woofi_optimism_swap_address,
        'CONTRACT': woofi_optimism_swap_contract,
    },
    'AVALANCHE' : {
        'CHAIN_ADDRESS': woofi_avalanche_swap_address,
        'CONTRACT': woofi_avalanche_swap_contract,
    }
}
