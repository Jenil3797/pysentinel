import hashlib
import os
import json
import logging
from datetime import datetime

# Setup Logging
logging.basicConfig(
    filename='logs/monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def calculate_sha256(filepath):
    """Calculates the SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read file in chunks of 4096 bytes
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except (FileNotFoundError, PermissionError) as e:
        logging.error(f"Could not read {filepath}: {e}")
        return None

def create_baseline(target_directory, baseline_path):
    """Scans directory and saves file hashes to a JSON file."""
    baseline = {}
    for root, dirs, files in os.walk(target_directory):
        for name in files:
            filepath = os.path.join(root, name)
            file_hash = calculate_sha256(filepath)
            if file_hash:
                baseline[filepath] = file_hash
    
    with open(baseline_path, 'w') as f:
        json.dump(baseline, f, indent=4)
    
    print(f"[+] Baseline created successfully in {baseline_path}")
    logging.info(f"Baseline created for {target_directory}")

def monitor_integrity(target_directory, baseline_path):
    """Compares current files against the baseline."""
    if not os.path.exists(baseline_path):
        print("[-] Error: Baseline file not found. Create one first.")
        return

    with open(baseline_path, 'r') as f:
        baseline = json.load(f)

    current_files = {}
    for root, dirs, files in os.walk(target_directory):
        for name in files:
            filepath = os.path.join(root, name)
            file_hash = calculate_sha256(filepath)
            if file_hash:
                current_files[filepath] = file_hash

    # Compare logic
    # 1. Check for modified or deleted files
    for filepath, original_hash in baseline.items():
        if filepath not in current_files:
            print(f"[!] ALERT: File Deleted - {filepath}")
            logging.warning(f"File Deleted: {filepath}")
        elif current_files[filepath] != original_hash:
            print(f"[!] ALERT: File Modified - {filepath}")
            logging.warning(f"File Modified: {filepath}")

    # 2. Check for new files
    for filepath in current_files:
        if filepath not in baseline:
            print(f"[!] ALERT: New File Created - {filepath}")
            logging.warning(f"New File Created: {filepath}")