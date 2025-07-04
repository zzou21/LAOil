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
    
    def viscosity(self):

        # newspaperCount = self.csvContentAsDf["NewspaperTitle"].value_counts()
        # newspaperRepeatedCount = 0
        # for paper, count in newspaperCount.items():
        #     if count > 5:
        #         print(paper, count)
        #         newspaperRepeatedCount += 1
        # print(newspaperRepeatedCount)

        # cityCount = self.csvContentAsDf["City"].value_counts()
        # cityRepeatedCount = 0
        # for city, count in cityCount.items():
        #     if count > 1:
        #         print(city, count)
        #         cityRepeatedCount += 1
        # print(cityRepeatedCount)

        stateCount = self.csvContentAsDf["State"].value_counts()
        stateRepeatedCount = 0
        for state, count in stateCount.items():
            if count > 5:
                print(state, count)
                stateRepeatedCount += 1
        print(stateRepeatedCount)
    
    def nonlocality(self):
        
        locationTimeDictByYear = {}
        for row in self.csvContentAsDf.itertuples():
            publicationYear = int(row.IssueDate[-4:])
            if publicationYear not in locationTimeDictByYear:
                locationTimeDictByYear[publicationYear] = []
            locationTimeDictByYear[publicationYear].append([row.NewspaperTitle, row.IssueDate, row.City, row.State, row.Region])

        locationTimeDictByHalfDecade = {}
        for row in self.csvContentAsDf.itertuples():
            publicationYear = int(row.IssueDate[-4:])
            offset = (publicationYear - 1890) % 10
            halfDecadeStart = publicationYear - offset if offset < 5 else publicationYear - offset + 5
            halfDecadeKey = f"{halfDecadeStart} to {halfDecadeStart + 4}"
            if halfDecadeKey not in locationTimeDictByHalfDecade:
                locationTimeDictByHalfDecade[halfDecadeKey] = []
            locationTimeDictByHalfDecade[halfDecadeKey].append([
                row.NewspaperTitle, row.IssueDate, row.City, row.State, row.Region
            ])
            
        # cityCounterList = []
        # for publicationYear, info in locationTimeDictByYear.items():
        #     citySet = set()
        #     for city in info:
        #         citySet.add(city[2])
        #     cityCounterList.append([publicationYear, len(citySet)])
        # cityCounterList = sorted(cityCounterList)
        # print(cityCounterList)

        # stateCounterList = []
        # for publicationYear, info in locationTimeDictByYear.items():
        #     stateSet = set()
        #     for state in info:
        #         stateSet.add(state[3])
        #     stateCounterList.append([publicationYear, len(stateSet)])
        # stateCounterList = sorted(stateCounterList)
        # print(stateCounterList)

        regionCounterList = []
        for publicationYear, info in locationTimeDictByYear.items():
            regionSet = set()
            for region in info:
                regionSet.add(region[4])
            regionCounterList.append([publicationYear, len(regionSet)])
        regionCounterList = sorted(regionCounterList)
        print(regionCounterList)
        
        # stateCounterListHalfDecade = []
        # for publicationRegion, info in locationTimeDictByHalfDecade.items():
        #     stateSet = set()
        #     for paper in info:
        #         stateSet.add(paper[3])
        #     stateCounterListHalfDecade.append([publicationRegion, len(stateSet)])
        # stateCounterListHalfDecade = sorted(stateCounterListHalfDecade)
        # print(stateCounterListHalfDecade)
        
        # cityCounterListHalfDecade = []
        # for publicationRegion, info in locationTimeDictByHalfDecade.items():
        #     citySet = set()
        #     for paper in info:
        #         citySet.add(paper[2])
        #     cityCounterListHalfDecade.append([publicationRegion, len(citySet)])
        # cityCounterListHalfDecade = sorted(cityCounterListHalfDecade)
        # print(cityCounterListHalfDecade)

        regionCounterListHalfDecacde = []
        for publicationRegion, info in locationTimeDictByHalfDecade.items():
            regionSet = set()
            for paper in info:
                regionSet.add(paper[4])
            regionCounterListHalfDecacde.append([publicationRegion, len(regionSet)])
        regionCounterListHalfDecacde = sorted(regionCounterListHalfDecacde)
        print(regionCounterListHalfDecacde)



    
if __name__ == "__main__":
    csvFile = "/Users/Jerry/Desktop/DHproj-reading/LAOilProject/LAOil/DataFolder/updatedCSVNewspaperCoordinatesCensusRegion.csv"
    locationAnalysisMachine = locationAnalysis(csvFile)
    # locationAnalysisMachine.locationAccumulation()
    locationAnalysisMachine.nonlocality()