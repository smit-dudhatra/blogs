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
> The service will not auto-restart if the script exits. This is intentional — if a major exception occurs (e.g., insufficient funds, broker API error), the script calls `exit(0)` and the service stops cleanly. This prevents uncontrolled retries and avoids hammering the broker server.

### 8b. Validate the service file syntax

Before reloading systemd, verify that the service file has no syntax errors:

```bash
systemd-analyze verify /etc/systemd/system/nifty-straddle.service
```

| Output | Meaning |
|---|---|
| No output | File is valid ✓ |
| Warnings or errors printed | Something is wrong — fix before proceeding |

> **Note:** `sudo systemctl daemon-reload` silently ignores bad syntax and will not warn you about errors. Always run `systemd-analyze verify` first after editing the service file to catch issues explicitly.

### 8c. Reload systemd

After confirming the file is valid, reload the systemd daemon so it picks up the changes:

```bash
sudo systemctl daemon-reload
```

> `daemon-reload` instructs systemd to rescan all unit files, rebuild the dependency tree, and rerun generators — without restarting the entire system.

### 8d. Disable boot auto-start (important — we use cron instead)

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

This is correct. `disabled` means it will not auto-start on boot. Your cron job still starts it on schedule as usual.

### 8e. Manually start the service

```bash
sudo systemctl start nifty-straddle
```

### 8f. Check actual running status

```bash
systemctl status nifty-straddle
```

| Output | Meaning |
|---|---|
| `Active: active (running)` | Script is running right now |
| `Active: inactive (dead)` | Script is stopped ✓ |

### 8g. Stop the service

To stop the service at any time — including mid-session if you need to halt the script abruptly:

```bash
sudo systemctl stop nifty-straddle
```

> systemd sends `SIGTERM` to the Python process, which kills it immediately. Use this whenever you need to stop the bot mid-run — for example, at 11:30 AM before market close.

### 8h. View live logs

```bash
sudo journalctl -u nifty-straddle -f
```

---

## 9. Journal Log Management

### Why this matters

Your script prints heavily — live ticker data, order logs, and minute-by-minute checks. `journalctl` stores all of it. Without a size limit, the journal grows unboundedly and can fill your VPS disk over weeks.

### 9a. Check current journal disk usage

Run this at any time to see how much disk space your logs are consuming:

```bash
journalctl --disk-usage
```

Example output:
```
Archived and active journals take up 16.0M in the file system.
```

| Term | Description |
|---|---|
| **Active journals** | Logs from currently running services (being written right now) |
| **Archived journals** | Old rotated log files from previous service runs |
| **16 MB total** | Completely fine — a typical VPS has 20–40 GB of disk space |

You only need to act if usage grows to several hundred MB or more. The one-time cap below handles that automatically.

### 9b. Set a permanent 100 MB size cap (run once, not in cron)

This tells `journald` to auto-delete the oldest log entries whenever total usage exceeds 100 MB. Set it once and never think about it again:

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
> This is completely normal. The 100 MB cap does not shrink existing logs — it only prevents future growth beyond 100 MB. Since 16 MB is already well under the limit, journald has nothing to delete. The cap will kick in automatically once logs accumulate and approach 100 MB, at which point journald will start auto-deleting the oldest entries to stay within the limit.

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
| `sudo systemctl status nifty-straddle` | Check if the service is running or stopped |
| `sudo systemctl enable nifty-straddle` | Mark the service to auto-start on boot |
| `sudo systemctl disable nifty-straddle` | Remove the auto-start on boot mark |
| `sudo systemctl daemon-reload` | Reload systemd config after editing the service file |
| `sudo systemctl reset-failed nifty-straddle` | Clear failed state and allow restarts again |
| `systemd-analyze verify /etc/systemd/system/nifty-straddle.service` | Validate service file syntax |

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
| `systemctl enable` | Marks the service to **auto-start on every boot** |
| `systemctl disable` | Removes the **auto-start on boot** mark |

`enabled` simply means the service will start when the VPS reboots — it says nothing about whether the process is running right now. Always use `systemctl status` to check the actual running state.

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

**STATE** — what the service is currently configured to do on boot:

