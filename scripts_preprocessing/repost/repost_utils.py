import hashlib
import sqlite3
import PIL.Image
import sys
import re
from typing import NamedTuple

IM_TABLE = 'imgs'
FILE_TABLE = 'files'
URL_TABLE = 'links'

IM_TYPES = [
    '.png',
    '.jpg',
    '.jpeg'
]

"""
================
Communication Structures
================
"""

class LinkData(NamedTuple):
    link: str
    date: int
    author: str

class HashData(NamedTuple):
    f_hash: bytes
    length: int
    date: int
    author: str

class RepostData(NamedTuple):
    repost_type: str
    original_date: str
    original_author: str
    last_date: str
    last_author: str
    num_reposts: int


"""
================
HASH FUNCTIONS
================
"""


def _get_file_hash(fp: str) -> str:
    with open(fp, 'rb') as f:
        f_bytes = f.read()
        return len(f_bytes), hashlib.sha256(f_bytes).digest()

def _get_img_hash(fp: str) -> str:
    f_bytes = PIL.Image.open(fp).tobytes()
    return len(f_bytes), hashlib.sha256(f_bytes.digest())

def calculate_hash(fp: str) -> (bool, int, str):
    is_image = True
    try:
        valid_ims = [fp.endswith(im_end) for im_end in IM_TYPES]
        if  True not in valid_ims: raise ValueError('Not an Image')

        f_len, f_hash = _get_img_hash(fp)
    except:
        is_image = False
        f_len, f_hash = _get_file_hash(fp)

    return is_image, f_len, f_hash


def _insert_hash(conn: sqlite3.Connection, table: str, hash_data: HashData) -> None:
    insert_sql = f""" INSERT INTO {table}(hash,
                                          len
                                          original_date,
                                          original_author,
                                          last_date,
                                          last_author,
                                          num_reposts)
                    VALUES(?, ?, ?, ?, ?, ?, ?)
    """
    cur = conn.cursor()
    cur.execute(insert_sql, (hash_data.f_hash,
                             hash_data.length,
                             hash_data.date,
                             hash_data.author,
                             hash_data.date,
                             hash_data.author,
                             0))
    conn.commit()


def _update_hash(conn: sqlite3.Connection, table: str, hash_data: HashData, num_reposts: int) -> None:
    cur_reposts = num_reposts + 1
    insert_sql = f""" UPDATE {table}
                     SET last_date=?, last_author=?, num_reposts=?
                     WHERE hash=? AND len=?
    """
    cur = conn.cursor()
    cur.execute(insert_sql, (hash_data.date, hash_data.author, cur_reposts, hash_data.f_hash, hash_data.length))
    conn.commit()

def check_hash_table(conn: sqlite3.Connection, table: str, hash_data: HashData):
    sql_query = f"""SELECT
                      original_date,
                      original_author,
                      last_date,
                      last_author,
                      num_reposts
                   FROM {table} WHERE
                   hash=? AND len=?
    """
    cur = conn.cursor()
    cur.execute(sql_query, (hash_data.f_hash, hash_data.length))

    hits = cur.fetchall()

    is_original = len(hits) == 0

    if is_original:
        _insert_hash(conn, table, hash_data)
        repost = RepostData()

    else:
        _update_hash(conn, table, hash_data, hits[0][4])
        repost = RepostData(table,
                            hits[0][0],
                            hits[0][1],
                            hits[0][2],
                            hits[0][3],
                            hits[0][4] + 1)

    return is_original, repost


"""
================
URL FUNCTIONS
================
"""
def extract_urls(msg: str) -> list:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    return re.findall(regex, msg, flags=re.MULTILINE)


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

    is_original = len(hits) == 0

    if is_original:
        _insert_url(conn, link_data)
        repost = RepostData()

    else:
        _update_url(conn, link_data, hits[0][4])
        repost = RepostData(URL_TABLE,
                            hits[0][0],
                            hits[0][1],
                            hits[0][2],
                            hits[0][3],
                            hits[0][4] + 1)

    return is_original, repost