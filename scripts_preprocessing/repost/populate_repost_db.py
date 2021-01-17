import argparse
import sqlite3
import hashlib
import PIL.Image
import repost_utils as ru
import pandas

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('channel_csv', help='CSV output of channel scrape')
    parser.add_argument('channel_id', help='Discord Channel ID')
    return parser.parse_args()


def main():
    args = parse_args()

    chat_data = pandas.read_csv(args.channel_csv)

    print('gothere')
    for _, row in chat_data.iterrows():
        links = ru.extract_urls(str(row['Content']))
        if len(links) > 1:
            pass




if __name__ == '__main__':
    main()