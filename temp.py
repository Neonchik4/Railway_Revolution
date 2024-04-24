@app.route('/list_stations/<line_name>')
def show_line_info(line_name):
    conn = sqlite3.connect('db/Railway_data.db')
    cursor = conn.cursor()
    stations = cursor.execute(f"""SELECT STATIONS FROM LINES WHERE NAME="{line_name}" """).fetchone()[0].split(', ')
    conn.close()
    conditions_ru = {"clear": "ясно", "partly-cloudy": "малооблачно", "cloudy": "облачно с прояснениями",
                     "overcast": "пасмурно",
                     "light-rain": "небольшой дождь", "rain": "дождь", "heavy-rain": "сильный дождь",
                     "showers": 'ливень',
                     "wet-snow": "дождь со снегом", "light-snow": "небольшой снег", "snow": 'снег',
                     "snow-showers": "снегопад",
                     "hail": 'град', "thunderstorm": "гроза", "thunderstorm-with-rain": "дождь с грозой",
                     "thunderstorm-with-hail": "гроза с градом"}
    wind_dir_ru = {
        'N': 'С',
        'S': 'Ю',
        'W': 'З',
        'E': 'В',
        'NW': 'СЗ',
        'NE': 'СВ',
        'SE': 'ЮВ',
        'SW': 'ЮЗ',
        'C': 'C'
    }
    to_wind_dir_ru_eng = {
        'N': 'S',
        'S': 'N',
        'W': 'E',
        'E': 'W',
        'NW': 'SE',
        'NE': 'SW',
        'SE': 'NW',
        'SW': 'NE',
        'С': 'Ю',
        'Ю': 'С',
        'З': 'В',
        'В': 'З',
        'СЗ': 'ЮВ',
        'СВ': 'ЮЗ',
        'ЮВ': 'СЗ',
        'ЮЗ': 'СВ',
        'C': 'штиль',
    }
    form_station_info = {"image_path": "", 'station': "", "temp": "", "feels_like": "", "icon": "",
                         "condition": "", "wind_speed": "", "pressure_mm": "", "wind_dir_from": "", "wind_dir_to": ""}

    stations_data = []
    for el_station in stations:
        weather_data = get_weather(el_station)
        image_path = ""
        temperature = weather_data['temp']
        feels_like = weather_data["feels_like"]
        icon = weather_data["icon"]
        condition = conditions_ru[weather_data["condition"]]
        wind_speed = weather_data['wind_speed']
        pressure_mm = weather_data['pressure_mm']
        wind_dir_from = wind_dir_ru[weather_data['wind_dir'].upper()]
        wind_dir_to = to_wind_dir_ru_eng[wind_dir_ru[weather_data['wind_dir'].upper()]]

        # делаем форму
        added_form = form_station_info.copy()
        added_form['image_path'] = image_path
        added_form['station'] = el_station
        added_form['temp'] = temperature
        added_form['feels_like'] = feels_like
        added_form["icon"] = icon
        added_form["condition"] = condition
        added_form["wind_speed"] = wind_speed
        added_form['pressure_mm'] = pressure_mm
        added_form['wind_dir_from'] = wind_dir_from
        added_form['wind_dir_to'] = wind_dir_to
        stations_data.append(added_form)

    return render_template('list_stations.html', **CONST_PARAMS, title=line_name,
                           line_name=line_name, stations=stations, stations_data=stations_data)
