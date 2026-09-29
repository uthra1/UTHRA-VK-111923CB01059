# Test Cases – Cybersecurity Asset Inventory System

## Overview
Manual test cases for verifying CRUD operations, input validation, and security summary.

### Test Case 1: Add Asset – Valid Input
| Field | Details |
|-------|---------|
| **Test ID** | TC-01 |
| **Scenario** | Add a new asset with all valid fields |
| **Steps** | 1. Run `python src/asset_inventory.py` <br>2. Choose `1. Add Asset` <br>3. Enter: A104, Finance-PC-01, Workstation, 192.168.1.30, Windows 11, Finance, Low, Secure |
| **Expected** | `Asset 'A104' added successfully!` and appears in `data/assets.json` |
| **Status** | Pass |

### Test Case 2: Display Assets – Expected Output Format
| Field | Details |
|-------|---------|
| **Test ID** | TC-02 |
| **Scenario** | Display all assets and verify formatting |
| **Steps** | 1. Choose `3. Display All Assets` |
| **Expected** | Header `CYBERSECURITY ASSET INVENTORY`, separators `-----------------------------------------`, and summary:<br>`Total Assets : 3`<br>`Critical Assets : 1`<br>`High Risk Assets : 1`<br>`Medium Risk Assets : 1`<br>`Vulnerable Assets : 1` |
| **Status** | Pass |

### Test Case 3: Search Asset – Found
| Field | Details |
|-------|---------|
| **Test ID** | TC-03 |
| **Scenario** | Search by Asset ID `A102` |
| **Steps** | 1. Choose `4. Search Asset` <br>2. Enter `A102` |
| **Expected** | Displays `Web-Server`, `Server`, `192.168.1.20`, `Critical`, `Vulnerable` |
| **Status** | Pass |

### Test Case 4: Search Asset – Not Found
| Field | Details |
|-------|---------|
| **Test ID** | TC-04 |
| **Scenario** | Search non-existent ID |
| **Steps** | 1. Choose `4. Search Asset` <br>2. Enter `A999` |
| **Expected** | `[!] No asset found matching 'A999'.` |
| **Status** | Pass |

### Test Case 5: Update Asset
| Field | Details |
|-------|---------|
| **Test ID** | TC-05 |
| **Scenario** | Update existing asset `A101` Risk Level from Medium to High |
| **Steps** | 1. Choose `5. Update Asset` <br>2. Enter `A101` <br>3. Leave others blank, enter `High` for Risk Level |
| **Expected** | `Asset 'A101' updated successfully!` and `risk_level` is `High` in JSON/display |
| **Status** | Pass |

### Test Case 6: Delete Asset
| Field | Details |
|-------|---------|
| **Test ID** | TC-06 |
| **Scenario** | Delete asset `A103` |
| **Steps** | 1. Choose `6. Delete Asset` <br>2. Enter `A103` <br>3. Confirm `y` |
| **Expected** | `Asset 'A103' deleted successfully. Remaining: 2` and asset removed from JSON |
| **Status** | Pass |

### Test Case 7: Input Validation – Invalid Asset Type
| Field | Details |
|-------|---------|
| **Test ID** | TC-07 |
| **Scenario** | Try to add asset with invalid type `Laptop` |
| **Steps** | 1. Choose `1. Add Asset` <br>2. Enter `Laptop` for Asset Type |
| **Expected** | `[!] Invalid value. Allowed: Workstation, Server, Router, Switch, Application` and re-prompt |
| **Status** | Pass |

### Test Case 8: Input Validation – Invalid IP Address
| Field | Details |
|-------|---------|
| **Test ID** | TC-08 |
| **Scenario** | Try to add asset with invalid IP `999.999.999.999` |
| **Steps** | 1. Enter `999.999.999.999` for IP Address |
| **Expected** | `[!] Invalid IP address...` and re-prompt until valid like `192.168.1.10` |
| **Status** | Pass |

### Test Case 9: Input Validation – Invalid Risk Level & Status
| Field | Details |
|-------|---------|
| **Test ID** | TC-09 |
| **Scenario** | Enter `Extreme` for Risk, `Safe` for Status |
| **Expected** | Re-prompt with allowed lists `Low, Medium, High, Critical` and `Secure, Warning, Vulnerable` |
| **Status** | Pass |

### Test Case 10: Security Summary
| Field | Details |
|-------|---------|
| **Test ID** | TC-10 |
| **Scenario** | Verify security summary counts |
| **Steps** | 1. Choose `7. Security Summary` |
| **Expected** | Shows counts by Risk/Status/Type and flags `Critical & Vulnerable` assets for immediate attention |
| **Status** | Pass |

### Test Case 11: Duplicate Asset ID
| Field | Details |
|-------|---------|
| **Test ID** | TC-11 |
| **Scenario** | Add asset with existing ID `A101` |
| **Expected** | `[!] Asset ID 'A101' already exists. Aborting.` and no duplicate created |
| **Status** | Pass |

### Test Case 12: Batch Add (Sample Input)
| Field | Details |
|-------|---------|
| **Test ID** | TC-12 |
| **Scenario** | Batch add 3 sample assets (A101-A103) from empty JSON |
| **Steps** | 1. Clear `assets.json` to `[]` <br>2. Choose `2. Add Multiple Assets (Batch)` <br>3. Enter `3` and fill each asset as per SAMPLE INPUT |
| **Expected** | All 3 added and display matches Expected Output in spec exactly |
| **Status** | Pass |

---
**Execution Environment:** Windows 11, Python 3.10+, PowerShell 5.1
**Date:** 2026-09-23
