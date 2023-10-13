# ZORA-AIO

* ### [RU](#RU)
* ### [EN](#EN)

# RU
<a name="RU"></a>

### Модули
1. Бридж через официальный мост https://zora.co/
2. Парсер бесплатных нфт (на зоре) с https://mint.fun/
3. Минт нфт также с https://mint.fun/

## Настройка
Весь сетап происходит в config.py, пропущу момент с установлением библиотек и очевидных вещей. Если вы нубик, то посмотрите прошлые мои софты, там все подробно описано.

В `data/keys.txt` - загрузить приватные ключи (1 ключ - 1 строка)

В `data/proxy.txt` - грузить прокси грузить в формате **log:pass@address:port**. Есть поддержка мобильных прокси, если использовать их, то достаточно загрузить его один прокси (прим. log:pass@cproxy.site:8080)

В `data/contracts.json` - здесь находятся контракты с минтфана. Можно вставить их самому, только по такому примеру:
```json
[
    {
        "type": "ERC1155",
        "contract": "0x6b2A5667D870B059920526243aE1c7CA3908A1d8",
        "mint_choices": {
            "1": "0.000777"
        },
        "tokens_id": [
            "1"
            ]
    },
    {
        "type": "ERC721",
        "contract": "0x62eB40DF0eb27e8b70CDAf0286D36600f8e7D06C",
        "mint_choices": {
            "1": "0.000040",
            "2": "0.000084",
            "10": "0.000420"
        },
        "tokens_id": null
    }
]
```

**Config.py разделен на "модули":**
1. `UTILITIES`

* Можно менять только prc

2. `PROXY`
* PROXY_MODE - Запускать софт с прокси
* MOBILE_PROXY - Мобильные ли прокси 
* PROXY_KEY - Ключ с ссылки для смены ip

3. `BLOCKCHAIN SETUP`
* MAX_GWEI - Максимальный gwei в ETH сети
* MIN_TIME_FOR_TXN - Минимальная задрежка перед транзакциями (всеми)
* MAX_TIME_FOR_TXN Максимальная задрежка перед транзакциями (всеми)

4. `BLOCK NFT`
* ONLY_FREE - Минтить только бесплатные нфт с папки contracts.json
* MAX_PAY_FOR_NFT - Максимальная цена за платную нфт, которая будет заминчена. **ЕСЛИ ВЫ ХОТИТЕ МИНТИТЬ ТОЛЬКО БЕСПЛАТНЫЕ, ЗДЕСЬ НЕ НУЖНО СТАВИТЬ 0**
* TIME_RANGE_FOR_SEARCH - Таймфрейм для парса нфт с минтфана

5. `BRIDGE SETUP`
* Задается интервал количества ETH для бриджа в зору

**После всех настроек можно запускать main.py!**

### Полезная информация
1. Если прокси меньше, чем кошельков, то прокси будут запускаться по кругу
2. Для каждого кошелька рандомный порядок нфт, которые он будет минтить
3. Если мобильные прокси, то на каждый кошелек - айпи будет меняться
## Возможные ошибки
1. [1013/173835.913:INFO:CONSOLE(9)] "Uncaught Error: Minified React error #425; visit https://reactjs.org/docs/error-decoder.html?invariant=425 for the full message or use the non-minified dev environment for full errors and additional helpful warnings.", source: https://mint.fun/_next/static/chunks/framework-19694439bdd76b71.js (9)

Ошибка в парсинге, ничего страшного, на его результаты это не повлияет, просто скип

2. Ошибка при минте

Здесь существует несколько проблем:
1. Неправильное отображение цены на минтфане, например на сайте 0.00099, а настоящая цена 0.000999. Такое исправлять только руками.
2. Не шаблонный контракт. Бывают попадаются не шаблонные, кастомные контракты, такие к сожалению, будут скипаться и выдавать ошибку.
3. Ограниченное количество нфт на юзера. Возможно, что по одному контракту не будут проходить транзакции с разным количеством.

# EN
<a name="EN"></a>
### Modules
1. Bridge through the official bridge https://zora.co/
2. Parser of free nft's (on zora) from https://mint.fun/
3. Mint nft also from https://mint.fun/

### Configuration
The whole setup happens in config.py, I'll skip the point about installing libraries and obvious stuff. If you're a noob, check out my past soft's, it's all detailed there.

In `data/keys.txt` - load private keys (1 key - 1 line)

In `data/proxy.txt` - load proxies in **log:pass@address:port** format. There is support for mobile proxies, if you use them, it is enough to load it one proxy (note log:pass@cproxy.site:8080).

In `data/contracts.json` - this is where the contracts from minfan are located. You can insert them yourself, just by following this example:
```json
[
    {
        "type": "ERC1155",
        { "contract": "0x6b2A5667D870B059920526243aE1c7CA3908A1d8",
        "mint_choices": {
            "1": "0.000777"
        },
        }, "tokens_id": [
              "1"
            ]
    },
    {
        { "type": "ERC721",
        { "contract": "0x62eB40DF0eb27e8b70CDAf0286D36600f8e7D06C",
        "mint_choices": {
            "1": "0.000040",
            "2": "0.000084",
            "10": "0.000420"
        },
        "tokens_id": null
    }
]
```
**Config.py is divided into "modules":**
1. `UTILITIES`.

* Only prc can be changed

2. `PROXY`.
* PROXY_MODE - Run software with proxies
* MOBILE_PROXY - Whether proxies are mobile or not
* PROXY_KEY - Key from the link to change ip

3. `BLOCKCHAIN SETUP`.
* MAX_GWEI - Maximum gwei in ETH network
* MIN_TIME_FOR_TXN - Minimum delay before transactions (all)
* MAX_TIME_FOR_TXN - Maximum delay before transactions (all)

4. `BLOCK NFT`
* ONLY_FREE - Mint only free nft's from data/contracts.json 
* MAX_PAY_FOR_NFT - Maximum price for paid nft that will be mined. **IF YOU WANT TO MIN ONLY FREE NFTS, YOU DON'T NEED TO SET 0** HERE
* TIME_RANGE_FOR_SEARCH - Timeframe for parsing nft's from mintfun

5. `BRIDGE SETUP`.
* Sets the interval of the amount of ETH for bridge to Zora

**After all settings you can run main.py!

### Useful information
1. If there are less proxies than wallets, the proxies will run in a circle
2. For each wallet, randomize the order of nfts it will minecheck
3. if mobile proxies, then for each wallet the IP will change

## Possible errors
1.[1013/173835.913:INFO:CONSOLE(9)] "Uncaught Error: Minified React error #425; visit https://reactjs.org/docs/error-decoder.html?invariant=425 for the full message or use the non-minified dev environment for full errors and additional helpful warnings.", source: https://mint.fun/_next/static/chunks/framework-19694439bdd76b71.js (9)

Error in parsing, no big deal, it won't affect the results, just a skip

2. Error in mint

There are several problems here:
1. Incorrect display of the price on mintfun, for example on the site 0.00099, and the real price is 0.000999. This can only be corrected by hand.
2. Not a template contract. There are some non-template, custom contracts, such unfortunately, will skip and give an error.
3. limited number of nft per user. It is possible that one contract will not pass transactions with different amounts nft.
