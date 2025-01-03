'''To combine the location data (latitude and longitude) of each city, we need to pair the LOC API output with the GNIS geographic names data and combine the two into one csv'''
import pandas as pd
class findLocationData:
    def __init__(self, newspaperCSV, GNISCSV, outputCSVLocation):
        self.newspaperCSV = newspaperCSV
        self.GNISCSV = GNISCSV
        self.outputCSVLocation = outputCSVLocation
    
    def readGNISCSV(self):
        GNISData = pd.read_csv(self.GNISCSV, sep = ",", dtype = str)
        # print(f"Column titles: {GNISData.columns}")
        GNISDataFilteredCivil = GNISData[ #filter original raw dataframe so that we only keep the rows from GNIS that might be related to a town or a city. This is to optimize the merging and comparison procedures in the future.
            GNISData["feature_name"].str.contains("city", case = False, na = False) |
            GNISData["feature_name"].str.contains("town", case = False, na = False) |
            GNISData["feature_class"].str.contains("civil", case = False, na = False)
        ]
        # print(GNISDataFilteredCivil.head())
        # print(len(GNISDataFilteredCivil.index))
        return GNISDataFilteredCivil
    
    def readNewspaperCSV(self):
        newspaperDataRaw = pd.read_csv(self.newspaperCSV, sep = ",", dtype = str)
        newspaperDataRaw = newspaperDataRaw.drop("Unnamed: 0", axis = 1)
        # print(f"Column titles: {newspaperDataRaw.columns}")
        # print(newspaperDataRaw.head())

        def cleanCityAndStates(column):
            # temporaryCityList = column.split(",")
            if "Chicago" in column:
                editedColumn = "Chicago, Illinois"
            elif "District Of Columbia" in column:
                editedColumn = "Washington, District Of Columbia"
            elif "O'Neill" in column and "Nebraska" in column:
                editedColumn = "O'Neill, Nebraska"

            elif "', '" in column:
                column = column.replace("'", "")
                temporaryColumnList = column.split(",")
                temporaryColumnList = [city.strip() for city in temporaryColumnList]
                
                editedColumn = ", ".join(temporaryColumnList[-2:])
            else:
                editedColumn = column
            return editedColumn
        
        newspaperDataRaw["City"] = newspaperDataRaw["City"].apply(cleanCityAndStates)

        newspaperDataRaw["City"] = newspaperDataRaw["City"].apply(lambda x: x.split(", "))

        newspaperDataRaw[["City", "State"]] = pd.DataFrame(newspaperDataRaw["City"].tolist(), index=newspaperDataRaw.index)
        return newspaperDataRaw
    
    def compareCSVData(self):
        newspaperData = self.readNewspaperCSV()
        GNISData = self.readGNISCSV()
        #newspaperData = newspaperData.drop_duplicates(subset = ["City", "Newspaper Title"]) # This line eliminates duplicated publication city and newspaper. NOTE that they are NOT duplicated publications, as they were published by the same publisher but in different dates.
        # newspaperData["City"] = newspaperData["City"].apply(lambda x: "City of " + x)
        
        print(f"readNewspaper: {newspaperData.head()}")
        print(f"length of newspaperData: {len(newspaperData.index)}")
        print(f"GNIS {GNISData.columns}")
        print(f"GNIS: {GNISData.head()}")
        # GNISData["key"] = GNISData["feature_name"].str.extract(f"({'|'.join(newspaperData['City'])})", expand=False)
        # newspaperData = pd.merge(newspaperData, GNISData[["key", "state_name", "prim_long_dec", "prim_lat_dec"]], left_on=["City", "State"], right_on=["key", "state_name"], how="left")
        
        def partialMatch(row, gnis_data):
            matches = gnis_data[(gnis_data['feature_name'].str.contains(row['City'], case=False)) &
                                (gnis_data["state_name"].str.contains(row["State"], case=False))]
            if not matches.empty:
                return matches.iloc[0][['prim_long_dec', 'prim_lat_dec']]  # Return the first matching row
            return pd.Series([None, None], index=['prim_long_dec', 'prim_lat_dec'])

        # Apply the function to each row of newspaperData
        newspaperCityCoordinates = newspaperData.apply(
            lambda row: partialMatch(row, GNISData),
            axis=1
        )

        # Combine the merged columns with the original DataFrame
        mergedNewspaperDataCoordinates = pd.concat([newspaperData, newspaperCityCoordinates], axis=1)
        mergedNewspaperDataCoordinates = mergedNewspaperDataCoordinates[["Newspaper Title", "Issue Date", "Page Number", "City", "State", "PDF Link", "prim_long_dec", "prim_lat_dec"]]
        # newspaperData.drop(columns=["key"], inplace=True)
        print(f"Merged newspaper data: {mergedNewspaperDataCoordinates.head()}")
        print(f"Merged newspaper data: {mergedNewspaperDataCoordinates.columns}")
        print(f"merged newsppaer data length: {len(mergedNewspaperDataCoordinates.index)}")
        mergedNewspaperDataCoordinates.to_csv(self.outputCSVLocation, index = False, encoding = "utf-8")

if __name__ == "__main__":
    newspaperCSV = "updatedCSVNewspaper.csv"
    GNISCSV = "C:/Users/zz341/Desktop/combinedAllStatesContent.csv"
    # GNISCSV = "/Users/Jerry/Desktop/DH proj-reading/LAOilNewspaper/GNISDomesticNamesAllStates/combinedAllStatesContent.csv"
    outputCSVLocation = "updatedCSVNewspaperCoordinates.csv"
    locationDataFindMachine = findLocationData(newspaperCSV, GNISCSV, outputCSVLocation)
    # locationDataFindMachine.readGNISCSV()
    # locationDataFindMachine.readNewspaperCSV()
    locationDataFindMachine.compareCSVData()