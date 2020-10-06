source ../dsb_env/bin/activate
python discord_main.py &
jobs -l > pid.txt
disown