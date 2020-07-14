from pprint import pprint
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re


class WeatherMaker:

    def __init__(self):
        self.site = "https://world-weather.ru/pogoda/russia/saint_petersburg/14days/"
        self.weather_dict = {}

    def get_data(self):
        req = Request(self.site, headers={'User-Agent': 'Mozilla/5.0'})
        web_page = urlopen(req).read().decode("utf-8")
        html_doc = BeautifulSoup(web_page, features="html.parser")
        dates_list_result = html_doc.find_all('a', {'name': re.compile("\d+-\d+-\d+")})
        night_weather_result = html_doc.find_all('tr', {'class': 'evening fourteen-n'})
        day_weather_result = html_doc.find_all('tr', {'class': 'day fourteen-d'})

        for date, day_weather, night_weather in zip(dates_list_result, day_weather_result, night_weather_result):
            date = date.attrs.get('name')
            day = day_weather.find_all('td', {'class': 'weather-day'})[0].text
            night = night_weather.find_all('td', {'class': 'weather-day'})[0].text
            day_sky = (day_weather.find_all('td', {'class': 'weather-temperature'}))[0].find('div').attrs.get('title')
            night_sky = (night_weather.find_all('td', {'class': 'weather-temperature'}))[0].find('div').attrs.get(
                'title')
            day_temperature = (day_weather.find_all('td', {'class': 'weather-temperature'}))[0].find('span').text
            night_temperature = (night_weather.find_all('td', {'class': 'weather-temperature'}))[0].find('span').text
            day_temperature_fill = day_weather.find_all('td', {'class': 'weather-feeling'})[0].text
            night_temperature_fill = night_weather.find_all('td', {'class': 'weather-feeling'})[0].text
            day_rain_prob = day_weather.find_all('td', {'class': 'weather-probability'})[0].text
            night_rain_prob = night_weather.find_all('td', {'class': 'weather-probability'})[0].text
            day_pressure = day_weather.find_all('td', {'class': 'weather-pressure'})[0].text
            night_pressure = night_weather.find_all('td', {'class': 'weather-pressure'})[0].text
            day_humidity = day_weather.find_all('td', {'class': 'weather-humidity'})[0].text
            night_humidity = night_weather.find_all('td', {'class': 'weather-humidity'})[0].text
            self.weather_dict.update({date: [
                {day: {'temperature': day_temperature,
                       'sky': day_sky,
                       'temperature_feeling': day_temperature_fill,
                       'rain_probability': day_rain_prob,
                       'pressure': day_pressure,
                       'humidity': day_humidity},
                 night: {'temperature': night_temperature,
                         'sky': night_sky,
                         'temperature_feeling': night_temperature_fill,
                         'rain_probability': night_rain_prob,
                         'pressure': night_pressure,
                         'humidity': night_humidity}
                 }]})
        # pprint(self.weather_dict)
        return self.weather_dict


WeatherMaker().get_data()
