from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    conn = sqlite3.connect('Railway_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM lines')
    lines = cursor.fetchall()
    conn.close()
    return render_template('index.html', lines=lines)


@app.route('/<line_name>')
def show_line(line_name):
    conn = sqlite3.connect('Railway_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stations FROM lines WHERE name = ?', (line_name,))
    stations = cursor.fetchone()[0].split(', ')
    station_weather = {station: get_weather(station) for station in stations}
    conn.close()
    return render_template('index.html', line_name=line_name, stations=stations, station_weather=station_weather)
