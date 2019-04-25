import pandas as pd
import numpy as np

RAW_DATA_PATHS = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]
	
RAW_EXPORT_PATHS = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]

ExpPathItr = iter(RAW_EXPORT_PATHS)
	
print("\n\n=================================\nMessage Count\n"
	 + "=================================\n\n")
for DataPath in RAW_DATA_PATHS:
	Name = DataPath[-9:-4]
	print("\n-----------------" + Name.upper() + "-----------------")
	
	RawChatDataFrame = pd.read_csv(DataPath)
	print("Number of Messages: " + str(len(RawChatDataFrame)))
	
	ChatByUser = RawChatDataFrame.groupby("Author").count()
	print(ChatByUser)
	ChatByUser.to_csv(next(ExpPathItr))
	
	ChatMessageMean = RawChatDataFrame.groupby("Author")["Content"].apply(lambda x: np.mean(x.str.len())).reset_index(name='mean_chat_message_length')
	print(ChatMessageMean)
	ChatMessageMean.to_csv(next(ExpPathItr))