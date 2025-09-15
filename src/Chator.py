import os
import sys
import subprocess
import shutil
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Paths
TOR_EXE = r"C:\ProgramData\chocolatey\lib\tor\tools\tor\tor.exe"
TORRC = r"C:\ProgramData\tor\torrc"
HSDIR = r"C:\Tor\hidden_service"

# Run a command helper
def run_cmd(cmd, shell=False, timeout=600):  # Timeout after 10 minutes (600 seconds)
    try:
        result = subprocess.run(cmd, shell=shell, check=False, capture_output=True, text=True, timeout=timeout)
        return result
    except subprocess.TimeoutExpired:
        print(f"[*] Command '{cmd}' timed out after {timeout} seconds.")
        return None
    except Exception as e:
        print(f"[-] Error executing command: {e}")
        return None

# Ensure Chocolatey
def ensure_chocolatey():
    choco_path = Path(r"C:\ProgramData\chocolatey\bin\choco.exe")
    if choco_path.exists():
        print("[+] Chocolatey already installed.")
        return True

    print("[*] Chocolatey not found. Installing...")
    try:
        # Fix: Clean up the PowerShell command string
        result = run_cmd(
            'Set-ExecutionPolicy AllSigned -A'
            '"Set-ExecutionPolicy Bypass -Scope Process -Force; '
            '[System.Net.ServicePointManager]::SecurityProtocol = '
            '[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; '
            'iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))"',
            shell=True
        )
        print("Chocolatey install stdout:", result.stdout)
        print("Chocolatey install stderr:", result.stderr)

        # Force refresh PATH in case choco was just installed
        os.environ["PATH"] += r";C:\ProgramData\chocolatey\bin"

        if choco_path.exists() or shutil.which("choco"):
            print("[+] Chocolatey installed successfully.")
            return True
        else:
            print("[-] Chocolatey not found after install.")
            return False
    except Exception as e:
        print("[-] Failed to install Chocolatey:", e)
        return False

# Ensure Tor
def ensure_tor():
    if Path(TOR_EXE).exists():
        print("[+] Tor already installed.")
        return True
    
    # Check if tor is available globally
    if shutil.which("tor"):
        print("[+] Tor found in PATH.")
        return True

    print("[*] Tor not found. Installing with Chocolatey...")

    # Run choco install command with a timeout
    result = run_cmd("choco install tor --force -y", shell=True, timeout=600)  # 10-minute timeout

    if result:
        print("Chocolatey install stdout:", result.stdout)
        print("Chocolatey install stderr:", result.stderr)
        if Path(TOR_EXE).exists() or shutil.which("tor"):
            print("[+] Tor installed successfully.")
            return True
        else:
            print("[-] Tor not found after install.")
            return False
    else:
        print("[-] Tor installation failed.")
        return False

if not ensure_tor():
    messagebox.showerror(
        "Installation failed",
        "Tor could not be installed automatically. Please install Tor manually from\n"
        "https://www.torproject.org/download/\n\nThen run the script again."
    )
    sys.exit(1)

# Start Tor process
def start_tor(log_widget=None):
    if log_widget:
        log_widget.insert(tk.END, "[*] Starting Tor...\n")
        log_widget.see(tk.END)

    proc = subprocess.Popen([TOR_EXE, "-f", TORRC], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    time.sleep(5)
    return proc

# Get onion address
def get_onion_address():
    hostname = Path(HSDIR, "hostname")
    if hostname.exists():
        return hostname.read_text().strip()
    return None

# GUI actions
def start_server_mode(text_widget):
    tor_proc = start_tor(text_widget)
    time.sleep(10)
    onion = get_onion_address()
    if onion:
        text_widget.insert(tk.END, f"\n[+] Hidden service running.\nYour .onion address:\n{onion}\n")
        text_widget.insert(tk.END, "\nKeep this window open to keep the server running.\n")
#        text_widget.see(tk.END,f"\n COPY THE URL START A SERVER USING THE GIVEN main.py select {s} for starting the server".format(s="s"))
        text_widget.insert(tk.END, "\n COPY THE URL START A SERVER USING THE GIVEN main.py select '{s}' for starting the server\n".format(s="s"))

    else:
        text_widget.insert(tk.END, "\n[-] Could not read .onion hostname.\n")


# Main GUI
def main():
    # Bootstrap dependencies
    if not ensure_chocolatey():
        messagebox.showerror("Setup failed", "Chocolatey installation failed.")
        sys.exit(1)

    if not ensure_tor():
        messagebox.showerror("Setup failed", "Tor installation failed.")
        sys.exit(1)

    root = tk.Tk()
    root.title("Chator")
    root.geometry("700x360")
    root.resizable(False, False)

    label = tk.Label(root, text="Start the onion server", font=("Arial", 14))
    label.pack(pady=10)

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=15)
    text_widget.insert(tk.END, "Welcome to Chator!\n")
    text_widget.insert(tk.END, "\nThis application installs dependencies like chocolatey, tor, writes config files and runs on backgound DO NOT CLOSE THIS!\n")
    text_widget.insert(tk.END, "\nIn case of failure check and free the port 24456 and start the onion server again.\n")
    text_widget.pack(padx=10, pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    btn_server = tk.Button(btn_frame, text="Start onion server", command=lambda: start_server_mode(text_widget))
    btn_server.grid(row=0, column=0, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()
