import discord
import random
import markovify as mk
import markov_module as mm
import json
import discord_utils as du
import rate_module as rm

MODEL_DIRS = '../markov_models'

client = discord.Client()
with open('../configs/discord_config.json') as config_f:
    config = json.load(config_f)

modules = [mm.Markov(), rm.Rate()]

@client.event
async def on_message(message: discord.Message):
    #Ignore Bots
    if message.author.bot:
        return

    #Ignore DMs and other guilds
    if message.guild is False or message.guild not in config['guild_whitelist']:
        return

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