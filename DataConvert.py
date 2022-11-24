import os

import openpyxl
import pandas as pd


def cleanAndConvert():
    # Open Excel file
    filePath = "rawData"
    os.chdir(filePath)
    excelFile = os.listdir('.')
    wb = openpyxl.load_workbook(excelFile[0])
    sheet = wb.active
    # Delete the non-informative rows
    sheet.delete_rows(0, amount=6)
    print("delete 6 first row")

    # Replace value with risk level
    sheet[f'AY1'].value = "Calculated Risk Level"
    i = 1
    while str(sheet[f'A{i + 1}'].value) != 'None':
        data = 0
        i = i + 1

        ##
        # Need update
        ##
        # Total Deaths
        if str(sheet[f'AI{i}'].value) == 'None':
            sheet[f'AI{i}'].value = 0
        # Total Affected
        if str(sheet[f'AM{i}'].value) == 'None':
            sheet[f'AM{i}'].value = 0
        # Total Damages
        if str(sheet[f'AS{i}'].value) == 'None':
            sheet[f'AS{i}'].value = 0

        # Convert to 1->3 scale
        totalDeaths = int(str(sheet[f'AI{i}'].value))
        if totalDeaths == 0:
            sheet[f'AI{i}'].value = 0
        elif 0 < totalDeaths <= 10:
            sheet[f'AI{i}'].value = 1
        elif 10 < totalDeaths < 100:
            sheet[f'AI{i}'].value = 2
        else:
            sheet[f'AI{i}'].value = 3
        data = data + int(sheet[f'AI{i}'].value)

        # Column AM: Total Affected
        totalAffected = int(str(sheet[f'AM{i}'].value))
        if totalAffected == 0:
            sheet[f'AM{i}'].value = 0
        elif 0 < totalAffected <= 500:
            sheet[f'AM{i}'].value = 1
        elif 500 < totalAffected < 50000:
            sheet[f'AM{i}'].value = 2
        else:
            sheet[f'AM{i}'].value = 3
        data = data + int(sheet[f'AM{i}'].value)

        # Column AS: Adjusted Total Damages (US$)
        totalDamages = int(str(sheet[f'AS{i}'].value))
        if totalDamages == 0:
            sheet[f'AS{i}'].value = 0
        elif 0 < totalDamages < 50000:
            sheet[f'AS{i}'].value = 1
        elif 50000 < totalDamages < 100000:
            sheet[f'AS{i}'].value = 2
        else:
            sheet[f'AS{i}'].value = 3
        data = data + int(sheet[f'AS{i}'].value)

        # Calculate risk level in average
        sheet[f'AY{i}'].value = int(round(data/3, 0))

    # Save and close file
    wb.save(excelFile[0])
    print(excelFile[0] + ' complete')

    # Convert .xlsx file to .csv file
    fullPath = "C:/Users/Administrator/PycharmProjects/NaturalDisasterRealTimeRiskLevelPrediction"
    read_file = pd.read_excel(fullPath + r'/rawData/emdat_public.xlsx')
    read_file.to_csv(fullPath + r'/data/emdat_public.csv', index=None, header=True)
