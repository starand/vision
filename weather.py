# -*- coding: utf-8 -*-
import config
import pyowm

class Weather():
    _owm = pyowm.OWM(config.weatherKey, language='ua')

    def __init__(self, location = 'Lviv'):
        self._location = self._owm.weather_at_place(location)

    def getTemperature(self):
        weather = self._location.get_weather()
        data = weather.get_temperature('celsius')
        return data['temp']

    def getHumidity(self):
        weather = self._location.get_weather()
        return weather.get_humidity()

    def getStatus(self, detailed = True):
        weather = self._location.get_weather()
        return weather.get_detailed_status() if detailed else weather.get_status()

    def getIcon(self):
        weather = self._location.get_weather()
        return weather.get_weather_icon_url() # http://openweathermap.org/img/w/02d.png

    def getSunriseTime(self):
        weather = self._location.get_weather()
        return weather.get_sunrise_time('iso')

    def getSunsetTime(self):
        weather = self._location.get_weather()
        return weather.get_sunset_time('iso')

    def getRain(self):
        weather = self._location.get_weather()
        return weather.get_rain()

    def getSnow(self):
        weather = self._location.get_weather()
        return weather.get_snow()

    def getPressure(self):
        weather = self._location.get_weather()
        return weather.get_pressure()

    def getWind(self):
        weather = self._location.get_weather()
        wind = weather.get_wind()
        return wind['speed']


if __name__ == '__main__':
    weather = Weather()
    print("Temperature: %s C" % weather.getTemperature())
    print("Humidity: %s %%" % weather.getHumidity())
    print("Status: %s" % weather.getStatus())

    print("Sunrize: %s" % weather.getSunriseTime())
    print("Sunset: %s" % weather.getSunsetTime())

    print("Raining: %s" % weather.getRain())
    print("Snow: %s" % weather.getSnow())
    print("Wind: %s" % weather.getWind())
    print("Icon: %s" % weather.getIcon())


#http://api.openweathermap.org/data/2.5/weather?q=lviv&appid=8feff299f40c49ae1b450a56b32426d9

## >>> w.get_clouds()                                     # Get cloud coverage
## 65
## >>> w.get_rain()                                       # Get rain volume
## {'3h': 0}
## >>> w.get_snow()                                       # Get snow volume
## {}
## >>> w.get_wind()                                       # Get wind degree and speed
## {'deg': 59, 'speed': 2.660}
## >>> w.get_humidity()                                   # Get humidity percentage
## 67
## >>> w.get_pressure()                                   # Get atmospheric pressure
## {'press': 1009, 'sea_level': 1038.381}
## >>> w.get_temperature() 