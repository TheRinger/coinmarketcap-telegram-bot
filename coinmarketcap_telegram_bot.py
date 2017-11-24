#Core
import coinmarketcap_telegram_core
#TG-Bot
from telegram.ext import Updater,CommandHandler
#Logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
#Errorhandling
from requests import HTTPError
#reading TG-API-Token from file
with open('token.txt','r') as tokenfile:
	token= tokenfile.readline()

#Initialize TG-Updater, TG-message-dispatcher, cryptomarket from coinmarketcap_telegram_core
updater= Updater(token)
dispatcher=updater.dispatcher
cryptomarket=coinmarketcap_telegram_core.CryptoMarket()


"""
Start function needed for the bot in order to be able to introduce itself

Params:
bot - equal to self, instance of bot calling
update - updateevent passed from Updater
"""
def start(bot,update):
	bot.send_message(chat_id=update.message.chat_id
					,text="I'm the Coinmarketcap Bot.")

start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)


"""
Function to convert given coinname / coin symbol to it's usd price

Params:
bot - equal to self, instance of bot calling
update - updateevent passed from Updater
args - arguments given (coinname / coin-symbol in this case

TODO: Write a basemethod to get bitcoin base price in usd, then use that value or convert to other currencies such as eur 
"""
def usd(bot,update,args):
	print(args)
	print(type(args))
	try:
		usd_price=cryptomarket.coin(args[0]).price_usd
		bot.send_message(chat_id=update.message.chat_id
						,text=usd_price)
	except (HTTPError,IndexError) :
		bot.send_message(chat_id=update.message.chat_id
						,text="I can't find this coin.\n Maybe try a different name?")
	
usd_handler= CommandHandler('usd',usd,pass_args=True)
dispatcher.add_handler(usd_handler)


"""
Function to convert given coinname / coin symbol to it's price in satoshi

Params:
bot - equal to self, instance of bot calling
update - updateevent passed from Updater
args - arguments given (coinname / coin-symbol in this case
"""
def satoshi(bot,update,args):
	try:
		btc_price=cryptomarket.coin(args[0]).price_btc
		sat_price=float(btc_price)/0.00000001
		bot.send_message(chat_id=update.message.chat_id
						,text="Price in BTC:\n"+str(btc_price)+"\nPrice in Satoshi:\n"+str(sat_price))
	except Exception as e:
		bot.send_message(chat_id=update.message.chat_id
						,text="Scheisendreck, wieder ein Fehler.") 
		logging.warning(e)

satoshi_handler= CommandHandler('satoshi',satoshi,pass_args=True)
dispatcher.add_handler(satoshi_handler)

"""
Function to get current market stats

Params:
bot - euqal to self, instance of bot calling
update - updateevent passed from Updater
"""
def stats(bot,update):
	try:
		stats=cryptomarket.stats()
		bot.send_message(chat_id=update.message.chat_id
						,text=str(stats))
	except Exception as e:
		bot.send_message(chat_id=update.message.chat_id
						,text="Could not get stats. Try again later.")

stats_handler=CommandHandler('stats',stats)
dispatcher.add_handler(stats_handler)



#Start the bot
updater.start_polling()
