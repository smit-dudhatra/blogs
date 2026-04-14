make script of this command (.sh) and run at specific time with "at" command or manually with UTC time


screen -S trading
source /home/trading_scripts/venv/bin/activate
cd /home/trading_scripts
python energy_with_sl.py
screen -S <trading> -X quit >> to close the screen session

screen -S <trading>         # Start named session
screen -r <trading>               # Reattach to session
screen -ls               # List sessions
ctrl A , D                 # Detach from session
screen -S <trading> -X quit >> to close the screen session
