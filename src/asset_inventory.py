#!/usr/bin/env python3
"""
Cybersecurity Asset Inventory System
Week 01 - Mini Project

Features: Add, Search, Update, Delete, Display assets
Classification: Asset Type, Risk Level, Security Status
Persistence: JSON file (data/assets.json)
"""

import json
import os
import re
import ipaddress

# --- Constants for Validation & Classification ---
VALID_ASSET_TYPES = ["Workstation", "Server", "Router", "Switch", "Application"]
VALID_RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
VALID_STATUSES = ["Secure", "Warning", "Vulnerable"]

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "assets.json")


# --- Utility / Validation Functions ---
def validate_ip(ip_str):
    """Validate IPv4 address format."""
    try:
        ipaddress.IPv4Address(ip_str.strip())
        return True
    except ValueError:
        return False

def validate_choice(value, valid_list):
    """Case-insensitive validation and normalization."""
    normalized = value.strip().title()
    # Special handling for Application etc already title-cased
    for valid in valid_list:
        if normalized.lower() == valid.lower():
            return True, valid
    return False, None

def get_validated_input(prompt, valid_list=None, allow_empty=False, validator=None):
    """Loop until valid input is received."""
    while True:
        value = input(prompt).strip()
        if allow_empty and value == "":
            return value
        if not value and not allow_empty:
            print("  [!] Input cannot be empty. Try again.")
            continue
        if validator:
            if validator(value):
                return value
            else:
                print(f"  [!] Invalid format. Try again.")
                continue
        if valid_list:
            is_valid, normalized = validate_choice(value, valid_list)
            if is_valid:
                return normalized
            else:
                print(f"  [!] Invalid value. Allowed: {', '.join(valid_list)}")
                continue
        return value


# --- Persistence ---
def load_assets():
    """Load assets from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        print(f"[!] Warning: Could not read {DATA_FILE}, starting with empty inventory.")
        return []

def save_assets(assets):
    """Save assets to JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(assets, f, indent=2)
        return True
    except IOError as e:
        print(f"[!] Error saving assets: {e}")
        return False


# --- Core Operations ---
def add_asset(assets):
    """Add a single asset with full validation."""
    print("\n--- Add New Asset ---")
    asset_id = get_validated_input("Asset ID: ")
    # Duplicate check
    if any(a["asset_id"].lower() == asset_id.lower() for a in assets):
        print(f"[!] Asset ID '{asset_id}' already exists. Aborting.")
        return

    asset_name = get_validated_input("Asset Name: ")
    asset_type = get_validated_input(f"Asset Type ({'/'.join(VALID_ASSET_TYPES)}): ", valid_list=VALID_ASSET_TYPES)
    ip_address = get_validated_input("IP Address: ", validator=validate_ip)
    # IP validator retry message is generic, improve
    while not validate_ip(ip_address):
        print(f"  [!] Invalid IP. Example: 192.168.1.10")
        ip_address = input("IP Address: ").strip()

    os_name = input("Operating System: ").strip()
    if not os_name:
        os_name = "N/A"

    department = get_validated_input("Department: ")
    # Some sample uses Owner/Department as same field
    risk_level = get_validated_input(f"Risk Level ({'/'.join(VALID_RISK_LEVELS)}): ", valid_list=VALID_RISK_LEVELS)
    status = get_validated_input(f"Security Status ({'/'.join(VALID_STATUSES)}): ", valid_list=VALID_STATUSES)

    new_asset = {
        "asset_id": asset_id,
        "asset_name": asset_name,
        "asset_type": asset_type,
        "ip_address": ip_address,
        "os": os_name,
        "department": department,
        "risk_level": risk_level,
        "status": status
    }
    assets.append(new_asset)
    save_assets(assets)
    print(f"\n[+] Asset '{asset_id}' added successfully!")

def add_assets_batch():
    """Batch add - sample input style: Enter number of assets"""
    assets = load_assets()
    try:
        n = int(input("Enter number of assets: ").strip())
    except ValueError:
        print("[!] Invalid number.")
        return

    for i in range(1, n + 1):
        print(f"\nAsset {i}")
        asset_id = get_validated_input("Asset ID: ")
        if any(a["asset_id"].lower() == asset_id.lower() for a in assets):
            print(f"[!] Duplicate ID '{asset_id}' - skipping this asset.")
            # consume remaining inputs to keep flow? just skip
            # need to still consume other fields? easier: skip rest
            # ask to re-enter
            while any(a["asset_id"].lower() == asset_id.lower() for a in assets):
                print("  Please enter a unique Asset ID.")
                asset_id = get_validated_input("Asset ID: ")

        asset_name = get_validated_input("Asset Name: ")
        asset_type = get_validated_input(f"Asset Type ({'/'.join(VALID_ASSET_TYPES)}): ", valid_list=VALID_ASSET_TYPES)

        ip_address = input("IP Address: ").strip()
        while not validate_ip(ip_address):
            print("  [!] Invalid IP address. Example: 192.168.1.10")
            ip_address = input("IP Address: ").strip()

        os_name = input("Operating System: ").strip()
        if not os_name:
            os_name = "N/A"

        department = get_validated_input("Department: ")
        risk_level = get_validated_input(f"Risk Level ({'/'.join(VALID_RISK_LEVELS)}): ", valid_list=VALID_RISK_LEVELS)
        status = get_validated_input(f"Security Status ({'/'.join(VALID_STATUSES)}): ", valid_list=VALID_STATUSES)

        assets.append({
            "asset_id": asset_id,
            "asset_name": asset_name,
            "asset_type": asset_type,
            "ip_address": ip_address,
            "os": os_name,
            "department": department,
            "risk_level": risk_level,
            "status": status
        })

    save_assets(assets)
    print(f"\n[+] {n} asset(s) processed. Current total: {len(assets)}")
    # Auto display after batch add to match expected output requirement
    display_assets(assets)

