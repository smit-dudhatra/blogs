# Screen Session Guide — Trading Bot

## 1. Start & Run the Trading Bot

```bash
screen -S trading
source /home/trading_scripts/venv/bin/activate
cd /home/trading_scripts
python <script_name>
```

## 2. Session Management Reference

| Command | Description |
|---|---|
| `screen -S trading` | Start named session |
| `screen -r trading` | Reattach to session |
| `screen -ls` | List sessions |
| `screen -S trading -X quit` | Close the screen session |
| `screen -X -S trading quit` | Close the screen session |
| `killall screen` | Kill all screen sessions |
| `pkill screen` | Kill all screen sessions |

## 3. Detaching

Press `Ctrl+A` then `d` to leave a session running in the background while returning to your main terminal.

## 4. Customization

For further customization, you can modify the `~/.screenrc` configuration file to set default behaviors, such as the scrollback buffer size or custom keybindings.

---

# Detaching When Console Output Is Scrolling Too Fast

**Problem:** Console output inside a `screen` session is printing too quickly, so the normal detach shortcut never gets a chance to register before more text floods in.

## Method 1: Remote Detach from a New Terminal (Recommended)

1. Open a new terminal window, or start a second SSH connection to the machine.
2. Find the active session's ID:
   ```bash
   screen -ls
   ```
3. Force the target session to detach remotely by passing its ID or name:
   ```bash
   screen -d <session_id>
   ```
   Example: `screen -d 12345.pts-0.server` 

## Method 2: Stop the Console Output Stream First

If you can't open a second terminal, pause the output stream so `screen` can actually read your shortcut keys :

1. Press `Ctrl + S` to temporarily freeze the terminal's output.
2. Immediately press `Ctrl + A`, release, then press `D` to detach.
3. **Note:** If you get stuck, or press `Ctrl + S` without detaching, press `Ctrl + Q` to unfreeze the output and try again. 

## Method 3: Use the Command Prompt Override

If the standard `Ctrl + A` then `D` shortcut fails, use Screen's internal command line instead :

1. Press `Ctrl + A` then `:` (colon) to bring up the Screen command bar at the bottom.
2. Type `detach` and press Enter.

---

Once safely detached, the process keeps running cleanly in the background. Reattach anytime with:

```bash
screen -r <session_id>
```
