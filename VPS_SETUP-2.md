# Setting Up a Python Script on Hostinger VPS

A practical guide for developers who are comfortable with Linux but new to VPS and cron job setup.

---

## Cron Job Setup

To run your Python script automatically every 15 minutes, you need to add a cron job that triggers the systemd service.

The cron expression for **every 15 minutes, all day, every day** is:

```bash
*/15 * * * *
```

### Full cron entry example

```bash
*/15 * * * * root systemctl start nifty-straddle
```

---

## ❓ Questions & Answers

### ❓ What if I don't write `root` in the cron entry?

It depends on which cron file you are editing.

#### `/etc/crontab` or `/etc/cron.d/` files

The username field (e.g., `root`) is **required** in these files. If you omit it, cron will misinterpret `systemctl` as the username and `start` as the command — the cron job will **fail silently** with no error output.

```bash
# ✅ Correct
*/15  *  *  *  *   root   systemctl start nifty-straddle

# ❌ Broken — cron reads "systemctl" as the username
*/15  *  *  *  *          systemctl start nifty-straddle
```

#### `crontab -e` (user crontab)

No username field is used here. Cron runs the command as the user who owns the crontab:

```bash
*/15  *  *  *  *   systemctl start nifty-straddle
```

This syntax is valid, but `systemctl start` requires root privileges. It will fail with **permission denied** unless the user running it is root.

#### Summary

| File | Username field | Notes |
|---|---|---|
| `/etc/crontab` | Required | Use `root` |
| `/etc/cron.d/myfile` | Required | Use `root` |
| `sudo crontab -e` | Not used | Runs as root automatically |
| `crontab -e` (non-root) | Not used | Cannot run `systemctl` |

> 💡 **Easiest approach:** Use `sudo crontab -e` — no username field is needed and it has full root access.

---

*More sections will be added as the setup guide grows.*