def display_assets(assets=None):
    """Display all assets in formatted view with summary."""
    if assets is None:
        assets = load_assets()

    print("\n=========================================")
    print(" CYBERSECURITY ASSET INVENTORY")
    print("=========================================\n")

    if not assets:
        print("No assets found in inventory.")
        print("\n=========================================")
        print("Total Assets : 0")
        print("=========================================\n")
        return

    for asset in assets:
        print(f"Asset ID : {asset.get('asset_id', 'N/A')}")
        print(f"Asset Name : {asset.get('asset_name', 'N/A')}")
        print(f"Asset Type : {asset.get('asset_type', 'N/A')}")
        print(f"IP Address : {asset.get('ip_address', 'N/A')}")
        print(f"OS : {asset.get('os', 'N/A')}")
        print(f"Department : {asset.get('department', 'N/A')}")
        print(f"Risk Level : {asset.get('risk_level', 'N/A')}")
        print(f"Status : {asset.get('status', 'N/A')}")
        print("\n-----------------------------------------\n")

    # Summary counts
    total = len(assets)
    critical = sum(1 for a in assets if a.get("risk_level", "").lower() == "critical")
    high = sum(1 for a in assets if a.get("risk_level", "").lower() == "high")
    medium = sum(1 for a in assets if a.get("risk_level", "").lower() == "medium")
    low = sum(1 for a in assets if a.get("risk_level", "").lower() == "low")
    vulnerable = sum(1 for a in assets if a.get("status", "").lower() == "vulnerable")
    warning = sum(1 for a in assets if a.get("status", "").lower() == "warning")
    secure = sum(1 for a in assets if a.get("status", "").lower() == "secure")

    print("=========================================\n")
    print(f"Total Assets : {total}")
    print(f"Critical Assets : {critical}")
    print(f"High Risk Assets : {high}")
    print(f"Medium Risk Assets : {medium}")
    if low > 0 or True:  # keep consistent; spec only shows up to medium but we show low if needed
        # Only show Low if present to not deviate too much, but we will show to be complete
        # To match spec exactly when low=0, we can optionally hide - but we include for completeness
        pass
    # To exactly match spec expected output (4 risk lines), we will print as spec:
    # If you want full summary uncomment below
    # print(f"Low Risk Assets : {low}")
    # print(f"Secure Assets : {secure}")
    # print(f"Warning Assets : {warning}")
    print(f"Vulnerable Assets : {vulnerable}")
    print("\n=========================================")

def search_asset(assets=None):
    """Search asset by ID or Name."""
    if assets is None:
        assets = load_assets()
    if not assets:
        print("\n[!] No assets to search.")
        return

    query = input("\nEnter Asset ID or Name to search: ").strip()
    found = []
    for a in assets:
        if query.lower() in a.get("asset_id", "").lower() or query.lower() in a.get("asset_name", "").lower():
            found.append(a)

    if not found:
        print(f"\n[!] No asset found matching '{query}'.")
        return

    print(f"\n[+] Found {len(found)} asset(s) matching '{query}':")
    display_assets(found)

