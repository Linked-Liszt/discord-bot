import markovify as mk

RAW_IMPORT_PATHS = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]

RAW_EXPORT_PATHS = [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]

ExportPathItr = iter(RAW_EXPORT_PATHS)


for FilePath in RAW_IMPORT_PATHS:
	InputFile = open(FilePath, encoding='utf8').read()
	OutputFile = open(next(ExportPathItr), "w")
	Model = mk.Text(InputFile, state_size=3)
	OutputFile.write(Model.to_json())
	OutputFile.close()