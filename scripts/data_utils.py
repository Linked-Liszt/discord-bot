import os
import typing

CONFIG_FP = '../configs/preprocessing_config.json'
TOKEN_LOCATION = "../configs/bot.txt"
RAW_DATA_DIR = "../data_raw"

def get_token(token_fp: str = TOKEN_LOCATION) -> str:
    with open(token_fp, 'r') as token_f:
        token = token_f.read().strip()
    return token

def get_data_files(files_dir: str, end: str, contains: str = None) -> typing.Generator[str, None, None]:
    for fp in os.listdir(files_dir):
        if fp.endswith(end):
            if contains is None or contains in fp:
                yield os.path.join(files_dir, fp)
