import hashlib
import sqlite3
import PIL.Image
import sys
import re

def get_file_hash(fp: str) -> str:
    with open(fp, 'rb') as f:
        f_bytes = f.read()
        return len(f_bytes), hashlib.sha256(f_bytes).digest()

def get_img_hash(fp: str) -> str:
    f_bytes = PIL.Image.open(fp).tobytes()
    return len(f_bytes), hashlib.sha256(f_bytes.digest())

def extract_urls(msg: str) -> list:
    regex = r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'
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

def check_files_table(conn: sqlite3.Connection, fp: str):
    f_len, f_hash = get_file_hash(fp)

    sql_query = """SELECT * FROM files WHERE
                   hash=? AND len=?
    """
    cur = conn.cursor()
    cur.execute(sql_query, (f_hash, f_len))

    return not (not cur.fetchall()) # Check is empty