import csv
import datetime
import json
import os.path
import time
import requests
import pandas as pd

import DataConvert

source_file = 'data/emdat_public_2022_11_22.csv'
dest_file = 'data/weather_data_for_training.csv'


def get_data_from_csv():
    if not (os.path.exists(source_file)):
        DataConvert.cleanAndConvert()

    filePath = os.path.abspath(__file__)
    dir_path = os.path.dirname(filePath) + '/'
    csv_columns = ['No', 'Temp', 'Pressure', 'Humidity', 'Clouds', 'Wind_speed', 'Wind_deg',
                   'Weather_main', 'Weather_des', 'Rain_1h', 'Risk_level']

    case_list = []
    index = 0
    with open(dir_path + '/' + source_file, 'r', newline='', encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            # Skip case with missing value
            if str(row['Calculated Risk Level']) == '' \
                    or str(row['Latitude']) == '' or str(row['Longitude']) == ''\
                    or str(row['Start Year']) == '' or str(row['Start Month']) == '' \
                    or str(row['Start Day']) == '':
                continue

            # Call API to create a new file
            year = int(float(row['Start Year']))
            month = int(float(row['Start Month']))
            day = int(float(row['Start Day']))
            epoch = datetime.date(year=1970, month=1, day=1)
            date_time = datetime.date(year=year, month=month, day=day)
            dt = int((date_time - epoch).total_seconds())

            print("dt: ", dt)

            # lat = 16.03456
            # lon = 108.22903

            lat = float((row['Latitude'].split(' ', 1)[0]))
            lon = float((row['Longitude'].split(' ', 1)[0]))

            response = get_historical_weather_json(lat, lon, dt)
            print(response)
            if response[0] == 200:
                dataDict = json.loads(str(response[1]).replace("'", '"'))
                rain_1h = 0.0

                mainData = dataDict['data'][0]
                temp = float(mainData['temp'])

                pressure = mainData['pressure']
                humidity = mainData['humidity']
                clouds = mainData['clouds']
                wind_speed = mainData['wind_speed']
                wind_deg = mainData['wind_deg']
                weather_main = mainData['weather'][0]['main']
                weather_des = mainData['weather'][0]['description']
                if str(response[1]).__contains__("'rain:'"):
                    rain_1h = mainData['rain']['1h']
                level = int(row['Calculated Risk Level'])

                case_list.append({'No': index + 1, 'Temp': temp, 'Pressure': pressure,
                                  'Humidity': humidity, 'Clouds': clouds,
                                  'Wind_speed': wind_speed, 'Wind_deg': wind_deg,
                                  'Weather_main': weather_main, 'Weather_des': weather_des,
                                  'Rain_1h': rain_1h, 'Risk_level': level})
                print(case_list[index])
                index = index + 1

    try:
        with open(dest_file, 'w', newline='') as destFile:
            writer = csv.DictWriter(destFile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerows(case_list)
    except IOError:
        print("I/O error")


def get_historical_weather_json(lat, lon, dt):
    params = {'lat': lat, 'lon': lon, 'dt': dt, 'appid': "c3a17117399f5b827712b21d570fd21b"}
    request_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    response = requests.get(url=request_url, params=params)
    return response.status_code, response.json()


if __name__ == "__main__":
    get_data_from_csv()
