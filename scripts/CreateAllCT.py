import pandas as pd
import numpy as np

RAW_DATA_PATHS = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]
	
RAW_EXPORT_PATHS = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]

ExpPathItr = iter(RAW_EXPORT_PATHS)

AllData = pd.read_csv(RAW_DATA_PATHS[0])

for DataPath in range(1, len(RAW_DATA_PATHS)):
	CurrentData = pd.read_csv(RAW_DATA_PATHS[DataPath])
	AllData = AllData.append(CurrentData)
	
AllData.to_csv(RAW_EXPORT_PATHS[0], index=False)
print (len(AllData))