import zora
import pars
import random
import itertools
import time
from model.proxy import Proxy
from data.config import Config
from loguru import logger
from typing import List
from termcolor import cprint

def get_private_keys():
    with open('data/keys.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

def bridge(private_keys: List[str]):
    for num, key in enumerate(private_keys, start=1):
        print(f"---Кошелек {num} из {len(private_keys)}---")
        eth_to_send = round(random.uniform(Config.MAX_TO_BRIDGE, Config.MIN_TO_BRIDGE), 5)
        zora.bridge_deposit(key, eth_to_send)
        seconds = random.randint(Config.MIN_TIME_FOR_TXN, Config.MAX_TIME_FOR_TXN)
        print(f"Ожидаю {seconds} до отправки следующей транзакции")
        time.sleep(seconds)

def parse():
    pars.parse_nft_contracts()

def mint(private_keys: List[str]):
    contracts = zora.get_contract_list(Config.ONLY_FREE)
    proxy_list = itertools.cycle(Proxy.get_proxylist() or [None])
    for num, key in enumerate(private_keys, start=1):
        if Config.MOBILE_PROXY:
            proxy = next(proxy_list)
            proxy.change_mobile_ip()
            random.shuffle(contracts)
            print(f"---Кошелек {num} из {len(private_keys)}---")
            for contract in contracts:
                for amount, value in contract.mint_choices.items():
                    if float(value) > Config.MAX_PAY_FOR_NFT:
                        continue
                    else:
                        try:
                            logger.info(f"Контракт: {contract.contract}")
                            zora.mint_nft(key, contract, value, amount, contract.type, proxy)
                        except TypeError:
                            logger.error("Возникла ошибка с контрактом! Перехожу к следующему!")
                            break
                        seconds = random.randint(Config.MIN_TIME_FOR_TXN, Config.MAX_TIME_FOR_TXN)
                        print(f"Ожидаю {seconds} до отправки следующей транзакции")
                        time.sleep(seconds)
        else:
            proxy = next(proxy_list)
            random.shuffle(contracts)
            print(f"---Кошелек {num} из {len(private_keys)}---")
            for contract in contracts:
                for amount, value in contract.mint_choices.items():
                    if float(value) > Config.MAX_PAY_FOR_NFT:
                        continue
                    else:
                        try:
                            logger.info(f"Контракт: {contract.contract}")
                            zora.mint_nft(key, contract, value, amount, contract.type, proxy)
                        except TypeError:
                            logger.error("Возникла ошибка с контрактом! Перехожу к следующему!")
                            break
                        seconds = random.randint(Config.MIN_TIME_FOR_TXN, Config.MAX_TIME_FOR_TXN)
                        logger.info(f"Ожидаю {seconds} секунд до отправки следующей транзакции")
                        time.sleep(seconds)
    
def main():
    cprint(random.choice(Config.TITLES), random.choice(Config.COLORS))
    print("https://t.me/v1aas \n")

    keys = get_private_keys()

    modules = {
        "1": lambda: bridge(keys),
        "2": lambda: parse(),
        "3": lambda: mint(keys)
    }

    while True:
        module = input(
            "Доступные модули: \n"
            "1 - Bridge to Zora \n"
            "2 - Parser nft's mint.fun \n"
            "3 - Mint nft's \n"
            "0 - Exit \n"
            "Your choice: "
        )

        if module == "0":
            break
        elif module in modules:
            modules[module]()
        else:
            print("Неправильный выбор!")

if __name__ == "__main__":
    main()