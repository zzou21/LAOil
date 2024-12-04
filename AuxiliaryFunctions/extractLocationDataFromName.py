'''To combine the location data (latitude and longitude) of each city, we need to pair the LOC API output with the GNIS geographic names data and combine the two into one csv'''

import pandas as pd

class findLocationData:
    def __init__(self, newspaperCSV, GNISCSV, outputCSVLocation):
        self.newspaperCSV = newspaperCSV
        self.GNISCSV = GNISCSV
        self.outputCSVLocation = outputCSVLocation
    
    def readGNISCSV(self):


if __name__ == "__main__":
    newspaperCSV = ""