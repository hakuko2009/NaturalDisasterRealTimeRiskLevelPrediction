import csv
import os

import DataConvert

source_file = 'data/emdat_public_2022_09_24.csv'


def get_case_list():
    print('Get the list of disaster for each level')
    caseDict = get_data_from_csv()
    print('Done get data')

    level_0 = list()
    level_1 = list()
    level_2 = list()
    level_3 = list()

    for disNo in caseDict:
        features = caseDict[disNo]
        case = (disNo, features[0], features[1], features[2],
                features[3], features[4], features[5], features[6])
        print('case = ', case)
        calculatedRiskLevel = features[6]
        if calculatedRiskLevel == 0:
            level_0.append(case)
        elif calculatedRiskLevel == 1:
            level_1.append(case)
        elif calculatedRiskLevel == 2:
            level_2.append(case)
        else:
            level_3.append(case)

    return level_0, level_1, level_2, level_3


def get_data_from_csv():
    # Convert csv data to dictionary
    # DataConvert.cleanAndConvert()

    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path) + '/'

    names = dict()
    with open(dir_path + '/' + source_file, 'r', newline='', encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            # Skip case with missing value
            if str(row['Calculated Risk Level']) == '' or str(row['Year']) == 'None' \
                    or str(row['Disaster Subtype']) == 'None' or str(row['Country']) == 'None' \
                    or str(row['Region']) == 'None' or str(row['Start Month']) == '' \
                    or str(row['End Month']) == '':
                continue

            names[row['Dis No']] = [int(row['Year']), str(row['Disaster Subtype']), str(row['Country']),
                                    str(row['Region']), int(float(row['Start Month'])), int(float(row['End Month'])),
                                    int(float(row['Calculated Risk Level']))]

    return names


if __name__ == "__main__":
    print(get_case_list())
