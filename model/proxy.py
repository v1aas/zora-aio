import requests
from data.config import Config

class Proxy:
    def __init__(self, proxy_format: str):
        self.proxy_request = {
            'http': f'http://{proxy_format}',
            'https': f'http://{proxy_format}'
        }
        self.proxy_selenium = {
            'proxy': {
                'http': f'http://{proxy_format}',
                'https': f'http://{proxy_format}'
            }
        }
        self.proxy_web3 = {
            'proxies': {
                'http': f'http://{proxy_format}',
                'https': f'http://{proxy_format}'
            }
        }
    
    def change_mobile_ip(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }
        URL = f"https://mobileproxy.space/reload.html?proxy_key={Config.PROXY_KEY}&format=json"
        response = requests.get(URL, headers=headers, timeout=60)
        if response.status_code == 200:
            new_ip = response.json()['new_ip']
            print(f"Новый ip: {new_ip}")

    @staticmethod
    def get_proxylist():
        proxylist = []
        with open('data/proxy.txt', 'r') as file:
            for line in file.readlines():
                if line.strip() == None:
                    continue
                proxylist.append(Proxy(line.strip()))
        return proxylist
