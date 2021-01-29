import argparse
import sqlite3
import hashlib
import PIL.Image
import repost_utils as ru
import pandas as pd
import dateutil.parser

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('channel_csv', help='CSV output of channel scrape')
    parser.add_argument('channel_db', help='Discord Channel ID')
    return parser.parse_args()

def populate_urls(chat_data: pd.DataFrame, db: sqlite3.Connection):
    for _, row in chat_data.iterrows():
        links = ru.extract_urls(str(row['Content']))
        link_date = dateutil.parser.parse(row['Date'])

        for link in links:
            link_data = ru.LinkData(
                link[0],
                int(link_date.timestamp()),
                row['Author']
            )

            print(link_data)
            input()

            ru.check_url_table(db, link_data)

def main():
    args = parse_args()
    db = sqlite3.connect(args.channel_db)

    chat_data = pd.read_csv(args.channel_csv)

    populate_urls(chat_data, db)

    print('gothere')

    db.close()


if __name__ == '__main__':
    main()