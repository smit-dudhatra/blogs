# 🐍 Python Virtual Environment

---

## 📌 Introduction

A Python virtual environment is an isolated directory on your computer that contains its own Python interpreter, libraries, and scripts. Its main purpose is to manage project-specific dependencies without interfering with other projects or the system's global Python installation, which prevents version conflicts.

---

## 🧠 Core Concepts

### What is a Python Virtual Environment?

A Python virtual environment acts as a self-contained **"toolbox"** for each project, ensuring that the specific tools and library versions needed for that project are always available and neatly organized.

### Why Are Python Virtual Environments Necessary?

| Reason | Description |
|---|---|
| **Dependency Isolation** | Different projects often require different versions of the same library. For example, one project might need version `1.0` of a library, while another needs version `2.0`. A virtual environment ensures each project uses the correct version without conflicts. |
| **System Protection** | It prevents accidental modification or corruption of the operating system's default Python installation, which the system itself may rely on for its own tools. |
| **Reproducibility & Portability** | Virtual environments make projects more portable and reproducible by allowing developers to list all required packages and their exact versions in a `requirements.txt` file. Other users can then easily recreate the exact same environment. |
| **Permission Management** | They allow you to install packages in a local project directory without needing administrator privileges — a common limitation in shared or corporate environments. |

---

### ⚙️ How Do They Work?

When you **activate** a virtual environment, it temporarily modifies your system's `PATH` environment variable to prioritize the Python interpreter and associated packages within that specific environment's directory. This effectively "tricks" Python and `pip` into installing and loading packages into the isolated directory instead of the global location.

---

### 🛠️ Common Tools

| Tool | Description |
|---|---|
| **venv** | The standard tool included in the Python 3 standard library. It is the recommended way to create virtual environments in modern Python. |
| **virtualenv** | A popular third-party tool that offers more features and supports Python versions older than 3.3. |
| **conda** | A powerful, general-purpose package and environment manager commonly used in data science. It can also manage non-Python libraries. |

---

## 🚀 Usage

### Step 1 — Create and Activate the Virtual Environment

```bash
python3.14 -m venv /home/trading_scripts/venv
```

```bash
source /home/trading_scripts/venv/bin/activate
```

### Step 2 — Install Required Packages

```bash
pip install fyers-apiv3 kiteconnect pyotp requests twisted zope.interface
```

### Step 3 — Run the Script (with venv active)

```bash
source /home/trading_scripts/venv/bin/activate
python3.14 /home/trading_scripts/nifty50_straddle_script.py
```

---

### 🔗 What Is the Direct Launcher?

```bash
/home/trading_scripts/venv/bin/python /home/trading_scripts/nifty50_straddle_script.py
```

This runs the script using the virtual environment's Python interpreter **directly by full path**, without needing to run `source venv/bin/activate` first.

**This is useful when:**

- ⏰ Running via a **cron job** — cron does not load shell profiles, so `activate` does not work
- ⚙️ Running via a **systemd service**
- 🔐 Running via an **SSH one-liner**
- 📦 Any case where you cannot or do not want to activate the virtual environment manually

> **Note:** If you are always manually activating the virtual environment in a terminal, you do not need this launcher.

---

### 🖥️ Running the Script Directly in the Terminal

```bash
/home/trading_scripts/venv/bin/python /home/trading_scripts/nifty50_straddle_script.py
```

---

## ⚙️ systemd Service Configuration

To run the script as a background service that automatically restarts on failure, create a systemd unit file:

**File path:** `/etc/systemd/system/nifty50_straddle.service`

```ini
[Unit]
Description=Nifty50 Straddle Trading Script
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/trading_scripts
ExecStart=/home/trading_scripts/venv/bin/python /home/trading_scripts/nifty50_straddle_script.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## ⚠️ Disadvantages

| Disadvantage | Description |
|---|---|
| **Disk Space Overhead** | Each virtual environment creates its own copy of the Python interpreter and packages, which can consume significant disk space across multiple projects. |
| **Manual Management** | You must remember to activate the correct virtual environment before working on a project. Forgetting to do so can lead to packages being installed globally by mistake. |
| **Not Truly Isolated** | `venv` does not isolate system-level dependencies (e.g., C libraries). For full isolation, tools like **Docker** are more appropriate. |
| **No Cross-Language Support** | Unlike `conda`, `venv` and `virtualenv` only manage Python packages and cannot handle non-Python dependencies. |
| **Environment Duplication** | Sharing a virtual environment directory directly between machines is unreliable due to hardcoded paths. You must always recreate it using `requirements.txt`. |

---

## 📄 Quick Reference

| Task | Command |
|---|---|
| Create virtual environment | `python3.14 -m venv /home/trading_scripts/venv` |
| Activate virtual environment | `source /home/trading_scripts/venv/bin/activate` |
| Deactivate virtual environment | `deactivate` |
| Install packages | `pip install <package-name>` |
| Save dependencies | `pip freeze > requirements.txt` |
| Restore dependencies | `pip install -r requirements.txt` |
| Run script directly | `/home/trading_scripts/venv/bin/python script.py` |

---

*Last updated: 2026-03-23*
