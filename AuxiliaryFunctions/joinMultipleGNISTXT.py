'''
This program combines the Domestic names data from GNIS that are stored in 50 different TXT files into one TXT
Data gained from: https://prd-tnm.s3.amazonaws.com/index.html?prefix=StagedProducts/GeographicNames/DomesticNames/
'''
import pandas as pd
import os

class manipulateTXT:
    def __init__(self, multipleTXTJoinFolderPath, storageJoinedOneTXTDestination):
        self.multipleTXTJoinFolderPath = multipleTXTJoinFolderPath
        self.storageJoinedOneTXTDestination = storageJoinedOneTXTDestination
    
    # This function joins multiple TXTs that are in the format of pipe-delimited and join them together. This function only works when all TXT files being joined follow the same pipe-delimited headers, data types, and format.
    def joinMultipleTXT(self):
        takenOneHeader = True
        filePathStorageListToIterate = []
        for txtFile in os.listdir(self.multipleTXTJoinFolderPath):
            if txtFile.endswith(".txt"):
                fullOneFilePath = os.path.join(self.multipleTXTJoinFolderPath, txtFile)
                filePathStorageListToIterate.append(fullOneFilePath)
        filePathStorageListToIterate = sorted(filePathStorageListToIterate, key = lambda x: x[-6:-4])
        
        


if __name__ == "__main__":
    multipleTXTJoinFolderPath = "/Users/Jerry/Desktop/DH proj-reading/LAOilNewspaper/GNISDomesticNamesAllStates/Text"
    storageJoinedOneTXTDestination = "/Users/Jerry/Desktop/DH proj-reading/LAOilNewspaper/GNISDomesticNamesAllStates"
    manipulateTXTArchitecture = manipulateTXT(multipleTXTJoinFolderPath, storageJoinedOneTXTDestination)
    manipulateTXTArchitecture.joinMultipleTXT()
