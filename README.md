# TorChat Setup GUI

A Python-based GUI tool to easily set up and run **Tor hidden services** and connect clients on a custom port (default: `24456`).
It provides a simple interface for managing **Tor installation**, **hidden service creation**, and **Python chat script execution** from the same window.

## [*] Features

* [*] **Automatic dependency setup**

  * Installs Chocolatey (if missing).
  * Installs Tor using Chocolatey.
* [*] **Tor hidden service launcher**

  * Starts Tor in the background on a configurable port (default: `24456`).
  * Displays generated `.onion` address directly in the GUI.
* [*] **File browser integration**

  * Browse and select a Python script (e.g., your chat server or client).
  * Run it with automatic `s` (server) or `c` (client) input selection.
* [*] **Real-time logging**

  * Logs Tor output and script stdout/stderr in a resizable text area.
* [*] **Threaded execution**

  * Runs Tor and your script in separate threads to keep the GUI responsive.

## [*] How It Works

1. On launch, the app checks for **Chocolatey** and **Tor** and installs them if missing.
2. You can start Tor as a **hidden service** with one click.
3. Use the **file browser** to select your Python script (chat server/client).
4. Choose **Server Mode** (`s`) or **Client Mode** (`c`).
5. All logs and the `.onion` address are shown in the GUI.

## [*] Getting Started

1. Clone this repo:

   ```bash
   git clone https://github.com/yourusername/torchat-setup.git
   cd torchat-setup
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the GUI:

   ```bash
   python main.py
   ```
4. Optionally, build into an `.exe` with [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/).

## [*] Requirements

* Python 3.8+
* Tor (installed automatically via Chocolatey if missing)
* Tkinter (bundled with Python)
* pysocks
* stem

## ⚠️ Notes

* The app binds hidden services to port `24456` by default.
* Make sure the port is free before starting the server.
* Logs and `.onion` hostname will be displayed after Tor fully boots up.
