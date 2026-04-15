make script of this command (.sh) and run at specific time with "at" command or manually with UTC time


screen -S trading
source /home/trading_scripts/venv/bin/activate
cd /home/trading_scripts
python energy_with_sl.py
screen -S <trading> -X quit >> to close the screen session

screen -S <trading>         # Start named session
screen -r <trading>               # Reattach to session
screen -ls               # List sessions
screen -S <trading> -X quit >> to close the screen session
killall screen
pkill screen

Detach from a session: Press Ctrl+A then d to leave a session running in the background while returning to your main terminal.
For further customization, you can modify the ~/.screenrc configuration file to set default behaviors, such as the scrollback buffer size or custom keybindings.

https://github.com/copilot/c/455d66a2-e400-40d1-8ffc-e9e3c58a5d0c

