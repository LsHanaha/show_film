import random
import requests
import datetime
from time import sleep
import telebot
from telebot import types
from flask import Flask
from flask import request
from flask import jsonify
import json

bot = telebot.TeleBot('609407669:AAGAdFducIDkdVyLVAaJzp1J5CTyrHU4p4k')
advices = ('\nLet me advice you this:\n', '\nWhat do you think about:\n', '\nWhat about:\n', '\nYour film is:\n')


app = Flask(__name__)


@app.route('/609407669:AAGAdFducIDkdVyLVAaJzp1J5CTyrHU4p4k', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        try:
            chat_id = r['message']['chat']['id']
            text = r['message']['text']
            username = r['message']['from']['username']
            time = datetime.datetime.now()
            f = open('log.txt', 'a')
            f.write('date: {}, id: {}, username: {},  text: {}\n'.format(time, chat_id, username, text))
            f.close()
        except KeyError:
            chat_id = r['callback_query']['message']['chat']['id']
            message_id = r['callback_query']['message']['message_id']
            text = r['callback_query']['data']
            if text == 'start':
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text=advices[random.randint(0, 3)])
                main_func(chat_id)
            elif text == 'stop':
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="See you!")
        if text == '/start':
            bot.send_message(chat_id, "Hello, Friend! This bot can advise you a random film. Send me something "
                                      "if you want to start")
        elif text == '/help':
            bot.send_message(chat_id, "Oh, it seems you lost, send me some random text and I gonna do my best")
        else:
            try:
                r['callback_query']
            except KeyError:
                any_msg(chat_id)
        return jsonify(r)
    return '<h1>Hello</h1>'


# https://api.telegram.org/bot609407669:AAGAdFducIDkdVyLVAaJzp1J5CTyrHU4p4k/setWebhook?url=kirik193.pythonanywhere.com/


def any_msg(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton(text="Show a film", callback_data="start")
    btn_2 = types.InlineKeyboardButton(text="Not today", callback_data="stop")
    keyboard.add(btn_1, btn_2)
    bot.send_message(chat_id, "Hi, i can offer you two ways", reply_markup=keyboard)


def any_msg2(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton(text="I've seen it", callback_data="start")
    btn_2 = types.InlineKeyboardButton(text="I will see this", callback_data="stop")
    keyboard.add(btn_1, btn_2)
    bot.send_message(chat_id, " \nDo you need smth else?", reply_markup=keyboard)


def main_func(chat_id):
    a = show_film()
    bot.send_message(chat_id, "{} \n\nGenre: {}\nRuntime: {}\nDirector: {}\nReleased: {}\n\n{} \n\n{}".format(
        a["Title"], a["Genre"], a["Runtime"], a["Director"], a["Released"], a["Plot"], a["Poster"]))
    if len(a["Ratings"]) > 1:
        bot.send_message(chat_id, "Ratings:\nIMDB      {}\nTomatoes   {}".format(a["Ratings"][0]["Value"],
                                                                                 a["Ratings"][1]["Value"]))
    elif len(a["Ratings"]) == 1:
        bot.send_message(chat_id, "Ratings:\nIMDB {}"  .format(a["Ratings"][0]["Value"]))
    else:
        bot.send_message(chat_id, "Choose of redaction!")
    any_msg2(chat_id)


def size_list():
    i = 0
    f = open("result.txt")
    for line in f:
        i += 1
    print(i)
    num = random.randint(0, i)
    return num


def point_to_rand_film(num):
    i = 0
    result = ''
    f = open("result.txt")
    for line in f:
        if i == num:
            result = line[0:-1]
            break
        i += 1
    return result


def get_updates(result):  # Получаем данные, написанные клиентами в чате бота каждые 30 сек
    api_url = "http://www.omdbapi.com/?i={}&apikey=ff236ae0".format(result)
    response = requests.get(api_url)  # запрашиваем данные с сервера
    result_json = response.json()  # представляем данные в формате json и по ключу result считываем данные
    return result_json  # Выводим данные в формате json


def show_film():
    num = random.randint(0, 7581)
    if get_updates(point_to_rand_film(num))['Type'] == 'movie':
        return get_updates(point_to_rand_film(num))
    while get_updates(point_to_rand_film(num))['Type'] == 'series':
        num = num + 1
    while get_updates(point_to_rand_film(num))['Type'] == 'episode':
        num = num + 1
    while get_updates(point_to_rand_film(num))['Type'] == 'game':
        num = num + 1
    return get_updates(point_to_rand_film(num))


if __name__ == '__main__':
    app.run()
