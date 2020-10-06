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

modules = [mm.Markov(MODEL_DIRS), rm.Rate()]

@client.event
async def on_message(message: discord.Message):
    #Ignore Bots
    if message.author.bot:
        return

    #Ignore DMs and other guilds
    if message.guild is False or message.guild.id not in config['guild_whitelist']:
        return

    if message.content.lower().strip() == "!info":
        await message.channel.send(respond_info())

    elif message.content.lower().startswith("!info-") and len(message.content.split('-')) > 1:
        await message.channel.send(respond_mod_info(message.content))

    elif message.content.lower().strip() == "!cmds":
        await message.channel.send(respond_cmds())

    elif message.content.lower().startswith("!cmds-") and len(message.content.split('-')) > 1:
        await message.channel.send(respond_mod_cmds(message.content))

    elif message.content.lower().strip() == "!modules":
        await message.channel.send(respond_modules())

    else:
        for module in modules:
            await module.handle_message(message)


def respond_modules():
    return "--Loaded Modules--\n" + ", ".join([module.abbrev for module in modules])


def respond_cmds() -> str:
    return ("--General Commands--\n"
            "!cmds: list general commands\n"
            "!cmds-[module]: get commands on module\n"
            "!info: info about the bot\n"
            "!info-[module]: get info on module\n"
            "!modules: list modules")


def respond_mod_cmds(text:str) -> str:
    text_mod = text.split('-')[1].strip().lower()
    for module in modules:
        if module.abbrev == text_mod:
            text = f"--{module.abbrev} commands--\n"
            text += "\n".join([f"{cmd}: {descr}" for cmd, descr in module.commands.items()])
            return text
    return "!cmds: Module not found. See !modules"


def respond_mod_info(text:str) -> str:
    text_mod = text.split('-')[1].strip().lower()
    for module in modules:
        if module.abbrev == text_mod:
            text = f"--{module.abbrev} info--\n"
            text += module.info
            return text
    return "!info: Module not found. See !modules"


def respond_info() -> str:
    return ("Discord bot written by Oxymoren#3640.\n"
            "Source code here: <https://github.com/Linked-Liszt/discord-bot>")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(du.get_token())