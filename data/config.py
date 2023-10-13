import json

class Config:
    #-----------------UTILITIES----------------#
    ETH_RPC = "https://eth.llamarpc.com"
    ZORA_RPC = "https://rpc.zora.energy"
    
    ZORA_ABI = json.load(open("data/jsons/zora_abi.json"))
    BRIDGE_ABI = json.load(open("data/jsons/zora_bridge_abi.json"))
    #------------------------------------------#
    

    #-----------PROXY-------------#
    PROXY_MODE = True # Включать ли прокси
    
    MOBILE_PROXY = False # Мобильные ли прокси 

    PROXY_KEY = "" # Ключ для смены ip в сервисе https://mobileproxy.space/
    #-----------------------------#


    #-------BLOCKCHAIN SETUP------#
    MAX_GWEI = 25 # Максимальный gwei в ETH

    MIN_TIME_FOR_TXN = 10 # Минимальная задрежка перед транзакциями
    MAX_TIME_FOR_TXN = 30 # Минимальная задрежка перед транзакциями
    #-----------------------------#

    #-------BLOCK NFT------#
    ONLY_FREE = False # Минтить только бесплатные нфт

    MAX_PAY_FOR_NFT = 0.0004 # Максимальная цена, которую возможно заплатить за минт нфт

    TIME_RANGE_FOR_SEARCH = 12 # Таймфрейм для парса mint.fun. Возможные значения: 0.5, 1, 6, 12, 24
    #----------------------#

    #-------BRIDGE SETUP------#
    MIN_TO_BRIDGE = 0.01 # Минимальное количество ETH для бриджа
    MAX_TO_BRIDGE = 0.02 # Максимальное количество ETH для бриджа
    #-------------------------#

    title1 = '''
                                   1111111
                                   1::::::1
                                   1:::::::1
                                   111:::::1
       vvvvvvv           vvvvvvv   1::::1     aaaaaaaaaaaaa     aaaaaaaaaaaaa       ssssssssss
       v:::::v         v:::::v    1::::1     a::::::::::::a    a::::::::::::a    ss::::::::::s
       v:::::v       v:::::v     1::::1     aaaaaaaaa:::::a   aaaaaaaaa:::::a ss:::::::::::::s
       v:::::v     v:::::v      1::::l              a::::a            a::::a s::::::ssss:::::s
        v:::::v   v:::::v       1::::l       aaaaaaa:::::a     aaaaaaa:::::a  s:::::s  ssssss
        v:::::v v:::::v        1::::l     aa::::::::::::a   aa::::::::::::a    s::::::s
        v:::::v:::::v         1::::l    a::::aaaa::::::a  a::::aaaa::::::a       s::::::s
         v:::::::::v          1::::l   a::::a    a:::::a a::::a    a:::::a ssssss   s:::::s
          v:::::::v        111::::::111a::::a    a:::::a a::::a    a:::::a s:::::ssss::::::s
           v:::::v         1::::::::::1a:::::aaaa::::::a a:::::aaaa::::::a s::::::::::::::s
            v:::v          1::::::::::1 a::::::::::aa:::a a::::::::::aa:::a s:::::::::::ss
             vvv           111111111111  aaaaaaaaaa  aaaa  aaaaaaaaaa  aaaa  sssssssssss
    '''

    title2 ='''
             __
            /  |
     __   __`| |   __ _   __ _  ___
     \ \ / / | |  / _` | / _` |/ __|
      \ V / _| |_| (_| || (_| |\__ \\
       \_/  \___/ \__,_| \__,_||___/
'''

    title3 = '''
         ___      ___    ____          __            __         ________
        |"  \    /"  | /  " \        /""\          /""\       /"       )
        \   \  //  /  /__|| |       /    \        /    \     (:   \___/
         \\  \/. ./      |: |      /' /\  \      /' /\  \     \___  \\
          \.    //      _\  |     //  __'  \    //  __'  \     __/  \\
           \\   /      /" \_|\   /   /  \\  \  /   /  \\  \   /" \   :)
            \__/      (_______) (___/    \___)(___/    \___) (_______/
    '''

    title5 = '''
                   ,--.
       ,--.  ,--. /   |  ,--,--.  ,--,--.  ,---.
        \  `'  /  `|  | ' ,-.  | ' ,-.  | (  .-'
         \    /    |  | \ '-'  | \ '-'  | .-'  `)
          `--'     `--'  `--`--'  `--`--' `----'
    '''

    title6 = '''
        ____    ____  __       ___           ___           _______.
        \   \  /   / /_ |     /   \         /   \         /       |
         \   \/   /   | |    /  ^  \       /  ^  \       |   (----`
          \      /    | |   /  /_\  \     /  /_\  \       \   \\
           \    /     | |  /  _____  \   /  _____  \  .----)   |
            \__/      |_| /__/     \__\ /__/     \__\ |_______/
    '''
    TITLES = [
        title1,
        title2,
        title3,
        title5,
        title6,
    ]

    COLORS = ['light_grey', 'light_yellow', 'light_blue', 'light_magenta', 'light_cyan']