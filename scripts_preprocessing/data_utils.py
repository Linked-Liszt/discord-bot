import os
import typing

CONFIG_FP = '../configs/preprocessing_config.json'
TOKEN_LOCATION = "../configs/bot.txt"
RAW_DATA_DIR = "../preprocessing_data/data_raw"
ALL_CLEAN_FP = '../preprocessing_data/data_clean/all_users_clean.csv'
MODELS_DIR = '../markov_models'

def get_token(token_fp: str = TOKEN_LOCATION) -> str:
    """
    Gets the stored bot token.
    """
    with open(token_fp, 'r') as token_f:
        token = token_f.read().strip()
    return token

def get_data_files(files_dir: str, end: str, contains: str = None) -> typing.Generator[str, None, None]:
    """
    Yields data files that meet certian conditions defined by the parameters.
    """
    for fp in os.listdir(files_dir):
        if fp.endswith(end):
            if contains is None or contains in fp:
                yield os.path.join(files_dir, fp)


def get_short_name(author: str, config: dict) -> str:
    if author in config['user_shortcuts']:
        return config['user_shortcuts'][author]
    return author.lower().split('#')[0]
