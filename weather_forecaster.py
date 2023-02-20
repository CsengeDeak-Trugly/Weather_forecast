import requests
from pprint import pprint
from datetime import datetime
from collections import OrderedDict

api_key = *******
one_call_api = 'https://api.openweathermap.org/data/2.5/forecast'
geocoding_api = 'https://api.openweathermap.org/data/2.5/weather'

def get_coordinates(city):
    geo_payload = { 'q': city, 'appid': api_key}
    geo_resp = requests.get(geocoding_api, params=geo_payload)
    geo_resp=geo_resp.json()
    return geo_resp['coord']['lat'], geo_resp['coord']['lon']

def get_weather(lat, lon, dt):
    weather_payload = {'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric', 'lang': 'hu', 'dt': dt}
    weather_resp = requests.get(one_call_api, params=weather_payload)
    weather_resp = weather_resp.json()
    sunrise_ts = weather_resp['city']['sunrise']
    sunset_ts = weather_resp['city']['sunset']
    weather_resp['city']['sunrise'] = datetime.utcfromtimestamp(sunrise_ts).strftime('%H:%M:%S')
    weather_resp['city']['sunset'] = datetime.utcfromtimestamp(sunset_ts).strftime('%H:%M:%S')
    weather_data = []
    for forecast in weather_resp['list']:
        weather_data.append(OrderedDict({
            'dt_txt': forecast['dt_txt'],
            'country': weather_resp['city']['country'],
            'name': weather_resp['city']['name'],
            'sunrise': weather_resp['city']['sunrise'],
            'sunset': weather_resp['city']['sunset'],
            'temp_max': forecast['main']['temp_max'],
            'temp_min': forecast['main']['temp_min'],
            'description': forecast['weather'][0]['description'],
            'main': forecast['weather'][-1]['main'],
            'wind': forecast['wind']
        }))
    return weather_data

def main():
    coordinates = get_coordinates('Törökbálint')
    date_time = int(datetime.now().timestamp())
    weather = get_weather(coordinates[0], coordinates[1], date_time)
    pprint(weather)
    
main()

