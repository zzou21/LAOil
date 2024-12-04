'''To combine the location data (latitude and longitude) of each city, we need to pair the LOC API output with the GNIS geographic names data and combine the two into one csv'''

import pandas as pd

class findLocationData:
    def __init__(self, newspaperCSV, GNISCSV, outputCSVLocation):
        self.newspaperCSV = newspaperCSV
        self.GNISCSV = GNISCSV
        self.outputCSVLocation = outputCSVLocation
    
    def readGNISCSV(self):
        GNISData = pd.read_csv(self.GNISCSV, sep = ",", dtype = str)
        print(f"Column titles: {GNISData.columns}")
        GNISDataFilteredCivil = GNISData[ #filter original raw dataframe
            GNISData["feature_name"].str.contains("city", case = False, na = False) |
            GNISData["feature_name"].str.contains("town", case = False, na = False) |
            GNISData["feature_class"].str.contains("civil", case = False, na = False)
        ]
        print(GNISDataFilteredCivil.head())
        print(len(GNISDataFilteredCivil.index))
        return GNISDataFilteredCivil
    
    def readNewspaperCSV(self):
        newspaperDataRaw = pd.read_csv(self.newspaperCSV, sep = ",", dtype = str)
        newspaperDataRaw = newspaperDataRaw.drop("Unnamed: 0", axis = 1)
        print(f"Column titles: {newspaperDataRaw.columns}")
        print(newspaperDataRaw.head())
        



if __name__ == "__main__":
    newspaperCSV = "updatedCSVNewspaper.csv"
    GNISCSV = "C:/Users/zz341/Desktop/combinedAllStatesContent.csv"
    outputCSVLocation = ""
    locationDataFindMachine = findLocationData(newspaperCSV, GNISCSV, outputCSVLocation)
    # locationDataFindMachine.readGNISCSV()
    locationDataFindMachine.readNewspaperCSV()