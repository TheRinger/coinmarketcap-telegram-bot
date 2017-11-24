#Core
import coinmarketcap_telegram_core
#TG-Bot
from telegram.ext import Updater,CommandHandler
#Logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
#Errorhandling
from requests import HTTPError



updater= Updater(token="450598796:AAF5nKRLw47lCWqHH2K1PXqBlpBRcyZ1VP0")
dispatcher=updater.dispatcher
cryptomarket=coinmarketcap_telegram_core.CryptoMarket()

def start(bot,update):
	bot.send_message(chat_id=update.message.chat_id
					,text="I'm the Coinmarketcap Bot.")

start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)

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


def satoshi(bot,update,args):
	try:
		btc_price=cryptomarket.coin(args[0]).price_btc
		sat_price=float(price_btc)/0.00000001 
updater.start_polling()