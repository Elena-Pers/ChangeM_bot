import telebot

from config import *
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Добро пожаловать!☀️ \n\n Этот бот поможет конвертировать валюту. \n\nЧтобы начать работу, введите команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводной валюты>\n \n Чтобы увидеть список всех доступных валют, нажмите/введите: /value'
    bot.reply_to(message, text)

@bot.message_handler(commands=['value'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):

    try:
        base, quote, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, 'Неверное количество параметров!')

    try:
        new_price = Converter.get_price(base, quote, amount)
        new_price = round(new_price, 2)
        bot.send_message(message.chat.id, f"Цена {amount} {quote} в {base}: {new_price}")
    except APIException as e:
        bot.reply_to(message, f"‼️ Ошибка в команде:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"‼️ Не удалось обработать команду\n{e}")

bot.polling()