# This file helps to analyze the geospatial spread of the newspapers
# import pandas as pd
import pandas as pd

class locationAnalysis:
    def __init__ (self, csvFile):
        self.csvContentAsDf = pd.read_csv(csvFile, sep=",", dtype=str)
    
    def locationAccumulation(self):
        newspaperCount = self.csvContentAsDf["NewspaperTitle"].value_counts()
        print(f"Total number of newspaper include: {len(newspaperCount)}")

        # for paper, count in newspaperCount.items():
        #     print(paper, count)


        stateCount = self.csvContentAsDf["State"].value_counts()
        print(f"Total number of states include: {len(stateCount)}")
        # for state, count in stateCount.items():
        #     print(state, count)

        cityCount = self.csvContentAsDf["City"].value_counts()
        print(f"Total number of city include: {len(cityCount)}")
        # for city, count in cityCount.items():
        #     print(city, count)

        censusDistrictCount = self.csvContentAsDf["Region"].value_counts()
        print(f"Total number of census district include: {len(censusDistrictCount)}")


if __name__ == "__main__":
    print("test")
    csvFile = "/Users/Jerry/Desktop/DHproj-reading/LAOilProject/LAOil/DataFolder/updatedCSVNewspaperCoordinatesCensusRegion.csv"
    locationAnalysisMachine = locationAnalysis(csvFile)
    locationAnalysisMachine.locationAccumulation()