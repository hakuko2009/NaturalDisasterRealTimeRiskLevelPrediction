import os
import pickle

import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB

import DataConvert
import DataLoader

source_file = 'data/emdat_public_2022_10_18.csv'


def _case_features(caseFeatures):
    return {
        'year': caseFeatures[1],
        'type': caseFeatures[2],
        'region': caseFeatures[3],
        'magValue': caseFeatures[4],
        'magScale': caseFeatures[5],
        'startMonth': caseFeatures[6],
        'endMonth': caseFeatures[7]
    }


class LevelClassifier:
    def __init__(self):
        pass

    def get_features(self):
        # classify into 4 level (0 -> 3)

        feature_set = DataLoader.get_case_list()

        return feature_set

    def train_and_test(self):
        if not (os.path.exists(source_file)):
            DataConvert.cleanAndConvert()

        data = pd.read_csv(source_file, encoding='utf8')
        data = data[
            ['Dis No', 'Year', 'Disaster Type', 'Region', 'Dis Mag Value', 'Dis Mag Scale', 'Start Month',
             'End Month', 'Calculated Risk Level']]

        labelEncoder = preprocessing.LabelEncoder()
        typeEncoder = preprocessing.LabelEncoder()
        regionEncoder = preprocessing.LabelEncoder()
        magScaleEncoder = preprocessing.LabelEncoder()

        data['Disaster Type'] = typeEncoder.fit_transform(data['Disaster Type'])
        data['Region'] = regionEncoder.fit_transform(data['Region'])
        data['Dis Mag Scale'] = magScaleEncoder.fit_transform(data['Dis Mag Scale'])

        pickle.dump(typeEncoder, open('TypeEncoder.pickle', 'wb'))
        pickle.dump(regionEncoder, open('RegionEncoder.pickle', 'wb'))
        pickle.dump(magScaleEncoder, open('MagScaleEncoder.pickle', 'wb'))

        X = data[['Year', 'Disaster Type', 'Region', 'Dis Mag Value', 'Dis Mag Scale', 'Start Month',
                  'End Month']]
        Y = labelEncoder.fit_transform(data['Calculated Risk Level'])

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20)
        print(X_train)
        print(Y_train)

        naiveBayesModel = BernoulliNB()
        naiveBayesModel.fit(X_train, Y_train)
        file = open('detection.pickle', 'wb')
        pickle.dump(naiveBayesModel, file)


if __name__ == "__main__":
    gp = LevelClassifier()
    gp.train_and_test()
    # print('Accuracy: %f' % metrics.accuracy_score(y_test, y_pred))

    year = 2000
    type = "Flood"
    region = "South-Eastern Asia"
    magValue = 1000
    magScale = "Kph"
    startMonth = 5
    endMonth = 6

    detectionFile = open('detection.pickle', 'rb')
    model = pickle.load(detectionFile)
    detectionFile.close()

    typeFile = open('TypeEncoder.pickle', 'rb')
    typeEn = pickle.load(typeFile)
    typeFile.close()

    regionFile = open('RegionEncoder.pickle', 'rb')
    regionEn = pickle.load(regionFile)
    regionFile.close()

    magScaleFile = open('MagScaleEncoder.pickle', 'rb')
    magScaleEn = pickle.load(magScaleFile)
    magScaleFile.close()

    encodedType = typeEn.transform([type])
    encodedRegion = regionEn.transform([region])
    encodedMagScale = magScaleEn.transform([magScale])

    caseDict = [[year, encodedType[0], encodedRegion[0], magValue,
                 encodedMagScale[0], startMonth, endMonth]]

    print(caseDict)
    print(model.predict(caseDict))

    # print('\n%s is classified as %s' % (case, gp.classify(case)))