| State | Meaning |
|---|---|
| `enabled` | Will auto-start on boot |
| `disabled` | Will not auto-start on boot |
| `static` | Cannot be enabled/disabled; started by other units only |
| `masked` | Completely blocked — cannot be started at all |

**PRESET** — the distribution's default recommendation for this service:

| Preset | Meaning |
|---|---|
| `enabled` | Ubuntu recommends this service be enabled by default |
| `disabled` | Ubuntu recommends this service be disabled by default |

> The PRESET column shows `enabled` because the `.service` file declares `WantedBy=multi-user.target`, which follows the standard Ubuntu convention. PRESET does not change unless you explicitly run `systemctl preset`. It is only a recommendation — your actual STATE (`disabled`) is what matters.

---

### Stopping the script abruptly mid-session

If the script is running (e.g., cron started it at 8:55 AM) and you need to stop it immediately at any point during the day:

```bash
sudo systemctl stop nifty-straddle
```

systemd sends `SIGTERM` to the Python process, which kills it immediately. Confirm it has stopped:

```bash
systemctl status nifty-straddle
# Expected: Active: inactive (dead)
```

---

### What is a symlink?

A symlink (symbolic link) is a file that **points to another file or directory** — similar to a shortcut.

```
/etc/systemd/system/multi-user.target.wants/
    nifty-straddle.service  →  /etc/systemd/system/nifty-straddle.service
```

| Type | How it works |
|---|---|
| **Hard link** | Points directly to data on disk (same inode) — must be on the same filesystem |
| **Symlink** | Points to a path — can cross filesystems and point to directories |

Deleting a symlink leaves the original file completely unaffected.

**How this relates to systemd:**
When you run `sudo systemctl enable nifty-straddle`, systemd creates a symlink inside `multi-user.target.wants/` — that is how it knows to start the service during boot. When you run `sudo systemctl disable nifty-straddle`, it simply removes that symlink. The `.service` file itself is never touched.

---

### What does `[Install] WantedBy=multi-user.target` mean?

The `[Install]` section in a `.service` file defines **how the service gets linked into the system** when you run `systemctl enable`.

```ini
[Install]
WantedBy=multi-user.target
```

`multi-user.target` is the standard Linux boot state where:
- The environment is non-graphical
- Networking is up
- The system is fully running and ready for use

When you run `sudo systemctl enable nifty-straddle`, systemd creates the following symlink:

```
/etc/systemd/system/multi-user.target.wants/nifty-straddle.service
    → /etc/systemd/system/nifty-straddle.service
```

This tells systemd: *"when `multi-user.target` is reached during boot, start this service as well."*

> **In your setup**, since cron is used to start the service rather than `systemctl enable`, the `[Install]` section has no effect on day-to-day operation. It is kept in the file as a convention so the service could be boot-enabled in the future if needed.

---

### Validating the service file syntax

Always validate the service file after creating or editing it. Unlike `daemon-reload`, which silently ignores syntax errors, `systemd-analyze verify` explicitly reports any issues:

```bash
systemd-analyze verify /etc/systemd/system/nifty-straddle.service
```

| Output | Meaning |
|---|---|
| No output | File is valid ✓ |
| Warnings or errors printed | Something is wrong — fix before reloading |

**Recommended workflow after any edit to the service file:**

```bash
# Step 1 — Validate syntax
systemd-analyze verify /etc/systemd/system/nifty-straddle.service

# Step 2 — Reload systemd (only after syntax is confirmed clean)
sudo systemctl daemon-reload

# Step 3 — Confirm the service status
sudo systemctl status nifty-straddle
```

---

### `Restart=` — all possible values

The `Restart=` directive controls under what conditions systemd will automatically restart your service after it exits.

| Value | Restarts when... |
|---|---|
| `no` | Never — the service is never restarted automatically (default) |
| `always` | Any exit — success, failure, signal, or timeout |
| `on-failure` | Non-zero exit code, killed by a signal, or timeout |
| `on-success` | Only when the process exits cleanly with code `0` |
| `on-abnormal` | Killed by a signal, timeout, or watchdog — but NOT a non-zero exit code |
| `on-abort` | Only when killed by an uncaught/unhandled signal |
| `on-watchdog` | Only when the watchdog timeout expires |

