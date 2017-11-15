import telepot
from pprint import pprint

token = 'TOKEN'

bot = telepot.Bot(token)
print(bot.getMe())
pprint(bot.getUpdates())
bot.sendMessage(TOKEN, '*bold text*\n_italic text_\n[link](http://www.google.com)')




