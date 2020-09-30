import discord
import random
import markovify as mk
import model_manager as mm
import data_utils as du

MODEL_DIRS = '../markov_models'

client = discord.Client()
model_mgr = mm.ModelManager(MODEL_DIRS)

@client.event
async def on_message(message: discord.Message):
    #Ignore Bots
    if message.author.bot:
        return

    #Ignore DMs
    if message.guild is False:
        return

    if message.content.lower().startswith("!list"):
        await message.channel.send(model_mgr.list_models())

    elif (message.content.lower().startswith("!sim ")
        or message.content.lower().startswith("!sim#")):
        await message.channel.send(model_mgr.serve_model(message.content.lower()))

    elif message.content.lower().startswith("!help"):
        msg = ("Current Commands:\n"
               + "!sim [name]: Simulate a goon with a standard tri-gram model\n"
               + "!sim#[n] [name]: Simulate a goon with a [n]-gram model\n"
               + "!list: List avaliable models and n\n"
               + "!info: Info about n-gram markov models\n"
               + "!help: List commands"
        )
        await message.channel.send(msg)

    elif message.content.lower().startswith("!info"):
        await message.channel.send(model_mgr.info())


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(du.get_token())