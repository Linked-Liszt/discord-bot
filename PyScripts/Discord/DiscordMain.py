import discord
import random
import markovify as mk

client = discord.Client()



ELO_PATH = "REMOVED FOR GITHUB"
ELO_NAMES = [["REMOVED FOR GITHUB", "REMOVED FOR GITHUB"],
			["REMOVED FOR GITHUB", "REMOVED FOR GITHUB"]]
				



				
MODEL_PATHS = {"REMOVED FOR GITHUB",
				"REMOVED FOR GITHUB"}
					
					
					

def GenerateMarkov(Name):
	OutputMessage = ""
	SentenceCount = 0
	JsonImport = open(MODEL_PATHS[Name]).read()
	Model=mk.Text.from_json(JsonImport)
	while OutputMessage == "" or SentenceCount < 5:
		GeneratedMessage = Model.make_sentence()
		if GeneratedMessage != None:
			OutputMessage = OutputMessage + ' ' + GeneratedMessage
		SentenceCount += 1
	return OutputMessage



def RNGLeague(Sender, Reciever, Dice):
	for EloIndex in range(len(ELO_NAMES)):
		if Sender == ELO_NAMES[EloIndex][1]:
			SenderIndex = EloIndex
		if Reciever == ELO_NAMES[EloIndex][0]:
			RecieverIndex = EloIndex
	if SenderIndex==RecieverIndex:
		return "You can't challenge yourself!"
	EloFile = open(ELO_PATH, "r+")
	EloList = EloFile.readlines()
	
	EloSender = int(EloList[SenderIndex])
	EloReciever = int(EloList[RecieverIndex])
	ExpSender = 1 / (1 + 10 ** ((EloReciever - EloSender) / 400))
	ExpReciever = 1 / (1 + 10 ** ((EloSender - EloReciever) / 400))
	
	SenderRoll = random.randint(0, Dice)
	RecieverRoll = random.randint(0, Dice)
	
	if SenderRoll < RecieverRoll:
		EloSender = int(round(EloSender + 128 * (0 - ExpSender)))
		EloReciever = int(round(EloReciever + 128 * (1 - ExpSender)))
		Winner=ELO_NAMES[RecieverIndex][0]
	elif SenderRoll > RecieverRoll:
		EloSender = int(round(EloSender + 128 * (1 - ExpSender)))
		EloReciever = int(round(EloReciever + 128 * (0 - ExpSender)))
		Winner=ELO_NAMES[SenderIndex][0]
	
	else: 
		Winner="nobody"
		
	EloList[SenderIndex] = str(EloSender) + "\n"
	EloList[RecieverIndex] = str(EloReciever) + "\n"
	
	EloFile.seek(0)
	EloFile.writelines(EloList)
	EloFile.truncate()
	EloFile.close()
	return "{0}: {1}, {2}: {3} |  {4} wins! | {5} elo: {6}, {7} elo: {8}".format(ELO_NAMES[SenderIndex][0], str(SenderRoll), ELO_NAMES[RecieverIndex][0], str(RecieverRoll), Winner, ELO_NAMES[SenderIndex][0], str(EloSender), ELO_NAMES[RecieverIndex][0], str(EloReciever))
		
def RNGLeagueList():
	EloFile = open(ELO_PATH)
	EloList = EloFile.readlines()
	EloFile.close()
	msg = "-\n"
	for EloI in range(len(EloList)):
		msg = msg + ELO_NAMES[EloI][0] + ": " + EloList[EloI]
	return msg

@client.event
async def on_message(message):
	if message.author.bot:
		return #Ignore Bots
	
	elif message.content.lower().startswith("!help"):
		msg = "Current Commands:\n!Simulate: Simulates a a _REMOVED_\n!List: Lists the _REMOVED_ keywords for !Simulate\n!RNGLeague: Challenge someone to a bout of RNG\nRNGLeagueList: Display RNGLeague Elos"
		await client.send_message(message.channel, msg)
		return
			
	elif message.content.lower().startswith("!list"):
		msg="REMOVED FOR GITHUB"
		await client.send_message(message.channel, msg)
		return
		
	elif message.content.lower().startswith("!simulate"):
		Name = message.content.split()[0:50][1]
		if Name.lower() in MODEL_PATHS.keys():
			msg = GenerateMarkov(Name.lower())
			await client.send_message(message.channel, msg)
			return
		else:
			msg = "Sorry I don't recognize that person (see !list)"
			await client.send_message(message.channel, msg)
			return
		
	elif message.content.lower().startswith("i'm"):
		if random.randint(0,100)==50:
			msg = "Hi {0}, I'm Dad... wait what?".format(message.content[4:])
			await client.send_message(message.channel, msg)
			return
	
	elif message.content.lower().startswith("!rngleaguelist"):
		msg = RNGLeagueList()
		await client.send_message(message.channel, msg)
		
	elif message.content.lower().startswith("!rngleague"):
		SplitMessage = message.content.split()[0:50]
		if len(SplitMessage) >= 2 and SplitMessage[1].lower() in MODEL_PATHS.keys() and SplitMessage[1].lower() != "ubergoon":
			try:
				if len(SplitMessage) == 2:
					dice = 1000
				else:
					dice = int(SplitMessage[2])
				if dice <= 10000 and dice >= 10:
					msg = RNGLeague(message.author.name, SplitMessage[1].lower(), dice)
				else:
					msg = "Dice number is not betweeen 10 and 10000"
			except ValueError:
				msg = "Unable to interpret dice number"
		
		else:
			msg = "Invalid Challenge. Use !RNGLeague [usr] [Dice 10-10000]" 
		await client.send_message(message.channel, msg)
		return
	
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

	
	
	
	
	
TOKEN = 'REMOVED FOR GITHUB'
client.run(TOKEN)