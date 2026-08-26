import os
import subprocess
import sys
import re
import ctypes
from pathlib import Path

def run_command(command, error_msg):
    """Executes a shell command and halts on failure."""
    try:
        subprocess.run(command, check=True, shell=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[X] {error_msg}\n{e.stderr.decode()}")
        sys.exit(1)

def is_ntfs(drive_letter):
    """Verifies the drive is formatted as NTFS for hardlink support."""
    buffer = ctypes.create_unicode_buffer(1024)
    result = ctypes.windll.kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(f"{drive_letter}:\\"),
        None, 0, None, None, None,
        buffer, ctypes.sizeof(buffer)
    )
    return result and buffer.value == "NTFS"

def get_torrent_dir():
    """Scans for torrent clients and handles standard vs non-standard routing."""
    local = os.environ.get('LOCALAPPDATA', 'C:\\Users\\Default\\AppData\\Local')
    roaming = os.environ.get('APPDATA', 'C:\\Users\\Default\\AppData\\Roaming')
    standard = os.path.join(local, "qBittorrent", "BT_backup")
    
    potential_paths = [
        standard,
        os.path.join(roaming, "qBittorrent", "BT_backup"),
        os.path.join(roaming, "BitTorrent"),
        os.path.join(roaming, "uTorrent")
    ]
    
    print("Scanning for existing torrent installations...")
    for p in potential_paths:
        if os.path.exists(p):
            if p.lower() != standard.lower():
                print(f"\n[!] Discovered non-standard torrent backup directory:\n    {p}")
                if input("Use this discovered location? (Y/N): ").strip().lower() == 'y':
                    return p
                print("[*] Opting for the standard documentation path instead.")
            return standard # If it was the standard one, or they rejected the non-standard one
            
    print("[!] No existing installations found. Enforcing standard path.")
    return standard

def main():
    print("=== Cross-Seed Windows Setup Wizard ===\n")
    
    # 1. Prerequisites & Installation
    print("--- 1. Prerequisites & Installation ---")
    run_command("node -v", "Node.js is missing. Please install Node.js 20+.")
    run_command("npm -v", "npm is missing.")
    print("[*] Node.js and npm verified.")
    
    run_command("npm install -g cross-seed", "Failed to install cross-seed via npm.")
    run_command("cross-seed gen-config", "Failed to generate default cross-seed config.")
    print("[*] cross-seed installed and default config generated.\n")

    # 2. Automated Directory Setup
    print("--- 2. Automated Directory Setup ---")
    torrent_dir_raw = get_torrent_dir()
    
    base_drive = os.environ.get('SystemDrive', 'C:')
    data_dir_raw = os.path.join(base_drive, "\\Torrents", "Movies")
    link_dir_raw = os.path.join(base_drive, "\\Torrents", "cross-seed")

    print("\nTarget Layout:")
    print(f"  - Torrent Dir: {torrent_dir_raw}")
    print(f"  - Data Dir:    {data_dir_raw}")
    print(f"  - Link Dir:    {link_dir_raw}\n")

    dirs_to_check = [torrent_dir_raw, data_dir_raw, link_dir_raw]
    missing_dirs = [p for p in dirs_to_check if not Path(p).exists()]
            
    if missing_dirs:
        print("Missing directories detected:")
        for p in missing_dirs: print(f"  [X] {p}")
            
        if input("\nGenerate these missing directories now? (Y/N): ").strip().lower() != 'y':
            print("\nSetup aborted. Directories must exist to proceed.")
            sys.exit(1)
            
        for p in missing_dirs:
            Path(p).mkdir(parents=True, exist_ok=True)
            print(f"  [*] Created: {p}")
    else:
        print("[*] All required directories are already present.")

    # 3. Volume & Hardlink Validation
    print("\n--- 3. Volume & Hardlink Validation ---")
    data_drive = data_dir_raw.split(':')[0].upper()
    link_drive = link_dir_raw.split(':')[0].upper()
    
    if data_drive != link_drive:
        print(f"[X] ERROR: Data ({data_drive}:) and Link ({link_drive}:) must be on the same drive.")
        sys.exit(1)

    if not is_ntfs(data_drive):
        print(f"[X] ERROR: Drive {data_drive}: is not NTFS. Hardlinks require NTFS.")
        sys.exit(1)
    print("[*] Validation passed (Same drive + NTFS).\n")

    # 4. Injecting Configuration
    print("--- 4. Injecting Configuration ---")
    config_path = Path(os.environ.get('LOCALAPPDATA', '')) / "cross-seed" / "config.js"
    
    if not config_path.exists():
        print(f"[X] Config file not found at {config_path}")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = f.read()

    # Condense string escaping for JavaScript formatting
    t_dir, d_dir, l_dir = [p.replace('\\', '\\\\') for p in (torrent_dir_raw, data_dir_raw, link_dir_raw)]

    # Safely inject paths via regex lambdas
    config = re.sub(r'(torrentDir:\s*)".*?"', lambda m: f'{m.group(1)}"{t_dir}"', config)
    config = re.sub(r'(dataDirs:\s*\[).*?(\])', lambda m: f'{m.group(1)}"{d_dir}"{m.group(2)}', config, flags=re.DOTALL)
    config = re.sub(r'(linkDirs:\s*\[).*?(\])', lambda m: f'{m.group(1)}"{l_dir}"{m.group(2)}', config, flags=re.DOTALL)

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config)

    print(f"[*] Success! Paths escaped and injected into:\n    {config_path}")
    print("\nSetup complete. You can now configure your trackers in the config file.")

if __name__ == "__main__":
    main()