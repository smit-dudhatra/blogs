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

Enable the service to start on boot:

```bash
sudo systemctl enable nifty-straddle
```

Manually start the service:

```bash
sudo systemctl start nifty-straddle
```

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
| `sudo systemctl stop nifty-straddle` | Stop the service |
| `sudo systemctl status nifty-straddle` | Check service status |
| `sudo systemctl enable nifty-straddle` | Enable on boot |
| `sudo systemctl disable nifty-straddle` | Disable on boot |
| `sudo systemctl daemon-reload` | Reload systemd config |

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

## 🕐 Cron Schedule Summary (IST ↔ UTC)

| Time (IST) | Time (UTC) | Action | Days |
|---|---|---|---|
| 8:50 AM | 3:20 AM | Stop service | Every day |
| 8:55 AM | 3:25 AM | Start service | Mon & Tue only |
| 3:35 PM | 10:05 AM | Stop service | Every day |
| 12:00 AM (Sun) | 6:00 PM (Sat) | Clean journal logs | Weekly |
