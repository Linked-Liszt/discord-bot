TOKEN_LOCATION = "../configs/bot.txt"

def get_token(token_fp=TOKEN_LOCATION: str) -> str:
    with open(token_fp, 'r') as token_f:
        token = token_f.read()
    return token