import pandas as pd
import numpy as np

RAW_DATA_PATHS =  [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]
	
RAW_EXPORT_PATHS =  [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]

					
ExportPathItr = iter(RAW_EXPORT_PATHS)

for RawDataPath in RAW_DATA_PATHS:
	RawData = pd.read_csv(RawDataPath)
	RawData["Date"] = pd.to_datetime(RawData["Date"])
	RawData.index = RawData["Date"]

	times= pd.DatetimeIndex(RawData["Date"])
	GroupedData = RawData.groupby(times.hour).count()
	GroupedData  = GroupedData.iloc[:,0:1] 
	GroupedData.index.names = ["Hour"]
	GroupedData.columns = ["Count"]
	GroupedData.to_csv(next(ExportPathItr))
	print (GroupedData)
