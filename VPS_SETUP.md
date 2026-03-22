# 🖥️ Hostinger VPS Setup — Nifty50 Straddle Bot

> Ubuntu 24.04 LTS · Python 3.14 · systemd + cron

---

## 📋 Table of Contents

1. [Update System](#1-update-system)
2. [Install Prerequisites](#2-install-prerequisites)
3. [Add Deadsnakes PPA](#3-add-deadsnakes-ppa)
4. [Install Python 3.14](#4-install-python-314)
5. [Verify Python Installation](#5-verify-python-installation)
6. [Install pip for Python 3.14](#6-install-pip-for-python-314)
7. [Setup Project Directory](#7-setup-project-directory)
8. [Setup systemd Service](#8-setup-systemd-service)
9. [Journal Log Management](#9-journal-log-management)
10. [Setup Cron Jobs](#10-setup-cron-jobs)
11. [Useful Commands](#11-useful-commands)
12. [Concepts & Reference](#12-concepts--reference)

---

## 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 2. Install Prerequisites

```bash
sudo apt install -y software-properties-common
```

---

## 3. Add Deadsnakes PPA

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

Then update the package list:

```bash
sudo apt update
```

---

## 4. Install Python 3.14

```bash
sudo apt install -y python3.14 python3.14-venv
```

---

## 5. Verify Python Installation

```bash
python3.14 --version
```

---

## 6. Install pip for Python 3.14

```bash
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.14
```

Verify pip:

```bash
python3.14 -m pip --version
```

---

## 7. Setup Project Directory

Create the working directory and place your script:

```bash
mkdir -p /home/my-scripts/nifty-straddle
```

Copy or upload `nifty50_straddle.py` to:

```
/home/my-scripts/nifty-straddle/nifty50_straddle.py
```

---

## 8. Setup systemd Service

### 8a. Create the service file

```bash
sudo nano /etc/systemd/system/nifty-straddle.service
```

Paste the following content:

```ini
[Unit]
Description=Nifty50 Straddle Trading Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/my-scripts/nifty-straddle
ExecStart=/usr/bin/python3.14 nifty50_straddle.py
Restart=no
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

> **Why `Restart=no`?**
> The service will NOT auto-restart if the script exits. This is intentional — if a major exception occurs (e.g., insufficient funds, broker API error), the script calls `exit(0)` and the service stops cleanly. This prevents uncontrolled retries or hammering the broker server.

### 8b. Reload systemd and enable the service

After creating or editing the service file, reload the systemd daemon so it picks up the changes:

```bash
sudo systemctl daemon-reload
```

> `daemon-reload` instructs systemd to rescan all unit files, rebuild the dependency tree, and rerun generators — without restarting the entire system.

### 8c. Disable boot auto-start (important — we use cron instead)

Since cron controls when the service starts (Mon & Tue at 8:55 AM IST), you do **not** want systemd to auto-start it on every VPS reboot:

```bash
sudo systemctl disable nifty-straddle
```

After disabling, verify:

```bash
systemctl list-unit-files | grep nifty-straddle
```

Expected output:
```
nifty-straddle.service    disabled    enabled
```

This is correct. `disabled` = won't auto-start on boot. Your cron job still starts it on schedule.

### 8d. Manually start the service

```bash
sudo systemctl start nifty-straddle
```

### 8e. Check actual running status

```bash
systemctl status nifty-straddle
```

| Output | Meaning |
|---|---|
| `Active: active (running)` | Script is running right now |
| `Active: inactive (dead)` | Script is stopped ✓ |

### 8f. Stop the service

To stop the service at any time — including mid-session if you need to halt the script abruptly:

```bash
sudo systemctl stop nifty-straddle
```

> systemd sends `SIGTERM` to the Python process, which kills it immediately. Use this anytime you want to stop the bot mid-run — e.g., at 11:30 AM before market close.

View live logs:

```bash
sudo journalctl -u nifty-straddle -f
```

---

## 9. Journal Log Management

### Why this matters

Your script prints heavily — live ticker data, order logs, minute-by-minute checks. `journalctl` stores **all of it**. Without any size limit, it grows unboundedly and can fill your VPS disk over weeks.

### 9a. Check current journal disk usage

Run this anytime to see how much disk space your logs are consuming:

```bash
journalctl --disk-usage
```

Example output:
```
Archived and active journals take up 16.0M in the file system.
```

**What this means:**
| Term | Description |
|---|---|
| **Active journals** | Logs from currently running services (being written right now) |
| **Archived journals** | Old rotated log files from previous service runs |
| **16 MB total** | Completely fine — a typical VPS has 20–40 GB disk |

You only need to act if it grows to several hundred MB or more. The one-time cap below handles that automatically.

### 9b. Set a permanent 100 MB size cap (run once, not in cron)

This tells `journald` to auto-delete the oldest log entries whenever total usage exceeds 100 MB — set it once and never think about it again:

```bash
sudo mkdir -p /etc/systemd/journald.conf.d/
```

```bash
echo -e "[Journal]\nSystemMaxUse=100M" | sudo tee /etc/systemd/journald.conf.d/size.conf
```

```bash
sudo systemctl restart systemd-journald
```

### 9c. Verify the config was applied

```bash
cat /etc/systemd/journald.conf.d/size.conf
```

Expected output:
```
[Journal]
SystemMaxUse=100M
```

> **Why does `journalctl --disk-usage` still show 16 MB after setting the cap?**
> That is completely normal. The 100 MB cap does **not** shrink existing logs — it only **prevents future growth** beyond 100 MB. Since 16 MB is already well under the limit, journald has nothing to delete. The cap kicks in automatically in the future when logs accumulate and approach 100 MB, at which point it will start auto-deleting the oldest entries to stay under the limit.

---

## 10. Setup Cron Jobs

### 10a. Verify VPS timezone

The Hostinger VPS uses **UTC** by default. All cron times below are in **UTC**.

> IST = UTC + 5:30

```bash
timedatectl
```

### 10b. Open crontab editor

```bash
crontab -e
```

### 10c. Add the following cron jobs

```cron
# Weekly journal cleanup (every Sunday at 12:00 AM IST / 6:00 PM UTC Saturday)
0 18 * * 0 journalctl --vacuum-time=7d

# Stop trading service at 8:50 AM IST (3:20 AM UTC) — runs every day
20 3 * * * systemctl stop nifty-straddle

# Start trading service at 8:55 AM IST (3:25 AM UTC) — runs Mon & Tue only
25 3 * * 1,2 systemctl start nifty-straddle

# Stop trading service at 3:35 PM IST (10:05 AM UTC) — runs every day
5 10 * * * systemctl stop nifty-straddle
```

### 10d. Crontab reference

| Command | Description |
|---|---|
| `crontab -e` | Edit cron jobs |
| `crontab -l` | List all cron jobs |
| `crontab -r` | Remove all cron jobs |

---

## 11. Useful Commands

### Service management

| Command | Description |
|---|---|
| `sudo systemctl start nifty-straddle` | Start the service |
| `sudo systemctl stop nifty-straddle` | Stop the service (kills process immediately via SIGTERM) |
| `sudo systemctl status nifty-straddle` | Check if running or stopped |
| `sudo systemctl enable nifty-straddle` | Mark to auto-start on boot |
| `sudo systemctl disable nifty-straddle` | Remove auto-start on boot |
| `sudo systemctl daemon-reload` | Reload systemd config after editing service file |

### Logs

| Command | Description |
|---|---|
| `sudo journalctl -u nifty-straddle -f` | Live logs |
| `sudo journalctl -u nifty-straddle --since today` | Today's logs |
| `sudo journalctl -u nifty-straddle -n 100` | Last 100 log lines |
| `journalctl --disk-usage` | Check total journal disk usage |

### List all systemd services

```bash
systemctl list-unit-files --type=service
```

---

## 12. Concepts & Reference

### stop vs enable — they are independent

A very common point of confusion:

```bash
sudo systemctl stop nifty-straddle
# service still shows: enabled
```

`stop` and `enable/disable` control **completely different things** and do not affect each other:

| Command | What it controls |
|---|---|
| `systemctl stop` | Kills the running process **right now** |
| `systemctl start` | Starts the process **right now** |
| `systemctl enable` | Marks it to **auto-start on every boot** |
| `systemctl disable` | Removes the **auto-start on boot** mark |

So `enabled` just means it will start when the VPS reboots — it says **nothing** about whether the process is running right now. Always use `systemctl status` to check the actual running state.

---

### Understanding `systemctl list-unit-files` columns

When you run:

```bash
systemctl list-unit-files | grep nifty-straddle
```

You see two columns:

```
nifty-straddle.service    disabled    enabled
                          ^STATE      ^PRESET
```

**STATE** — what it's currently configured to do on boot:

| State | Meaning |
|---|---|
| `enabled` | Will auto-start on boot |
| `disabled` | Will NOT auto-start on boot |
| `static` | Can't be enabled/disabled, used by other units |
| `masked` | Completely blocked, can't be started at all |

**PRESET** — the distribution's default/recommended state for this service:

| Preset | Meaning |
|---|---|
| `enabled` | Ubuntu recommends this should be enabled by default |
| `disabled` | Ubuntu recommends this should be disabled by default |

> The PRESET column shows `enabled` because the `.service` file has `WantedBy=multi-user.target`, which is the standard Ubuntu default. It doesn't change unless you explicitly run `systemctl preset`. It's just a recommendation — your actual STATE (`disabled`) is what matters.

---

### Stopping the script abruptly mid-session

If the script is running (e.g., cron started it at 8:55 AM) and you need to stop it immediately at any point:

```bash
sudo systemctl stop nifty-straddle
```

systemd sends `SIGTERM` to the Python process, which kills it immediately. Confirm it stopped:

```bash
systemctl status nifty-straddle
# Expected: Active: inactive (dead)
```

---

## 🕐 Cron Schedule Summary (IST ↔ UTC)

| Time (IST) | Time (UTC) | Action | Days |
|---|---|---|---|
| 8:50 AM | 3:20 AM | Stop service | Every day |
| 8:55 AM | 3:25 AM | Start service | Mon & Tue only |
| 3:35 PM | 10:05 AM | Stop service | Every day |
| 12:00 AM (Sun) | 6:00 PM (Sat) | Clean journal logs | Weekly |
