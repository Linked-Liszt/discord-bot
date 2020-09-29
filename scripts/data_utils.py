TOKEN_LOCATION = "../configs/bot.txt"

def get_token(token_fp:str = TOKEN_LOCATION) -> str:
    with open(token_fp, 'r') as token_f:
        token = token_f.read().strip()
    return token