import hashlib
import sqlite3
import PIL.Image
import sys
import re
from typing import NamedTuple

class LinkData(NamedTuple):
    link: str
    date: int
    author: str

class RepostData(NamedTuple):
    repost_type: str
    original_date: str
    original_author: str
    last_date: str
    last_author: str
    num_reposts: int


def get_file_hash(fp: str) -> str:
    with open(fp, 'rb') as f:
        f_bytes = f.read()
        return len(f_bytes), hashlib.sha256(f_bytes).digest()

def get_img_hash(fp: str) -> str:
    f_bytes = PIL.Image.open(fp).tobytes()
    return len(f_bytes), hashlib.sha256(f_bytes.digest())

def extract_urls(msg: str) -> list:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    return re.findall(regex, msg, flags=re.MULTILINE)

def insert_file(conn: sqlite3.Connection, fp: str) -> None:
    f_len, f_hash = get_file_hash(fp)

    if not check_files_table(conn, fp):
        insert_sql = """ INSERT INTO files(hash, len)
                        VALUES(?, ?)
        """
        cur = conn.cursor()
        cur.execute(insert_sql, (f_hash, f_len))
        conn.commit()


def _insert_url(conn: sqlite3.Connection, link_data: LinkData) -> None:
    insert_sql = """ INSERT INTO links(link,
                                       original_date,
                                       original_author,
                                       last_date,
                                       last_author,
                                       num_reposts)
                    VALUES(?, ?, ?, ?, ?, ?)
    """
    cur = conn.cursor()
    cur.execute(insert_sql, (link_data.link,
                             link_data.date,
                             link_data.author,
                             link_data.date,
                             link_data.author,
                             0))
    conn.commit()


def _update_url(conn: sqlite3.Connection, link_data: LinkData, num_reposts: int) -> None:
    cur_reposts = num_reposts + 1
    insert_sql = """ UPDATE links
                     SET last_date=?, last_author=?, num_reposts=?
                     WHERE link=?
    """
    cur = conn.cursor()
    cur.execute(insert_sql, (link_data.date, link_data.author, cur_reposts, link_data.link))
    conn.commit()


def check_url_table(conn: sqlite3.Connection, link_data: LinkData):
    sql_query = """SELECT
                      original_date,
                      original_author,
                      last_date,
                      last_author,
                      num_reposts
                   FROM links WHERE
                   link=?
    """
    cur = conn.cursor()
    cur.execute(sql_query, (link_data.link,))

    hits = cur.fetchall()

    print(hits)
    input()
    is_original = len(hits) == 0

    if is_original:
        _insert_url(conn, link_data)
        repost = RepostData()

    else:
        _update_url(conn, link_data, hits[0][4])
        repost = RepostData(link_data.link,
                            'url',
                            hits[0][0],
                            hits[0][1],
                            hits[0][2],
                            hits[0][3],
                            hits[0][4] + 1)

    return is_original, repost

def check_files_table(conn: sqlite3.Connection, fp: str):
    f_len, f_hash = get_file_hash(fp)

    sql_query = """SELECT * FROM files WHERE
                   hash=? AND len=?
    """
    cur = conn.cursor()
    cur.execute(sql_query, (f_hash, f_len))

    return not (not cur.fetchall()) # Check is empty