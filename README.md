# Cybersecurity Asset Inventory System – Week 01

A Python-based CLI system to manage IT assets, track security status, and prioritize risk for security administrators.

## 📋 Problem Statement
Organizations maintain many IT assets (computers, servers, routers, switches, applications). Manual management makes it difficult to identify assets, track security status, and determine which require immediate attention. This system provides CRUD operations with classification by **Asset Type** and **Risk Level**.

## ✨ Features
- **Add Asset** – Single entry with full validation
- **Batch Add** – `Enter number of assets` flow (as per sample input)
- **Display Assets** – Formatted inventory view + summary (Total/Critical/High/Medium/Vulnerable)
- **Search Asset** – By Asset ID or Asset Name (case-insensitive, partial match)
- **Update Asset** – Update any field by ID (blank keeps current value)
- **Delete Asset** – Delete by ID with confirmation
- **Security Summary** – Counts by Risk/Status/Type + flags Critical & Vulnerable assets needing immediate attention
- **Input Validation** – Strict checks for Asset Type, Risk Level, Status, IP Address, duplicate IDs
- **Persistence** – JSON storage at `data/assets.json` (auto load/save)

## 🗂️ Asset Fields
| Field | Description | Validation |
|-------|-------------|------------|
| Asset ID | Unique identifier | Non-empty, unique |
| Asset Name | Display name | Non-empty |
| Asset Type | `Workstation`, `Server`, `Router`, `Switch`, `Application` | Must be one of list |
| IP Address | IPv4 | Valid IPv4 via `ipaddress` module |
| Operating System | e.g., Windows 11, Ubuntu | Optional (defaults to N/A) |
| Owner/Department | HR, IT, Network... | Non-empty |
| Risk Level | `Low`, `Medium`, `High`, `Critical` | Must be one of list |
| Security Status | `Secure`, `Warning`, `Vulnerable` | Must be one of list |

## 📁 Repository Structure
```
Week-01-Cyber-security-Asset-Inventory/
├── src/
│   └── asset_inventory.py
├── data/
│   └── assets.json
├── tests/
│   └── test_cases.md
├── screenshots/
│   ├── 01-add-asset.png
│   ├── 02-display-assets.png
│   ├── 03-search-asset.png
│   ├── 04-update-asset.png
│   ├── 05-delete-asset.png
│   ├── 06-security-summary.png
│   └── 07-input-validation.png
└── README.md
```

## 🚀 How to Run

### Prerequisites
- Python 3.8+

### Execution
```bash
# From repository root
python src/asset_inventory.py
```

You will see a menu:
```
========== CYBERSECURITY ASSET INVENTORY SYSTEM ==========
1. Add Asset
2. Add Multiple Assets (Batch)
3. Display All Assets
4. Search Asset
5. Update Asset
6. Delete Asset
7. Security Summary
8. Exit
==========================================================
```

### Sample Input – Batch Mode (Recommended to match spec)
```
Enter number of assets: 3

Asset 1
Asset ID: A101
Asset Name: HR-PC-01
Asset Type: Workstation
IP Address: 192.168.1.10
Operating System: Windows 11
Department: HR
Risk Level: Medium
Security Status: Secure
...
```
Choose option `2` to enter this flow. Option `1` adds one asset at a time.

### Display Output
Matches expected spec:
```
=========================================
 CYBERSECURITY ASSET INVENTORY
=========================================

Asset ID : A101
...
Total Assets : 3
Critical Assets : 1
High Risk Assets : 1
Medium Risk Assets : 1
Vulnerable Assets : 1
=========================================
```

## 🧪 Testing
See `tests/test_cases.md` for 12 manual test cases covering:
- Add / Display / Search / Update / Delete
- Validation for invalid IP, type, risk, status
- Duplicate ID handling
- Security summary & batch add

## 🖼️ Screenshots
Placeholders in `screenshots/` – capture each operation:
1. `01-add-asset.png` – Adding an asset
2. `02-display-assets.png` – Display view
3. `03-search-asset.png` – Searching
4. `04-update-asset.png` – Updating
5. `05-delete-asset.png` – Deleting
6. `06-security-summary.png` – Security summary
7. `07-input-validation.png` – Invalid input handling

To generate: Run the app and screenshot each menu choice.

## 🔒 Validation Logic
- **Asset Type/Risk/Status**: Case-insensitive but stored normalized (Title Case); invalid values re-prompt with allowed list.
- **IP**: Validated via `ipaddress.IPv4Address`; rejects `999.999.999.999` etc.
- **Duplicate ID**: Blocked with message `already exists`.

## 🔮 Future Enhancements
- Export to CSV/PDF
- Role-based authentication
- Vulnerability scanner integration
- Web dashboard (Flask/Django)
- Audit log

## 👤 Author
Week 01 Mini Project – Cybersecurity Asset Inventory System

## 📄 License
Educational use.
"# UTHRA-VK-111923CB01059" 
