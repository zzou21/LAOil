# This file cleans up the CSV output gained from the Library of Congress Chronicling America API (https://libraryofcongress.github.io/data-exploration/loc.gov%20JSON%20API/Chronicling_America/ChronAm_analyzing_specific_titles_limit_results.html)

import json, pandas as pd

def processExportedCSV(csvPath, savePath):
    dataFrame = pd.read_csv(csvPath)
    columnsToIterateCleanListFormat = ["Newspaper Title", "City", "State"] #This is to get rid of the ["title"] bracket and quotation marks that came with the LOC API for these three columns.
    for column in columnsToIterateCleanListFormat:
        dataFrame[column] = dataFrame[column].apply(lambda x: x[2:-2])
        dataFrame[column] = dataFrame[column].apply(lambda x: x[:-1] if x.endswith(".") else x)
        dataFrame[column] = dataFrame[column].apply(lambda x: x.title())
    dataFrame["City"] = dataFrame["City"] + ", " + dataFrame["State"]
    for name in dataFrame["City"]:
        print(name)
    dataFrame = dataFrame.drop(columns=["State"])
    dataFrame.to_csv(savePath, index = False, encoding = "utf-8")

if __name__ == "__main__":
    csvPath = "/Users/Jerry/Desktop/DH proj-reading/LAOilNewspaper/LAOil/LOCLAOilInitialExtractWithoutBlankCities.csv"
    savePath = "/Users/Jerry/Desktop/DH proj-reading/LAOilNewspaper/LAOil/updatedCSV.csv"
    processExportedCSV(csvPath, savePath)