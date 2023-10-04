import os
import json

import requests


class Get_Data_Spot:
    def __init__(self, url, file_name, name_arg, way):
        self.url = url
        self.name = file_name
        self.name_arg = name_arg
        self.way = way

    def is_dirs(self):
        folder_path = './data'
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        folder_path = './bucket'
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

    def sorted_data(self, data):
        dict = {}
        list_symbols = []
        for ad in data:
            symbol = ad[self.name_arg['name']]
            price = ad[self.name_arg['price']]
            dict[symbol] = price
            list_symbols.append(symbol)
        return dict, list_symbols

    def get_data(self):
        response = requests.get(self.url)
        data = response.json()
        for i in self.way:
            data = data[i]
        return data

    def file_path(self):
        return f'./data/{self.name}.txt'

    def file_path_list(self):
        return f'./data/{self.name}_list.txt'

    def file_path_bucket(self):
        return f'./bucket/{self.name}.txt'

    def file_path_bucket_list(self):
        return f'./bucket/{self.name}_list.txt'
    
    def save(self, data, path):
        with open(path, 'w') as file:
            json.dump(data, file)

    def is_file(self):
        if os.path.exists(self.file_path()):
            return True
        return False

    def read_file(self):
        with open(self.file_path(), 'r') as file:
            data = json.load(file)
        return data

    def clearing_data(self, old_data, data):
        del_symbol = []
        bucket = {}
        print(type(old_data))
        for old, old_price in old_data.items():
            for new, new_price in data.items():
                if old != new:
                    continue
                if old_price != new_price:
                    continue
                bucket[old] = old_price
                del_symbol.append(old)
        
        for symbol in del_symbol:
            del data[symbol]

        self.save(bucket, self.file_path_bucket())
        return data, del_symbol
    
    def save_data(self):
        self.is_dirs()
        status = self.is_file()
        data = self.get_data()
        dict, list_symbols = self.sorted_data(data)
        if not status:
            self.save(dict, self.file_path())
            self.save(list_symbols, self.file_path_list())
            return True
        
        old_data = self.read_file()
        clear_data, garbage_token = self.clearing_data(old_data, dict)
        self.save(clear_data, self.file_path())
        self.save(clear_data, self.file_path_list())
        return len(garbage_token)


file_name = 'gateio'
url = 'https://api.gateio.ws/api/v4/spot/tickers'
name_arg = {'name': 'currency_pair', 'price': 'last'}
data_gateio = Get_Data_Spot(url, file_name, name_arg, [])
print(data_gateio.save_data())

file_name = 'binance'
url = 'https://api.binance.com/api/v3/ticker/price'
name_arg = {'name': 'symbol', 'price': 'price'}
data_binance = Get_Data_Spot(url, file_name, name_arg, [])
print(data_binance.save_data())

file_name = 'bitget'
url = 'https://api.bitget.com/api/spot/v1/market/tickers'
name_arg = {'name': 'symbol', 'price': 'close'}
data_bitget = Get_Data_Spot(url, file_name, name_arg, ['data'])
print(data_bitget.save_data())

file_name = 'bybit'
url = 'https://api.bybit.com/spot/v3/public/quote/ticker/price'
name_arg = {'name': 'symbol', 'price': 'price'}
data_bybit = Get_Data_Spot(url, file_name, name_arg, ['result', 'list'])
print(data_bybit.save_data())

file_name = 'huobi'
url = 'https://api-aws.huobi.pro/market/tickers'
name_arg = {'name': 'symbol', 'price': 'close'}
data_huobi = Get_Data_Spot(url, file_name, name_arg, ['data'])
print(data_huobi.save_data())

file_name = 'kucoin'
url = 'https://api.kucoin.com/api/v1/market/allTickers'
name_arg = {'name': 'symbol', 'price': 'last'}
data_kucoin = Get_Data_Spot(url, file_name, name_arg, ['data', 'ticker'])
print(data_kucoin.save_data())

file_name = 'mexc'
url = 'https://api.mexc.com/api/v3/ticker/price'
name_arg = {'name': 'symbol', 'price': 'price'}
data_mexc = Get_Data_Spot(url, file_name, name_arg, [])
print(data_mexc.save_data())

file_name = 'okx'
url = 'https://www.okx.com/api/v5/market/tickers?instType=SPOT'
name_arg = {'name': 'instId', 'price': 'last'}
data_okx = Get_Data_Spot(url, file_name, name_arg, ['data'])
print(data_okx.save_data())

class Get_Data_Pancake(Get_Data_Spot):
    def get_data(self):
        all_data = []
        for i in range(1, 23):
            url_template = self.url.format(page=i)
            response = requests.get(url_template)
            data = response.json()
            for i in self.way:
                data = data[i]
            all_data.extend(data)
        return all_data

file_name = 'pancake'
url = 'https://api.coinmarketcap.com/dexer/v3/platformpage/pair-pages?platform-id=14&dexer-id=6706&sort-field=txns24h&category=spot&page={page}'
name_arg = {'name': 'pairContractAddress', 'price': 'priceQuote'}
data_pancake = Get_Data_Pancake(url, file_name, name_arg, ['data', 'pageList'])
print(data_pancake.save_data())