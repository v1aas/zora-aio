import requests
import json
import random
from loguru import logger
from typing import List
from data.config import Config
from model.contract import Contract
from model.proxy import Proxy
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

URL = f"https://mint.fun/api/mintfun/feed/free?range={Config.TIME_RANGE_FOR_SEARCH}h&chain=7777777"

soup = BeautifulSoup()

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")

def save_nft_contracts(contract_list: List[Contract]):
    contract_data_list = []
    with open('data/contracts.json', 'w') as file:
        for contract in contract_list:
            contract_data = {
                "type": contract.contract_type,
                "contract": contract.contract, 
                "mint_choices": contract.mint_choices,
                "tokens_id": contract.token_id
            }
            contract_data_list.append(contract_data)
        json.dump(contract_data_list, file, indent=2)

def get_response():
    if Config.PROXY_MODE:
        proxy = Proxy.get_proxylist()
        return requests.get(URL, headers = {'User-Agent': UserAgent().random}, proxies=random.choice(proxy).proxy_request, timeout=20)
    else:
        return requests.get(URL, headers = {'User-Agent': UserAgent().random}, timeout=20)

def parse_nft_contracts():
    response = get_response()
    if response.status_code == 200:
        logger.info("Парсинг контрактов прошел успешно!")
        data = response.json()
        collections_list = data.get('collections', [])
        contract_list = []
        for contract in collections_list:
            is_reported = 'userReported' in contract.get('flags', [])
            contract_nft = Contract(
                name=contract['name'],
                contract=contract['contract'].split(":")[1],
                contract_type=contract['contractKind'],
                max_supply=int(contract.get('maxSupply', 0)),
                total_mints=int(contract['totalMints']),
                is_reported=is_reported
            )
            if not (contract_nft.is_reported or contract_nft.max_supply == contract_nft.total_mints):
                if contract_nft.contract_type == "ERC1155":
                    contract_nft.token_id = get_token_id(contract_nft.contract)
                contract_list.append(contract_nft)
        contract_list = get_mint_choices(contract_list)
        print("\n"+"Сохранены следующие контракты: ")
        for num, contract in enumerate(contract_list, start=1):
            print(f"Контракт {num}: \n{contract}")
            print("----------------------------")
        save_nft_contracts(contract_list)
    else:
        logger.error("Error:", response.status_code, response.text)

def get_mint_choices(contract_list: List[Contract]):
    logger.info("Начинаю парсить цены и количество, это займет некоторое время")
    print(f"Количество контрактов: {len(contract_list)}")
    contract_list_with_mint_choices = []
    if Config.PROXY_MODE:
        proxy = Proxy.get_proxylist()
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options, 
            seleniumwire_options=random.choice(proxy).proxy_selenium)
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    for num, contract in enumerate(contract_list, start=1):
        mint_choices = {}
        print(f"Обрабатываю контракт №{num}")
        driver.get(f"https://mint.fun/zora/{contract.contract}")
        elements = driver.find_elements(By.CSS_SELECTOR, '.group.relative.w-full.md\\:w-auto')
        for element in elements:
            button = element.find_element(By.TAG_NAME, 'button')
            mint_choice = button.get_attribute("aria-label").split(" ")
            try:
                amount = mint_choice[1]
                price = mint_choice[3]
                if (price == "FREE"):
                    mint_choices[amount] = 0
                else:
                    mint_choices[amount] = price
            except Exception as e:
                logger.error(f"Ошибка: {e}")
        contract.mint_choices = mint_choices
        contract_list_with_mint_choices.append(contract)
    driver.quit()
    return contract_list_with_mint_choices

def get_token_id(address):
    URL = f"https://explorer.zora.energy/api/v2/tokens/{address}/transfers"
    token_list = []
    if Config.PROXY_MODE:
        proxy = Proxy.get_proxylist()
        response = requests.get(
            URL,headers = {'User-Agent': UserAgent().random}, 
            proxies=random.choice(proxy).proxy_request, 
            timeout=20).json()
        if 'items' in response:
            items = response['items']
            for item in items:
                token_id = item['total']['token_id']
                if not token_id in token_list:
                    token_list.append(token_id)
        return token_list
    else:
        response = requests.get(URL, headers = {'User-Agent': UserAgent().random}, timeout=20)
        if 'items' in response:
            items = response['items']
            for item in items:
                token_id = item['total']['token_id']
                if not token_id in token_list:
                    token_list.append(token_id)
                    
        return token_list
