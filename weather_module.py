import requests
from dotenv import load_dotenv
import os 

load_dotenv()
weather_api_key = os.getenv('weather_key')

def get_lat_long(city_name :str):

    url = "http://api.openweathermap.org/geo/1.0/direct"

    parameters = {
        'q': city_name,
        'appid': weather_api_key,
        'limit': '2'
    }

    try:
        response = requests.get(url=url, params = parameters)
        response.raise_for_status()
        data= response.json()

        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            print('no data found')

    except requests.exceptions.RequestException as e:
        print('Error',e)


    