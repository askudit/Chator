# TorChat Setup GUI

A Python-based GUI tool to run **Tor hidden services** and connect clients where you discuss under no-ones hood.

## [*] Features

* [*] **Automatic dependency setup**

  * Installs Chocolatey (if missing) in case of execution initial failure goto chocolatey.org/install or use these command in windows-powershell(admin):
     * "Set-ExecutionPolicy Bypass -Scope Process"
     * "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
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

1. On launch, the app checks for **Chocolatey** and **Tor** and installs them if missing in pre-defined directories.
2. You can start Tor as a **hidden service** with one click.
3. Use the given .py file in /server and start a **server**.
4. Then with the pre-defined user list and creds they can join the server.
5. Required `.onion` address will be shown in the chator.exe.

   Happy anon

## [*] Getting Started

1. Clone this repo:

   ```bash
   git clone https://github.com/yourusername/torchat-setup.git
   cd torchat-setup
   ```
2. Install dependencies(for developers):

   ```bash
   pip install -r requirements.txt
   ```
## [*] For developers:

   This executable application was converted from .py to .exe using auto-py-to-exe, the dev's can utilize the /src/Chator.py for further development and similarly convert it to .exe using the same config.
   
## [*] Requirements

* Python 3.8+(only)

## ⚠️ Notes

* The app binds hidden services to port `24456` by default.
* Make sure the port is free before starting the server.
* Logs and `.onion` hostname will be displayed after Tor fully boots up.
