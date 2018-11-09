import random
import requests


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
