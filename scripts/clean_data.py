import data_utils as du
import pandas as pd
import numpy as np
import logging
import json
import re

OUTPUT_FP = '../data_clean/all_users_clean.json'

def clean_data() -> None:
    with open(du.CONFIG_FP, 'r') as config_f:
        config = json.load(config_f)

    full_data = combine_all_data(config)
    filtered_data = filter_all_messages(filter_global(full_data, config))
    filtered_data.to_csv(OUTPUT_FP)


def combine_all_data(config: dict) -> pd.DataFrame:
    full_data = None
    for data_fp in du.get_data_files(du.RAW_DATA_DIR, '.csv'):
        if any(ignore in data_fp for ignore in config['raw_ignore']):
            continue
        if full_data is None:
            full_data = pd.read_csv(data_fp)
        else:
            full_data = full_data.append(pd.read_csv(data_fp))
        logging.info(f"Read raw data: {data_fp}")
    return full_data.reset_index(drop=True)

def filter_global(full_data: pd.DataFrame, config: dict) -> pd.DataFrame:
    # Filter by approved users
    filtered_data = full_data[full_data['Author'].isin(config['users'])]

    # Remove contentless posts
    filtered_data = filtered_data[filtered_data['Content'].notnull()]

    # Remove bot commands
    filtered_data = filtered_data[~filtered_data['Content'].str.startswith('!')]
    filtered_data = filtered_data[~filtered_data['Content'].str.startswith('-play')]
    filtered_data = filtered_data[~filtered_data['Content'].str.startswith('-skip')]
    filtered_data = filtered_data[~filtered_data['Content'].str.startswith('/r')]
    filtered_data = filtered_data[~filtered_data['Content'].str.startswith('-search')]
    filtered_data = filtered_data[~filtered_data['Content'].str.startswith('-pause')]
    return filtered_data.reset_index(drop=True)


def filter_all_messages(full_data: pd.DataFrame) -> pd.DataFrame:
    for i, row in full_data.iterrows():
        filter_text = filter_message(row['Content'])
        if len(filter_text) == 0:
            filter_text = np.nan
        full_data.at[i, 'Content'] = filter_text
    full_data = full_data[full_data['Content'].notnull()]
    return full_data.reset_index(drop=True)


def filter_message(text: str) -> str:
    filter_text = re.sub(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', str(text), flags=re.MULTILINE)
    filter_text = re.sub(r'@\w+', '', str(filter_text), flags=re.MULTILINE)
    filter_text = filter_text.replace('@', '@/')
    return filter_text.strip()


if __name__ == '__main__':
    clean_data()