def update_asset(assets=None):
    """Update an existing asset by ID."""
    if assets is None:
        assets = load_assets()
    if not assets:
        print("\n[!] No assets to update.")
        return

    asset_id = input("\nEnter Asset ID to update: ").strip()
    target = None
    for a in assets:
        if a.get("asset_id", "").lower() == asset_id.lower():
            target = a
            break

    if not target:
        print(f"[!] Asset ID '{asset_id}' not found.")
        return

    print(f"\n--- Updating Asset {asset_id} (leave blank to keep current) ---")
    print(f"Current: {target}")

    # Helper to update field with validation if needed
    def prompt_update(field_name, current_value, valid_list=None, validator=None, allow_empty=True):
        prompt = f"{field_name} [{current_value}]: "
        new_val = input(prompt).strip()
        if new_val == "":
            return current_value
        if valid_list:
            is_valid, normalized = validate_choice(new_val, valid_list)
            if not is_valid:
                print(f"  [!] Invalid value. Allowed: {', '.join(valid_list)} - keeping old value.")
                return current_value
            return normalized
        if validator and not validator(new_val):
            print(f"  [!] Invalid format - keeping old value.")
            return current_value
        return new_val

    target["asset_name"] = prompt_update("Asset Name", target.get("asset_name", ""))
    target["asset_type"] = prompt_update("Asset Type", target.get("asset_type", ""), valid_list=VALID_ASSET_TYPES)
    target["ip_address"] = prompt_update("IP Address", target.get("ip_address", ""), validator=validate_ip)
    target["os"] = prompt_update("Operating System", target.get("os", ""), allow_empty=True)
    target["department"] = prompt_update("Department", target.get("department", ""))
    target["risk_level"] = prompt_update("Risk Level", target.get("risk_level", ""), valid_list=VALID_RISK_LEVELS)
    target["status"] = prompt_update("Security Status", target.get("status", ""), valid_list=VALID_STATUSES)

    save_assets(assets)
    print(f"\n[+] Asset '{asset_id}' updated successfully!")

def delete_asset(assets=None):
    """Delete an asset by ID."""
    if assets is None:
        assets = load_assets()
    if not assets:
        print("\n[!] No assets to delete.")
        return

    asset_id = input("\nEnter Asset ID to delete: ").strip()
    index = -1
    for i, a in enumerate(assets):
        if a.get("asset_id", "").lower() == asset_id.lower():
            index = i
            break

    if index == -1:
        print(f"[!] Asset ID '{asset_id}' not found.")
        return

    print(f"\nAsset to delete:")
    display_assets([assets[index]])
    confirm = input(f"Are you sure you want to delete '{asset_id}'? (y/N): ").strip().lower()
    if confirm == 'y' or confirm == 'yes':
        deleted = assets.pop(index)
        save_assets(assets)
        print(f"[+] Asset '{deleted.get('asset_id')}' deleted successfully. Remaining: {len(assets)}")
    else:
        print("[*] Deletion cancelled.")


def security_summary(assets=None):
    """Display security summary only."""
    if assets is None:
        assets = load_assets()
    print("\n========== SECURITY SUMMARY ==========")
    if not assets:
        print("No assets in inventory.")
        return
    total = len(assets)
    from collections import Counter
    risk_counter = Counter(a.get("risk_level", "Unknown") for a in assets)
    status_counter = Counter(a.get("status", "Unknown") for a in assets)
    type_counter = Counter(a.get("asset_type", "Unknown") for a in assets)

    print(f"Total Assets: {total}")
    print("\n-- By Risk Level --")
    for level in VALID_RISK_LEVELS:
        print(f"  {level}: {risk_counter.get(level, 0)}")
    print("\n-- By Security Status --")
    for s in VALID_STATUSES:
        print(f"  {s}: {status_counter.get(s, 0)}")
    print("\n-- By Asset Type --")
    for t in VALID_ASSET_TYPES:
        print(f"  {t}: {type_counter.get(t, 0)}")

    # Attention needed
    critical_vuln = [a for a in assets if a.get("risk_level") == "Critical" and a.get("status") == "Vulnerable"]
    high_vuln = [a for a in assets if a.get("risk_level") == "High" and a.get("status") in ["Vulnerable", "Warning"]]
    if critical_vuln:
        print(f"\n[!] IMMEDIATE ATTENTION: {len(critical_vuln)} Critical & Vulnerable asset(s):")
        for a in critical_vuln:
            print(f"    - {a['asset_id']} ({a['asset_name']}) @ {a['ip_address']}")
    if high_vuln:
        print(f"\n[!] High Risk Attention: {len(high_vuln)} High risk asset(s) needing review.")
    print("======================================")


def print_menu():
    print("\n========== CYBERSECURITY ASSET INVENTORY SYSTEM ==========")
    print("1. Add Asset")
    print("2. Add Multiple Assets (Batch)")
    print("3. Display All Assets")
    print("4. Search Asset")
    print("5. Update Asset")
    print("6. Delete Asset")
    print("7. Security Summary")
    print("8. Exit")
    print("==========================================================")

def main():
    assets = load_assets()
    print("Cybersecurity Asset Inventory System Initialized.")
    print(f"Loaded {len(assets)} asset(s) from {DATA_FILE}")

    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            # reload to ensure fresh
            assets = load_assets()
            add_asset(assets)
            assets = load_assets()
        elif choice == '2':
            add_assets_batch()
            assets = load_assets()
        elif choice == '3':
            assets = load_assets()
            display_assets(assets)
        elif choice == '4':
            assets = load_assets()
            search_asset(assets)
        elif choice == '5':
            assets = load_assets()
            update_asset(assets)
            assets = load_assets()
        elif choice == '6':
            assets = load_assets()
            delete_asset(assets)
            assets = load_assets()
        elif choice == '7':
            assets = load_assets()
            security_summary(assets)
        elif choice == '8':
            print("\nExiting system. Goodbye!")
            break
        else:
            print("[!] Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    main()
