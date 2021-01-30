import argparse
import sqlite3
import hashlib
import PIL.Image
import repost_utils as ru
import urllib.request
import json
import pandas as pd
import dateutil.parser

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('channel_csv', help='CSV output of channel scrape')
    parser.add_argument('channel_db', help='Discord Channel ID')
    return parser.parse_args()

def populate_urls(chat_data: pd.DataFrame, db: sqlite3.Connection, ignore_users: list):
    for i, row in chat_data.iterrows():

        if row['Author'] in ignore_users:
           continue

        links = ru.extract_urls(str(row['Content']))
        link_date = dateutil.parser.parse(row['Date'])

        for link in links:
            link_data = ru.LinkData(
                link,
                int(link_date.timestamp()),
                row['Author']
            )

            ru.check_url_table(db, link_data)
        print(f'{i}/{len(chat_data)} urls')

def _download_file(url: str) -> (bool, bytes):
    is_valid = True
    data = None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})) as response:
            data = response.read()
    except Exception as e:
        print(f'URL error: {e}')
        is_valid = False

    return is_valid, data


def populate_files(chat_data: pd.DataFrame, db: sqlite3.Connection, ignore_users: list):
    num_errors = 0
    for i, row in chat_data.iterrows():
        if type(row['Attachments']) is str and row['Author'] not in ignore_users:
            is_valid, data = _download_file(row['Attachments'])
            if is_valid:
                is_img, f_len, f_hash = ru.calculate_hash(row['Attachments'], data)
                file_date = dateutil.parser.parse(row['Date'])

                hash_data = ru.HashData(f_hash,
                                        f_len,
                                        row['Attachments'],
                                        int(file_date.timestamp()),
                                        row['Author']
                )
                ru.check_hash_table(db, is_img, hash_data)
                print('File Hashed')
            else:
                num_errors += 1
        print(f'{i}/{len(chat_data)} files')
    print(f'Total Errors {num_errors}')


def main():
    args = parse_args()
    db = sqlite3.connect(args.channel_db)

    chat_data = pd.read_csv(args.channel_csv)

    with open('configs/discord_config.json', 'r') as f:
        disc_config = json.load(f)

    populate_urls(chat_data, db, disc_config['repost']['ignore_users'])
    populate_files(chat_data, db, disc_config['repost']['ignore_users'])

    db.close()


if __name__ == '__main__':
    main()