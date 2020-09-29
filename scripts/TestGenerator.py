import markovify as mk
import random
import string

RAW_EXPORT_PATHS =  [ 
    "REMOVED FOR GITHUB",
	"REMOVED FOR GITHUB"]
					
					
JsonImport = open(RAW_EXPORT_PATHS[0]).read()
Model=mk.Text.from_json(JsonImport)
#print(" ".join(Model.make_sentence() for i in range(5)))
for i in range(10):
	print(Model.make_sentence())