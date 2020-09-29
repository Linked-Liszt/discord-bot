import json
import data_utils as du
import os

CONFIG_LOCATION = "../configs/scrape_config.json"
EXPORTER_LOCATION = "..\\export_cli\\DiscordChatExporter.Cli.exe"
"""
JSON Structure:
[
    "channel id 1",
    "channel id 2"
]
"""

def export_guilds() -> None:
    token = du.get_token()
    with open(CONFIG_LOCATION, 'r') as config_f:
        guilds = json.load(config_f)
    for guild in guilds:
        os.system(f"{EXPORTER_LOCATION} exportguild -t {token} -b -g {guild} -o ../data_raw -f csv")

if __name__ == "__main__":
    export_guilds()