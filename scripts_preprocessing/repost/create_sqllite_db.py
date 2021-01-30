import sqlite3
import json
import os

DB_PREFIX = 'repost_dbs'

def create_db(fp: str):
    conn = sqlite3.connect(fp)

    sql_create_file_table = """ CREATE TABLE IF NOT EXISTS files (
                                hash blob PRIMARY KEY,
                                len integer NOT NULL,
                                link text,
                                original_date integer,
                                original_author text,
                                last_date integer,
                                last_author,
                                num_reposts integer
                                )
    """

    sql_create_ims_table = """ CREATE TABLE IF NOT EXISTS imgs (
                                hash blob PRIMARY KEY,
                                len integer NOT NULL,
                                link text,
                                original_date integer,
                                original_author text,
                                last_date integer,
                                last_author,
                                num_reposts integer
                                )
    """

    sql_create_links_table = """ CREATE TABLE IF NOT EXISTS links (
                                link text PRIMARY KEY,
                                original_date integer,
                                original_author text,
                                last_date integer,
                                last_author,
                                num_reposts integer
                                )
    """

    cur = conn.cursor()
    cur.execute(sql_create_file_table)
    cur.execute(sql_create_ims_table)
    cur.execute(sql_create_links_table)

    conn.commit()
    conn.close()


def create_folder():
    if not os.path.exists(DB_PREFIX):
        os.mkdir(DB_PREFIX)

def main():
    create_folder()

    with open('configs/discord_config.json', 'r') as config_f:
        config = json.load(config_f)

    for channel in config['repost']['channels']:
        db_path = os.path.join(DB_PREFIX, f'{channel}.db3')
        if not os.path.exists(db_path):
            create_db(db_path)


if __name__ == '__main__':
    main()
