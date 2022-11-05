import csv
import os.path

import pandas as pd

import DataConvert

source_file = 'data/emdat_public_2022_10_18.csv'


def get_case_list():
    print('Get the list of disaster for each level')
    caseDict = get_data_from_csv()
    print('Done get data')

    level = list()
    featureList = list()
    resultList = list()

    for disNo in caseDict:
        features = caseDict[disNo]
        case = (features[0], features[1], features[2],
                features[3], features[4], features[5], features[6])
        case = pd.get_dummies(case)
        calculatedRiskLevel = features[7]
        featureList.append(case)
        resultList.append(calculatedRiskLevel)

        level.append(case)

    return featureList, resultList


def get_data_from_csv():
    # Convert csv data to dictionary
    if not (os.path.exists(source_file)):
        DataConvert.cleanAndConvert()

    filePath = os.path.abspath(__file__)
    dir_path = os.path.dirname(filePath) + '/'

    names = dict()
    with open(dir_path + '/' + source_file, 'r', newline='', encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            # Skip case with missing value
            if str(row['Calculated Risk Level']) == '' or str(row['Year']) == 'None' \
                    or str(row['Disaster Type']) == 'None' or str(row['Region']) == 'None' \
                    or str(row['Dis Mag Value']) == '' or str(row['Dis Mag Scale']) == 'None' \
                    or str(row['Start Month']) == '' \
                    or str(row['End Month']) == '':
                continue

            names[row['Dis No']] = [int(float(row['Year'])), str(row['Disaster Type']), str(row['Region']),
                                    int(float(row['Dis Mag Value'])), str(row['Dis Mag Scale']),
                                    int(float(row['Start Month'])), int(float(row['End Month'])),
                                    int(float(row['Calculated Risk Level']))]

    return names


if __name__ == "__main__":
    print(get_case_list())
