'''This code adds the respective census region that a publication city belongs to.'''
import pandas as pd

class addRegionToFrame:
    def __init__(self, inputOutputFilePath):
        self.inputOutputFilePath = inputOutputFilePath
    
    def addRegion(self):
        mainDF = pd.read_csv(self.inputOutputFilePath)
        def createRegion(data):
            if data in ["Connecticut", "Main", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont"]:
                return "New England"
            elif data in ["New Jersey", "New York", "Pennsylvania"]:
                return "Middle Atlantic"
            elif data in ["Indiana", "Illinois", "Michigan", "Ohio", "Wisconsin"]:
                return "East North Central"
            elif data in ["Iowa", "Kansas", "Minnesota", "Missouri", "Nebraska", "North Dakota", "South Dakota"]:
                return "West North Central"
            elif data in ["Delaware", "District Of Columbia", "Florida", "Georgia", "Maryland", "North Carolina", "South Carolina", "Virginia", "West Virginia"]:
                return "South Atlantic"
            elif data in ["Alamaba", "Kentucky", "Mississippi", "Tennessee"]:
                return "East South Central"
            elif data in ["Arkansas", "Louisiana", "Oklahoma", "Texas"]:
                return "West South Central"
            elif data in ["Arizona", "Colorado", "Idaho", "New Mexico", "Montana", "Utah", "Nevada", "Wyoming"]:
                return "Mountain"
            elif data in ["California", "Alaska", "Hawaii", "Oregon", "Washington"]:
                return "Pacific"
            
        mainDF["Region"] = mainDF["State"].apply(createRegion)
        mainDF.to_csv(self.inputOutputFilePath, index = False, encoding = "utf-8")

if __name__ == "__main__":
    inputOutputFilePath = "/Users/Jerry/Desktop/DH proj-reading/LAOilNewspaper/LAOil/updatedCSVNewspaperCoordinates.csv"
    addRegionTool = addRegionToFrame(inputOutputFilePath)
    addRegionTool.addRegion()