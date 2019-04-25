RAW_DATA_PATH = "REMOVED FOR GITHUB"

with open(RAW_DATA_PATH, 'r') as RawFile:
    FileText = RawFile.read()
	
EmojiDict = {}
for Word in FileText.split():
	if len(Word) > 1 and Word[0] == ':':
		if Word[1:].find(':') != -1:
			Word = Word[: Word[1:].find(':')+2]
			if Word in EmojiDict.keys():
				EmojiDict[Word] = EmojiDict[Word] + 1
			else:
				EmojiDict[Word] = 1

	
	
for Emoji in sorted(EmojiDict, key = EmojiDict.get, reverse=True):
	print("{0} {1}".format(Emoji, EmojiDict[Emoji]))