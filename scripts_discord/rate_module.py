import discord
import discord_module as dm

class Rate(dm.DiscordModule):
    def __init__(self):
        self.info = ""
        self.commands = {
            "rate": ""
        }

    def handle_message(self, message: discord.Message):
        pass