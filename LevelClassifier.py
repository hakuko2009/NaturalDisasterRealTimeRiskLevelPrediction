import os
import pickle

import pandas as pd
import sklearn
import DataConvert
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier as KNN
from starlette.responses import JSONResponse

source_file = 'data/weather_data_for_training.csv'
app = FastAPI()


# api key for current weather: c3a17117399f5b827712b21d570fd21b


@app.get('/')
def basic_view():
    return {"WELCOME": "GO TO /docs route, or /post or send post request to /predict "}


@app.get('/predict/', response_class=JSONResponse)
def predict(temp: float, pressure: float, humidity: float, clouds: float, wind_speed: float, wind_deg: float,
            weather_main: str, weather_des: str, rain_1h: float):
    detectionFile = open('detection.pickle', 'rb')
    loadedModel = pickle.load(detectionFile)
    detectionFile.close()

    weatherMainFile = open('WeatherMainEncoder.pickle', 'rb')
    weatherMainEn = pickle.load(weatherMainFile)
    weatherMainFile.close()

    weatherDescFile = open('WeatherDescEncoder.pickle', 'rb')
    weatherDescEn = pickle.load(weatherDescFile)
    weatherDescFile.close()

    encodedWeatherMain = weatherMainEn.transform([weather_main])
    encodedWeatherDesc = weatherDescEn.transform([weather_des])

    caseDict = [[temp, pressure, humidity, clouds, wind_speed, wind_deg, encodedWeatherMain[0], encodedWeatherDesc[0], rain_1h]]

    # train here
    result = loadedModel.predict(caseDict)[0]
    return JSONResponse(content=jsonable_encoder(obj=int(result)), media_type="application/json")


def train_and_test():
    if not (os.path.exists(source_file)):
        DataConvert.cleanAndConvert()

    data = pd.read_csv(source_file, encoding='utf8')

    # labelEncoder = preprocessing.LabelEncoder()
    weatherMain = preprocessing.LabelEncoder()
    weatherDesc = preprocessing.LabelEncoder()

    data['Weather_main'] = weatherMain.fit_transform(data['Weather_main'])
    data['Weather_des'] = weatherDesc.fit_transform(data['Weather_des'])

    pickle.dump(weatherMain, open('WeatherMainEncoder.pickle', 'wb'))
    pickle.dump(weatherDesc, open('WeatherDescEncoder.pickle', 'wb'))

    X = data[['Temp', 'Pressure', 'Humidity', 'Clouds', 'Wind_speed', 'Wind_deg',
              'Weather_main', 'Weather_des',
              'Rain_1h']]
    Y = data['Risk_level']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    knn = KNN(n_neighbors=35)
    knn.fit(X_train, Y_train)
    Y_pred = knn.predict(X_test)
    accuracy = sklearn.metrics.accuracy_score(Y_test, Y_pred)
    print(accuracy)

    file = open('detection.pickle', 'wb')
    pickle.dump(knn, file)


class LevelClassifier:
    def __init__(self):
        pass


if __name__ == '__main__':
    train_and_test()
