import requests
import logging

"""Class to represent each coin as a object. Contains useful values such as a unique id, name, symbol, etc."""
class Coin(object):
    def __init__(self,
                 id="",
                 name="",
                 symbol="",
                 rank="",
                 price_usd="",
                 price_btc="",
                 market_cap_usd="",
                 available_supply="",
                 total_supply="",
                 percent_change_1h="",
                 percent_change_24h="",
                 percent_change_7d="",
                 last_updated="",
                 last_day_volume_usd=""):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.rank = rank
        self.price_usd = price_usd
        self.price_btc = price_btc
        self.market_cap_usd = market_cap_usd
        self.available_supply = available_supply
        self.total_supply = total_supply
        self.percent_change_1h = percent_change_1h
        self.percent_change_24h = percent_change_24h
        self.percent_change_7d = percent_change_7d
        self.last_updated = last_updated
        self.last_day_volume_usd = last_day_volume_usd

    #Classmethod for string representation of a coin     
    def __str__(self):
        info = "Coin: %s \nRanked: %s" % (self.name, self.rank)
        info += "\nPrice : %s $ \nPrice BTC: %s " % (self.price_usd,
                                                   self.price_btc)
        info += "\nAvailable supply: %s \nTotal supply: %s"\
                %(self.available_supply, self.total_supply)
        info += "\nPercent changes:1h  = %s\n \t\t24h = %s\n \t\t1d  = %s" \
                %(self.percent_change_1h, self.percent_change_7d,
                  self.percent_change_24h)
        return info

    #Returning printable representation of a coin 
    def __repr__(self):
        return "Coin"

    def get_price_btc(self):
        return self.price_btc

"""Class representing current market stats, providing information such as Bitcoin's market percentage (USD), number of active assets, etc."""
class Stats(object):

    def __init__(self,
                 btc_market_percent="",
                 total_market_usd="",
                 active_market="",
                 active_assets="",
                 active_currencies="",
                 last_day_volume_usd=""):
        self.btc_market_percent = btc_market_percent
        self.total_market_usd = total_market_usd
        self.active_market = active_market
        self.active_assets = active_assets
        self.active_currencies = active_currencies
        self.last_day_volume_usd = last_day_volume_usd

    #Classmethod for string representation of a coin 
    def __str__(self):
        statistics =  "   Market value: %s" % self.total_market_usd + " Billion USD"
        statistics += "\n Bitcoin share: %s" % self.btc_market_percent
        statistics += "\n Active markets: %s" % self.active_market
        statistics += "\n Active assets: %s" % self.active_assets
        statistics += "\n Active currencies: %s" % self.active_currencies
        statistics += "\n Last 24h volume: %s" % self.last_day_volume_usd
        return statistics

    def __repr__(self):
        return "Stats"

"""Core class, providing the ability to obtain objects of class Coin and market stats"""
class CryptoMarket(object):
    __COIN_MARKET_CAP_URL = \
        'https://api.coinmarketcap.com/v1/'

    #Internal method to access coinmarketcap API with given endpoint, typically a coin
    def __call_market(self, endpoint, params):
        try:
            #LOGGING AND DEBUGGING
            print(str(endpoint))
            logging.info("Trying to get API request from "+__COIN_MARKET_CAP_URL+endpoint)

            response = requests.get(
                self.__COIN_MARKET_CAP_URL + endpoint, params=params)
            if response.status_code != '200':
                response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
        data = response.json()
        return data

    #Method to get a specificed coin using a coin_id (ISO compliant), accepts optional kwargs but does not use them.
    def coin(self,  coin_id, **kwargs):
        params = {}
        params.update(**kwargs)
        data = self.__call_market('ticker/'+coin_id, params)
        if 'error' in data:
            return 'Error occurred'
        coin = data[0]
        return Coin(coin['id'], coin['name'], coin['symbol'], coin['rank'],
                    coin['price_usd'], coin['price_btc'],
                    coin['market_cap_usd'], coin['available_supply'],
                    coin['total_supply'], coin['percent_change_1h'],
                    coin['percent_change_24h'], coin['percent_change_7d'],
                    coin['last_updated'], coin['24h_volume_usd'])

    #Method to get market statistics from coinmarketcap.com API
    def stats(self, **kwargs):
        params = {}
        params.update(**kwargs)
        data = self.__call_market('global', params)
        if 'error' in data:
            return 'Error occurred'
        return Stats(data['bitcoin_percentage_of_market_cap'],
                     data['total_market_cap_usd'],
                     data['active_markets'], data['active_assets'],
                     data['active_currencies'], data['total_24h_volume_usd'])