# Cross-Seed Windows Setup Wizard

An automated Python script designed to streamline the installation and configuration of [cross-seed](https://cross-seed.org) on Windows. 

Setting up `cross-seed` natively on Windows can be tricky due to strict path escaping requirements in JavaScript and hardlink limitations across different drive volumes. This wizard completely automates the process, eliminating the most common setup errors before they happen.

## ✨ Features

* **Prerequisite Verification:** Automatically checks if Node.js (20+) and npm are installed on your system.
* **Automated Installation:** Installs `cross-seed` globally via npm and generates the default configuration file.
* **Smart Directory Scanning:** Scans standard Windows `AppData` locations for existing torrent clients (qBittorrent, uTorrent, BitTorrent) to locate your `BT_backup` folder.
* **Automatic Directory Generation:** Enforces a clean, standard directory layout and can automatically create missing data and link directories with your approval.
* **Hardlink & File System Validation:** Validates that your data and link directories are located on the same drive and verifies that the drive is formatted as NTFS (a strict requirement for hardlinks).
* **Syntax-Safe Config Injection:** Automatically escapes Windows backslashes (converting `\` to `\\`) and safely injects your custom paths directly into the `config.js` file, preventing the most common JavaScript syntax errors.

## 🚀 How to Use

### Requirements
* **Python 3.x** installed on your system.
* **Node.js (v20+)** (The script will warn you if it is missing).

### Running the Wizard
1. Download the script or clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/cross-seed-windows-wizard.git](https://github.com/YourUsername/cross-seed-windows-wizard.git)
   cd cross-seed-windows-wizard


2. Run the script via the command prompt or terminal:

Bash
python wizard.py
(Note: If you saved your file as cross-seedarr.py, run python cross-seedarr.py instead).


3. Follow the interactive prompts. The wizard will scan your system, ask for approval to create missing directories, validate your drives, and configure your config.js file.

|----------:🛠️ What it Modifies:----------|


This script directly modifies the cross-seed configuration file located at:
C:\Users\<YourUsername>\AppData\Local\cross-seed\config.js

It specifically updates the following variables based on the wizard's strict naming and escaping policies:

-torrentDir

-dataDirs

-linkDirs

Once the wizard completes, you can open your config.js file to manually configure your specific trackers, Torznab URLs, and torrent client credentials.

⚠️ Disclaimer
This is an unofficial community tool and is not affiliated with the official cross-seed project. Always review configuration changes to ensure they match your specific home server setup.
