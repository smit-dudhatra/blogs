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
9. [Setup Cron Jobs](#9-setup-cron-jobs)
10. [Useful Commands](#10-useful-commands)

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

## 9. Setup Cron Jobs

### 9a. Verify VPS timezone

The Hostinger VPS uses **UTC** by default. All cron times below are in **UTC**.

> IST = UTC + 5:30

```bash
timedatectl
```

### 9b. Open crontab editor

```bash
crontab -e
```

### 9c. Add the following cron jobs

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

### 9d. Crontab reference

| Command | Description |
|---|---|
| `crontab -e` | Edit cron jobs |
| `crontab -l` | List all cron jobs |
| `crontab -r` | Remove all cron jobs |

---

## 10. Useful Commands

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
