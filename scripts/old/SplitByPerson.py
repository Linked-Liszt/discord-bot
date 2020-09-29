import pandas as pd
import numpy as np

RAW_DATA_PATH = "REMOVED FOR GITHUB"
	
RAW_EXPORT_PATHS = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]
					
ACTUAL_NAMES = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]

ActualNamesItr = iter(ACTUAL_NAMES)
RawData = pd.read_csv(RAW_DATA_PATH)
RawData.set_index("Author")

for ExportDataPath in RAW_EXPORT_PATHS:
	SinglePerson = RawData.loc[RawData["Author"] == next(ActualNamesItr)]
	SinglePerson.to_csv(ExportDataPath)
	print (SinglePerson)
