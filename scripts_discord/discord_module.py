import discord

class DiscordModule():
    """
    Base discord module class. This can organize various discord
    functions.

    Required Vars:
        -info (str): Long form info of commands.
        -commands: (dict): keys: commands values: short description
            of command
    """
    async def handle_message(self, message: discord.Message) -> None:
        raise NotImplementedError()
