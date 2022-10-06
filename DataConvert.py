import pandas as pd
import openpyxl
import os
import sys


def cleanAndConvert():
    # Open Excel file
    filePath = "rawData"
    os.chdir(filePath)
    excelFile = os.listdir('.')
    wb = openpyxl.load_workbook(excelFile[0])
    sheet = wb.active

    # Replace value with risk level
    sheet[f'AY7'].value = "Calculated Risk Level"
    i = 8
    while str(sheet[f'A{i}'].value) != 'None':
        data = 0
        i = i + 1
        # Column AI: Total Deaths
        # Skip case with missing value
        if str(sheet[f'AI{i}'].value) == 'None' or str(sheet[f'AM{i}'].value) == 'None' \
                or str(sheet[f'AS{i}'].value) == 'None':
            continue

        totalDeaths = int(str(sheet[f'AI{i}'].value))
        if totalDeaths == 0:
            sheet[f'AI{i}'].value = 0
        elif 0 < totalDeaths <= 20:
            sheet[f'AI{i}'].value = 1
        elif 20 < totalDeaths < 100:
            sheet[f'AI{i}'].value = 2
        else:
            sheet[f'AI{i}'].value = 3
        data = data + int(sheet[f'AI{i}'].value)

        # Column AM: Total Affected
        totalAffected = int(str(sheet[f'AM{i}'].value))
        if totalAffected == 0:
            sheet[f'AM{i}'].value = 0
        elif 0 < totalAffected <= 1000:
            sheet[f'AM{i}'].value = 1
        elif 1000 < totalAffected < 1000000:
            sheet[f'AM{i}'].value = 2
        else:
            sheet[f'AM{i}'].value = 3
        data = data + int(sheet[f'AM{i}'].value)

        # Column AS: Adjusted Total Damages (US$)
        totalDamages = int(str(sheet[f'AS{i}'].value))
        if totalDamages == 0:
            sheet[f'AS{i}'].value = 0
        elif 0 < totalDamages < 100000:
            sheet[f'AS{i}'].value = 1
        elif 100000 < totalDamages < 5000000:
            sheet[f'AS{i}'].value = 2
        else:
            sheet[f'AS{i}'].value = 3
        data = data + int(sheet[f'AS{i}'].value)

        # Calculate risk level in average
        sheet[f'AY{i}'].value = data / 3

    # Save and close file
    wb.save(excelFile[0])
    print(excelFile[0] + ' complete')

    # Convert .xlsx file to .csv file
    fullPath = "C:/Users/Administrator/PycharmProjects/NaturalDisasterRealTimeRiskLevelPrediction"
    read_file = pd.read_excel(fullPath + r'/rawData/emdat_public_2022_09_24.xlsx')
    read_file.to_csv(fullPath + r'/data/emdat_public_2022_09_24.csv', index=None, header=True)
    sys.exit()


if __name__ == "__main__":
    cleanAndConvert()
