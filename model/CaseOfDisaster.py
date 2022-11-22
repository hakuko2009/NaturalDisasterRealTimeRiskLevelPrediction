class CaseOfDisaster:
    def __init__(self, temp, pressure, humidity, clouds, wind_speed, weather_main, weather_des, rain_1h):
        self.temp = temp
        self.pressure = pressure
        self.humidity = humidity
        self.clouds = clouds
        self.wind_speed = wind_speed
        self.weather_main = weather_main
        self.weather_des = weather_des
        self.rain_1h = rain_1h
        self.level = 1

    def __getitem__(self, item):
        return item