**Detailed explanation of each value:**

- **`no`** — systemd never restarts the service regardless of how it exits. Used when the service is intentionally short-lived or managed externally (e.g., by cron). This is what your trading bot uses.

- **`always`** — systemd restarts the service no matter what — whether it exited cleanly with code `0`, crashed with an error, or was killed by a signal. Useful for services that should never go down (e.g., a web server).

- **`on-failure`** — the most common production choice. Restarts only on unexpected exits: non-zero exit codes, signal kills, or timeouts. Does not restart on a clean `exit(0)`. Ideal for services where a graceful shutdown should be respected.

- **`on-success`** — restarts only when the process exits with code `0`. Rarely used in practice; mostly useful for batch jobs that should re-run after a successful completion.

- **`on-abnormal`** — restarts when the process is killed by a signal (e.g., `SIGKILL`, `SIGSEGV`), hits a timeout, or triggers the watchdog. A non-zero exit from inside the code does NOT trigger a restart. Useful when you want to distinguish between a controlled error exit and an unexpected crash.

- **`on-abort`** — restarts only when the process is terminated by an uncaught signal that would normally produce a core dump (e.g., `SIGABRT`, `SIGSEGV`). A finer-grained subset of `on-abnormal`.

- **`on-watchdog`** — restarts only when the watchdog timer expires (requires the service to implement systemd watchdog keep-alive notifications). Rarely needed outside of highly reliable system services.

---

### `StartLimitBurst` and `StartLimitIntervalSec` — restart rate limiting

These two directives act as a **rate limiter** to prevent systemd from restarting a crashing service in an infinite loop.

```ini
StartLimitBurst=3
StartLimitIntervalSec=600
```

This means: **allow at most 3 restarts within any 10-minute window.**

If the service crashes and restarts 3 times in under 10 minutes, systemd gives up, sets the service to a `failed` state, and stops attempting any further restarts.

**Example with `RestartSec=60`:**

```
crash → wait 60s → restart (1)
crash → wait 60s → restart (2)
crash → wait 60s → restart (3)
crash → LIMIT HIT → service enters "failed" state, no more restarts
```

With `RestartSec=60` and `StartLimitBurst=3`, the limit is hit in approximately 4 minutes.

**Why this matters for your trading bot:**

If the Fyers API goes completely down and the script crashes on every startup, without this limit systemd would restart it indefinitely — potentially making repeated bad API calls or placing duplicate orders on recovery. With the rate limit in place, after 3 failures systemd stops and waits for manual intervention.

**Check status after the limit is hit:**

```bash
sudo systemctl status nifty-straddle
# shows: "start request repeated too quickly"
```

**Reset the failed state and allow restarts again:**

```bash
sudo systemctl reset-failed nifty-straddle
sudo systemctl start nifty-straddle
```

---

### Redundant settings — do they cause issues?

No. Redundant settings in a service file cause **zero issues** — no performance impact, no errors, nothing serious.

systemd reads and applies each directive independently. If a setting has no effect because another directive already covers it, systemd silently ignores it.

The only downside is readability — someone reading your service file later might be confused about why a particular directive is there. That is the extent of it.

---

### Comments in a service file

Use `#` at the start of a line to write a comment. Comments are ignored by systemd entirely.

```ini
[Service]
# This prevents the service from restarting after a clean exit(0)
Restart=no

# Ensures Python output is not buffered — logs appear in journald immediately
Environment=PYTHONUNBUFFERED=1
```

Comments can be placed anywhere in the file — inside any section or between sections. They are purely for human readability and have no effect on behaviour.

---

## 🕐 Cron Schedule Summary (IST ↔ UTC)

| Time (IST) | Time (UTC) | Action | Days |
|---|---|---|---|
| 8:50 AM | 3:20 AM | Stop service | Every day |
| 8:55 AM | 3:25 AM | Start service | Mon & Tue only |
| 3:35 PM | 10:05 AM | Stop service | Every day |
| 12:00 AM (Sun) | 6:00 PM (Sat) | Clean journal logs | Weekly |
