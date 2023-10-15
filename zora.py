import json
import time
import random
from loguru import logger
from model.client import Client
from model.contractDTO import ContractDTO
from data.config import Config
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import ContractLogicError

CONTRACT_ZORA_BRIDGE = "0x1a0ad011913A150f69f6A19DF447A0CfD9551054"

def get_private_keys():
    with open('data/keys.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

def check_gwei():
    web3 = Web3(Web3.HTTPProvider(Config.ETH_RPC))
    while True:
        currnet_gwei = web3.from_wei(web3.eth.gas_price, 'gwei')
        if currnet_gwei > Config.MAX_GWEI:
            logger.info(f"Газ высокий: {currnet_gwei}, жду минуту до следующей проверки")
            time.sleep(60)
        else:
            logger.info(f"Газ в порядке: {round(currnet_gwei, 3)}")
            break

def get_contract_list(only_free: bool = False):
    contract_list = []
    with open('data/contracts.json', 'r') as file:
        data = json.load(file)
        for item in data:
            if only_free:
                mint_choices = {}
                raw_choces = item["mint_choices"]
                for key, value in raw_choces.items():
                    if value == 0 or value == "0":
                        mint_choices[key] = value
                if mint_choices:
                    contractDto = ContractDTO (
                        type=item["type"],
                        contract=item["contract"],
                        mint_choices=mint_choices,
                        tokens_id=item["tokens_id"],
                    )
                    contract_list.append(contractDto)
            else:
                contractDto = ContractDTO(
                    type=item["type"],
                    contract=item["contract"],
                    mint_choices=item["mint_choices"],
                    tokens_id=item["tokens_id"],
                )
                contract_list.append(contractDto)
    return contract_list

def bridge_deposit(private_key, eth_to_send):
    check_gwei()
    web3 = Web3(Web3.HTTPProvider(Config.ETH_RPC))
    bridge_contract = web3.eth.contract(address=CONTRACT_ZORA_BRIDGE, abi=Config.ZORA_ABI)
    client = Client(web3, private_key)
    txn = bridge_contract.functions.depositTransaction(
        client.address,
        web3.to_wei(eth_to_send, 'ether'),
        50000,
        False,
        web3.to_bytes(text='')
    ).build_transaction({
        'chainId': 1,
        'from': web3.to_checksum_address(client.address),
        'value': web3.to_wei(eth_to_send, 'ether'),
        'gas': 99936,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(client.address),
    })
    signed_txn = web3.eth.account.sign_transaction(txn, client.private_key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.info(f"Транзакция отправлена. Хэш: {txn_hash.hex()}")
    receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    if (receipt['status'] == 1):
        logger.success(f"Транзакция прошла успешно! Бридж успешен!")
    else:
        logger.error(f"Ошибка. Статус: {receipt['status']}")

def mint_nft(private_key, contract, value, amount, type, proxy):
    if proxy == None:
        web3 = Web3(Web3.HTTPProvider(Config.ZORA_RPC))
    else:
        web3 = Web3(Web3.HTTPProvider(Config.ZORA_RPC, request_kwargs=proxy.proxy_web3))
    client = Client(web3, private_key)
    txn = get_transaction(web3, contract, web3.to_checksum_address(client.address), value, amount, type)

    if 'gas' not in txn:
        txn['gas'] = web3.eth.estimate_gas(txn)
        
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.info(f"Транзакция отправлена. Хэш: {txn_hash.hex()}")
    receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    if (receipt['status'] == 1):
        logger.success(f"Транзакция прошла успешно! NFT заминчено!")
    else:
        logger.error(f"Ошибка. Статус: {receipt['status']}")

def get_transaction(web3, contract, address, value, amount, type):
    if type == "ERC721":
        abi_names = ["712_ABI_WITH_QUANTITY", "712_ABI_MINT"]
        for name in abi_names:
            try:
                if name == "712_ABI_WITH_QUANTITY":
                    nft_contract = web3.eth.contract(
                        address=web3.to_checksum_address(contract.contract), 
                        abi=[Config.ZORA_ABI[name]]
                    )
                    max_priority_fee_per_gas, max_fee_per_gas = get_eip1559_gas(web3)
                    tx_raw = nft_contract.functions.mint(
                        int(amount)
                    ).build_transaction({
                        'from': web3.to_checksum_address(address),
                        'value': web3.to_wei(value, 'ether'),
                        'nonce': web3.eth.get_transaction_count(address),
                        'maxPriorityFeePerGas': max_priority_fee_per_gas,
                        'maxFeePerGas': max_fee_per_gas
                    })
                    return tx_raw
                elif name == "712_ABI_MINT":
                    nft_contract = web3.eth.contract(
                        address=web3.to_checksum_address(contract.contract), 
                        abi=[Config.ZORA_ABI[name]])
                    max_priority_fee_per_gas, max_fee_per_gas = get_eip1559_gas(web3)
                    tx_raw = nft_contract.functions.mint().build_transaction({
                        'from': web3.to_checksum_address(address),
                        'value': web3.to_wei(value, 'ether'),
                        'maxPriorityFeePerGas': max_priority_fee_per_gas,
                        'maxFeePerGas': max_fee_per_gas,
                        'nonce': web3.eth.get_transaction_count(address)
                    })
                    return tx_raw
            except ContractLogicError as e:
                pass
    else:
        try:
            nft_contract = web3.eth.contract(
                address=web3.to_checksum_address(contract.contract),
                abi=[Config.ZORA_ABI["1155_ABI_MINT"]])
            max_priority_fee_per_gas, max_fee_per_gas = get_eip1559_gas(web3)
            tx_raw = nft_contract.functions.mint(
                Web3.to_checksum_address("0x04e2516a2c207e84a1839755675dfd8ef6302f0a"),
                int(random.choice(contract.tokens_id)),
                int(amount),
                Web3.to_hex(b'\x00' * 12 + Web3.to_bytes(hexstr=address))
            ).build_transaction({
                'from': web3.to_checksum_address(address),
                'value': web3.to_wei(value, 'ether'),
                'maxPriorityFeePerGas': max_priority_fee_per_gas,
                'maxFeePerGas': max_fee_per_gas,
                'nonce': web3.eth.get_transaction_count(address)
            })
            return tx_raw
        except ContractLogicError as e:
            print(f"Ошибка контракта: {e}")

def get_eip1559_gas(web3):
    latest_block = web3.eth.get_block('latest')
    max_fee_priotiry_gas = web3.eth.max_priority_fee
    max_fee_per_gas = int(latest_block['baseFeePerGas']) + max_fee_priotiry_gas
    return max_fee_priotiry_gas, max_fee_per_gas
