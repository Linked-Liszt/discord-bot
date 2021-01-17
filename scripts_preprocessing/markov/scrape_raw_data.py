import json
import data_utils as du
import os

EXPORTER_LOCATION = "..\\preprocessing_data\\export_cli\\DiscordChatExporter.Cli.exe"
"""
JSON Structure:
[
    "channel id 1",
    "channel id 2"
]
"""

def export_guilds() -> None:
    """
    Calls the discord exporting tool to scrape the raw data from a set of
    discord guilds. Uses a bot token defined in the token file.
    """
    token = du.get_token()
    with open(du.CONFIG_FP, 'r') as config_f:
        guilds = json.load(config_f)['guild']
    for guild in guilds:
        os.system(f"{EXPORTER_LOCATION} exportguild -t {token} -b -g {guild} -o ../data_raw -f csv")

if __name__ == "__main__":
    export_guilds()