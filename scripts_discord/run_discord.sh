source ../dsb_env/bin/activate
python scripts_discord/discord_main.py &
jobs -l > pid.txt
disown