import pandas as pd
import numpy as np
import re as re

RAW_DATA_PATHS = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]
	
RAW_EXPORT_PATHS = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]

EVERYONE_EXPORT_PATH ="REMOVED FOR GITHUB"
					
ExportPathItr = iter(RAW_EXPORT_PATHS)
for RawDataPath in RAW_DATA_PATHS:
	TextDF = pd.read_csv(RawDataPath)
	OutputFile = open(next(ExportPathItr), "wb")
	for index, Message in TextDF.iterrows():
		FilteredMessage = re.sub(r'^https?:\/\/.*[\r\n]*', '', str(Message["Content"]), flags=re.MULTILINE)
		FilteredMessage = re.sub(r'@\w+', '', str(FilteredMessage), flags=re.MULTILINE)
		FilteredMessage+=". "
		if FilteredMessage[0:3] == "/r " or FilteredMessage=="nan. ":
			continue
		
		FilteredMessage = FilteredMessage.encode('utf8', 'ignore')
		OutputFile.write(FilteredMessage)
	OutputFile.close() 

OutputFile = open(EVERYONE_EXPORT_PATH, "wb")	
for RawDataPath in RAW_DATA_PATHS:
	TextDF = pd.read_csv(RawDataPath)
	for index, Message in TextDF.iterrows():
		FilteredMessage = re.sub(r'^https?:\/\/.*[\r\n]*', '', str(Message["Content"]), flags=re.MULTILINE)
		FilteredMessage = re.sub(r'@\w+', '', str(FilteredMessage), flags=re.MULTILINE)
		FilteredMessage+=". "
		if FilteredMessage[0:3] == "/r " or FilteredMessage=="nan. ":
			continue
		
		FilteredMessage = FilteredMessage.encode('utf8', 'ignore')
		OutputFile.write(FilteredMessage)
OutputFile.close()