import discord
import discord_module as dm
import textstat
import sqlite3
import aiohttp
import asyncio
import repost_utils as ru
import random
import datetime

REPOST_REPLIES = [
    ":ref: Repost Detected:",
    ":ref: Re:b:ost Detected!",
    ":ref: :b:ig :b:rother has observed a repost!",
    ":ref: To the repost gulag!",
    ":ref:",
    ":ref: The repost oracle demands repentance!",
    ":ref: State mandated repost callout:"
]

REPOST_IGNORE = [
    "repost",
    "classic"
]


class Repost(dm.DiscordModule):
    def __init__(self, config: dict):
        self.info = ("This module detects reposts in specified channels.")
        self.abbrev = 'repost'
        self.config = config
        self.commands = {}
        self.db_conns = {}

        self.db_lock = asyncio.Lock()

        for channel_id in config['repost']['channels']:
            self.db_conns[channel_id] = sqlite3.connect(f'repost_dbs/{channel_id}.db3')

        self.cur_tz = datetime.datetime.utcnow().astimezone().tzinfo

    async def handle_message(self, message: discord.Message):
        msg_author = f'{message.author.name}#{message.author.discriminator}'

        if (message.channel.id not in self.config['repost']['channels']
           or msg_author in self.config['repost']['ignore_users']):
            return

        reposts = []

        if message.attachments:
            is_valid, data = await self.download_file(message.attachments[0].url)
            if is_valid:
                is_img, f_len, f_hash = ru.calculate_hash(message.attachments[0].url, data)

                hash_data = ru.HashData(f_hash,
                                        f_len,
                                        message.attachments[0].url,
                                        datetime.datetime.now().timestamp(), #discord.py timestamps incorrect
                                        msg_author
                )
                async with self.db_lock:
                    is_original, repost = ru.check_hash_table(self.db_conns[message.channel.id], is_img, hash_data)
                if not is_original:
                    reposts.append(repost)


        urls = ru.extract_urls(message.content)
        for url in urls:
            link_data = ru.LinkData(url,
                                    datetime.datetime.now().timestamp(), #discord.py timestamps incorrect
                                    msg_author
            )
            async with self.db_lock:
                is_original, repost = ru.check_url_table(self.db_conns[message.channel.id], link_data)
            if not is_original:
                reposts.append(repost)


        ignores = [text in message.content.lower() for text in REPOST_IGNORE]
        if True in ignores:
            return

        if len(reposts) > 0:
            cur_repost = reposts[-1]

            msg = random.choice(REPOST_REPLIES)
            og_date = datetime.datetime.fromtimestamp(cur_repost.original_date).strftime('%Y-%m-%d %H:%M:%S')
            msg += f'\n Original Post By: `{cur_repost.original_author}` on `{og_date}`'

            if cur_repost.num_reposts > 0:
                last_date = datetime.datetime.fromtimestamp(cur_repost.last_date).strftime('%Y-%m-%d %H:%M:%S')
                add_s = ""
                if cur_repost.num_reposts > 1: add_s = "s"

                msg += f'\n Last Repost By: `{cur_repost.last_author}` on `{last_date}` ({cur_repost.num_reposts} repost{add_s} found)'

            await message.channel.send(msg)



    async def download_file(self, url: str):
        is_valid = True
        is_open = False
        data = None
        try:
            session = aiohttp.ClientSession()
            is_open = True
            async with session.get(url) as resp:
                data = await resp.read()
            await session.close()
        except Exception as e:
            print(f'Repost File Download Error: {e}')
            if is_open:
                await session.close()
            is_valid = False

        return is_valid, data