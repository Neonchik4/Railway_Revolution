import requests
import os


def get_coords_of_object(name_object):
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={API_GEOCODE_MAPS}&geocode={name_object}&format=json"
    response = requests.get(url)
    response_json = response.json()
    pos = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    lon, lat = pos.split(" ")
    return lat, lon


API_GEOCODE_MAPS = "40d1649f-0493-4b70-98ba-98533de7710b"
lst = ['Стрешнево', 'Балтийская', 'Коптево', 'Лихоборы', 'Окружная', 'Владыкино', 'Ботанический сад', 'Ростокино',
       'Белокаменная', 'Бульвар Рокоссовского', 'Локомотив', 'Измайлово', 'Соколиная Гора', 'Шоссе Энтузиастов',
       'Андроновка', 'Нижегородская', 'Новохохловская', 'Угрешская', 'Дубровка', 'Автозаводская', 'ЗИЛ',
       'Верхние Котлы', 'Крымская', 'Площадь Гагарина', 'Лужники', 'Кутузовская', 'Москва-Сити', 'Шелепиха', 'Хорошёво',
       'Зорге', 'Панфиловская']

for i in lst:
    coords = ",".join(get_coords_of_object('станция ' + i)[::-1])
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&z=16&l=sat"

    response = requests.get(map_request)

    directory = "static/img/stations/"

    image_path = os.path.join(directory, f"станция_{i}.jpg")

    with open(image_path, 'wb') as file:
        file.write(response.content)
