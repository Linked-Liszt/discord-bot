import markovify
import pandas as pd
import data_utils as du
import json
import re
import os

def create_all_models() -> None:
    """
    Extracts data from the cleaned file
    and creates all sets of models.
    """
    with open(du.CONFIG_FP, 'r', encoding='utf-8') as config_f:
        config = json.load(config_f)

    full_data = pd.read_csv(du.ALL_CLEAN_FP)
    user_data = split_by_user(full_data, config)
    user_data['everyone'] = full_data

    for user, user_data in user_data.items():
        create_model_set(user, user_data, config)

def create_model_set(user: str, user_data: pd.DataFrame, config: dict) -> None:
    """
    Creates a set of models based off a single user's data.
    """
    data_str = ""
    user_short = du.get_short_name(user, config)
    for _, row in user_data.iterrows():
        data_str += row['Content'] + ". "

    for k in range(config['model_params']['min'], config['model_params']['max'] + 1):
        model = markovify.Text(data_str, state_size=k, well_formed=False)
        model.compile(inplace=True)
        with open(os.path.join(du.MODELS_DIR, f"{user_short}_{k}.json"), 'w') as model_f:
            model_f.write(model.to_json())


def split_by_user(full_data: pd.DataFrame, config: dict) -> dict:
    """
    Splits the data by users. If duplicate users exist, handles them.
    """
    combined_groups = {}

    for author, group in full_data.groupby('Author'):
        found_combine = [author in combine for combine in config['dup_users']]
        if any(found_combine):
            base_author = config['dup_users'][found_combine.index(True)]
            if author in combined_groups:
                combined_groups[base_author[0]] = combined_groups[author].append(group)
            else:
                combined_groups[base_author[0]] = group
        else:
            combined_groups[author] = group
    return combined_groups

if __name__ == "__main__":
    create_all_models()