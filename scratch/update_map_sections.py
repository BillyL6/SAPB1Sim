import re

file_path = "/Users/billy/SAPB1_Sim/Process_Hierarchy_Map.md"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Version
text = text.replace(
    "| **Document Version** | **2.3.0 (Exceptions & Financial Reconciliation Extensions)** |",
    "| **Document Version** | **2.4.0 (Master Data Maintenance & Group Reporting Extensions - 20260905 (BL))** |"
)

# 2. Update Section 1
old_sec1 = """├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 2: Supply Network Node Groups & Operational Domains                                              │
│   ├── 2.1 [SNG-AU-ONLY]: old_b1.db Only (Australian Domestic DC Network)                               │
│   ├── 2.2 [SNG-HYBRID]: old_b1.db + new_b1.db (Cross-System Intercompany & Trans-Tasman Relay)        │
│   ├── 2.3 [SNG-NEW-ONLY]: new_b1.db Only (International Multi-Leg, NZ, UK & D2C Network)              │
│   ├── 2.4 [SNG-EXCEPTION]: Exception Management & Routing Modification Workflows                       │
│   └── 2.5 [SNG-RECON]: Enterprise Financial & Landed Cost Reconciliation Workflows                     │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 3: Supply Network Route Groups & Lifecycle Control Processes (28 Master Processes)              │
│   ├── 2.1.1 - 2.1.3: Domestic AU & Direct Export Routes (old_b1.db)                                    │
│   ├── 2.2.1 - 2.2.11: Consolidated Trans-Tasman & Global Intercompany Routes (Hybrid DBs)              │
│   ├── 2.3.1 - 2.3.9: Direct & Consolidated NZ, UK Wayfair & D2C Drop-Ship Routes (new_b1.db)           │
│   ├── 2.4.1 - 2.4.3: PO Reroutes & Intercompany Transfer Quantity Discrepancies                        │
│   └── 2.5.1 - 2.5.2: Perpetual Inventory & Landed Cost G/L Clearing Reconciliations                   │"""

new_sec1 = """├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 2: Supply Network Node Groups & Operational Domains (6 Node Groups)                              │
│   ├── 2.1 [SNG-AU-ONLY]: old_b1.db Only (AU Domestic DC Network - 3 Routes)                            │
│   ├── 2.2 [SNG-HYBRID]: old_b1.db + new_b1.db (Cross-System Intercompany & Trans-Tasman - 11 Routes)   │
│   ├── 2.3 [SNG-NEW-ONLY]: new_b1.db Only (International Multi-Leg, NZ, UK & D2C Network - 9 Routes)    │
│   ├── 2.4 [SNG-EXCEPTION]: Exception Management & Routing Modification Workflows - 3 Routes            │
│   ├── 2.5 [SNG-RECONCILIATION]: Enterprise Financial & Landed Cost Reconciliation - 3 Routes           │
│   └── 2.6 [MD-MAINTENANCE]: SAP B1 Master Data Maintenance (Items & Business Partners) - 2 Routes      │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 3: Supply Network Route Groups & Lifecycle Control Processes (31 Master Processes)              │
│   ├── 2.1.1 - 2.1.3: Domestic AU & Direct Export Routes (old_b1.db)                                    │
│   ├── 2.2.1 - 2.2.11: Consolidated Trans-Tasman & Global Intercompany Routes (Hybrid DBs)              │
│   ├── 2.3.1 - 2.3.9: Direct & Consolidated NZ, UK Wayfair & D2C Drop-Ship Routes (new_b1.db)           │
│   ├── 2.4.1 - 2.4.3: PO Reroutes & Intercompany Transfer Quantity Discrepancies                        │
│   ├── 2.5.1 - 2.5.3: Perpetual Inventory, Landed Cost Clearing & Group Report Reconciliation          │
│   └── 2.6.1 - 2.6.2: SAP B1 Inventory Item & Business Partner Master Data Maintenance                 │"""

text = text.replace(old_sec1, new_sec1)

# 3. Update Master Table in Section 2 to match 20260905 Register exactly
old_table = """### Master Supply Network Routing & Control Matrix (28 Processes)

| Level 2 Domain | Level 3 Code | Process Pathway & Operational Title | System Warehouses | Operating Databases | Valuation & Governance Impact |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **`2.1` old_b1.db Only** | **`2.1.1`** | **Factory → AU Warehouse → AU Consumer** | Factory → `FDMSYD` → AU Consumer | `old_b1.db` | Single-Stage Destination Landed Cost (`OIPF` DocType 'A' in AUD). |
| *(AU Domestic DC)* | **`2.1.2`** | **Factory → AU Warehouse → NZ Consumer** | Factory → `FDMSYD` → NZ Consumer | `old_b1.db` | AU Inward Landed Cost + Cross-border export freight markup. |
| | **`2.1.3`** | **Factory → AU Warehouse → UK Wayfair** | Factory → `FDMSYD` → `UKWYF` | `old_b1.db` | AU Base Cost + International container freight to UK. |
| **`2.2` Hybrid DBs** | **`2.2.1`** | **Factory → ICC → AU Warehouse → AU Consumer** | Factory → `ICCNGB` → `FDMSYD` → AU Consumer | `new_b1` + `old_b1` | Two-Stage Stacked Cost: Origin LC at `ICCNGB` + Dest LC at AU DC. |
| *(Intercompany Relay)* | **`2.2.2`** | **Factory → ICC → AU Warehouse → NZ Consumer** | Factory → `ICCNGB` → `FDMSYD` → NZ Consumer | `new_b1` + `old_b1` | Stacked Cost at AU DC + Cross-border freight markup to NZ. |
| | **`2.2.3`** | **Factory → ICC → AU Whs → NZ Whs → NZ Consumer** | Factory → `ICCNGB` → `FDMSYD` → `NZNTH` → NZ | `new_b1` + `old_b1` | Triple-Stacked Cost: Origin LC + AU Landed + Trans-Tasman freight. |
| | **`2.2.4`** | **Factory → ICC → NZ Whs → AU Whs → AU Consumer** | Factory → `ICCNGB` → `NZNTH` → `FDMSYD` → AU | `new_b1` + `old_b1` | Triple-Stacked Cost: Origin LC + NZ Landed + Trans-Tasman freight. |
| | **`2.2.5`** | **Factory → AU Warehouse → NZ Warehouse → NZ Consumer** | Factory → `FDMSYD` → `NZNTH` → NZ Consumer | `new_b1` + `old_b1` | Direct AU Landed Cost + Trans-Tasman transfer at AU MWAG. |
| | **`2.2.6`** | **Factory → NZ Warehouse → AU Warehouse → AU Consumer** | Factory → `NZNTH` → `FDMSYD` → AU Consumer | `new_b1` + `old_b1` | Direct NZ Landed Cost + Trans-Tasman transfer at NZ MWAG. |
| | **`2.2.7`** | **Factory → ICC → AU Warehouse → UK Wayfair** | Factory → `ICCNGB` → `FDMSYD` → `UKWYF` | `new_b1` + `old_b1` | Two-Stage Stacked at AU + Long-haul re-export freight to UK. |
| | **`2.2.8`** | **Factory → AU Warehouse → NZ Warehouse → UK Wayfair** | Factory → `FDMSYD` → `NZNTH` → `UKWYF` | `new_b1` + `old_b1` | AU Landed + Trans-Tasman transfer + UK export freight. |
| | **`2.2.9`** | **Factory → NZ Warehouse → AU Warehouse → UK Wayfair** | Factory → `NZNTH` → `FDMSYD` → `UKWYF` | `new_b1` + `old_b1` | NZ Landed + Trans-Tasman transfer + UK export freight. |
| | **`2.2.10`**| **Factory → ICC → AU Whs → NZ Whs → UK Wayfair** | Factory → `ICCNGB` → `FDMSYD` → `NZNTH` → `UKWYF` | `new_b1` + `old_b1` | Multi-Leg Stacked Costing across 3 intercompany entities. |
| | **`2.2.11`**| **Factory → ICC → NZ Whs → AU Whs → UK Wayfair** | Factory → `ICCNGB` → `NZNTH` → `FDMSYD` → `UKWYF` | `new_b1` + `old_b1` | Multi-Leg Stacked Costing across 3 intercompany entities. |
| **`2.3` new_b1.db Only** | **`2.3.1`** | **Factory → NZ Warehouse → NZ Consumer** | Factory → `NZNTH` / `NZSTH` → NZ Consumer | `new_b1.db` | Direct NZ Landed Cost (`OIPF` DocType 'A' in AUD). |
| *(Int'l Multi-Leg)* | **`2.3.2`** | **Factory → ICC → NZ Warehouse → NZ Consumer** | Factory → `ICCNGB` → `NZNTH` / `NZSTH` → NZ | `new_b1.db` | Two-Stage Stacked Cost: `ICCNGB` ($424) → `NZNTH` ($522) → `NZSTH` ($545). |
| | **`2.3.3`** | **Factory → UK Wayfair** | Factory → `UKWYF` | `new_b1.db` | Direct UK Landed Cost (Felixstowe port duty + cartage into `UKWYF`). |
| | **`2.3.4`** | **Factory → ICC → UK Wayfair** | Factory → `ICCNGB` → `UKWYF` | `new_b1.db` | Two-Stage Stacked Cost: `ICCNGB` ($424) → `UKSIT` ($424) → `UKWYF` ($560). |
| | **`2.3.5`** | **Factory → NZ Warehouse → UK Wayfair** | Factory → `NZNTH` → `UKWYF` | `new_b1.db` | NZ Inbound Landed Cost + UK maritime re-export freight into `UKWYF`. |
| | **`2.3.6`** | **Factory → ICC → NZ Warehouse → UK Wayfair** | Factory → `ICCNGB` → `NZNTH` → `UKWYF` | `new_b1.db` | Two-Stage Stacked at NZ ($522) + UK maritime freight into `UKWYF` ($560). |
| | **`2.3.7`** | **Factory → ICC → AU Consumer (D2C Air Express)** | Factory → `ICCNGB` → AU Consumer | `new_b1.db` | Origin Staging & Drop-Ship Landed Cost (Direct air courier to AU). |
| | **`2.3.8`** | **Factory → ICC → NZ Consumer (D2C Air Express)** | Factory → `ICCNGB` → NZ Consumer | `new_b1.db` | Origin Staging & Drop-Ship Landed Cost (Direct air courier to NZ). |
| | **`2.3.9`** | **Factory → ICC → UK Consumer (D2C Air Express)** | Factory → `ICCNGB` → UK Consumer / Wayfair Drop | `new_b1.db` | Origin Staging & Drop-Ship Landed Cost (Direct air courier to UK). |
| **`2.4` Exceptions** | **`2.4.1`** | **PO Changes from ICC to AU Warehouse** | `ICCNGB` (`new_b1`) → `FDMSYD` (`old_b1`) | `new_b1` → `old_b1` | Cancels `new_b1` factory PO; re-issues direct import PO in `old_b1.db`. |
| *(Routing Changes)* | **`2.4.2`** | **PO Changes from AU Warehouse to ICC** | `FDMSYD` (`old_b1`) → `ICCNGB` (`new_b1`) | `old_b1` → `new_b1` | Cancels `old_b1` factory PO; establishes multi-leg ICC PO in `new_b1.db`. |
| | **`2.4.3`** | **Intercompany Transfer Quantity Over/Under-Supply** | `ICCSIT` → Destination DC (`FDMSYD`/`NZNTH`) | `new_b1` + `old_b1` | Resolves variance: partial GRPO, goods return (`ORPC`), or stock write-off. |
| **`2.5` Reconciliation** | **`2.5.1`** | **Inventory Valuation Reconciliation** | All Configured Warehouses (`OITW`/`OITM`) | `new_b1` + `old_b1` | Monthly audit: Warehouse subledger (`OITW`) vs G/L Control (`100010`/`100050`). |
| *(Financial Closing)* | **`2.5.2`** | **Landed Cost Entries Reconciliation** | Customs & Freight Clearing Accounts (`200050`) | `new_b1` + `old_b1` | Reconciles Estimated (`OIPF` 'E') vs Actual (`OIPF` 'A') broker invoices to $0. |"""

new_table = """### Master Supply Network Routing & Control Matrix (31 Process Variants — Last Updated 20260905 BL)

| Level 2 Process Group | Level 3 Code | Process Pathway & Title | Operating DBs | Origin Node | Transit Node | Destination Node | Primary Valuation & Costing Mechanism |
| :--- | :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| **GROUP 2.1: old_b1.db ONLY (AU DOMESTIC DC NETWORK) — 3 Route Process Variants** | | | | | | | |
| `2.1 [SNG-AU-ONLY]` | **`2.1.1`** | **Factory → AU Warehouse → AU Consumer** | `old_b1.db` | Factory | Direct B/L | `FDM/BDL/MF (AU whs)` | Two-Stage Destination Landed Cost (`OIPF 'E'` Accrual + `'A'` Overwrite). |
| `2.1 [SNG-AU-ONLY]` | **`2.1.2`** | **Factory → AU Warehouse → NZ Consumer** | `old_b1.db` | Factory | Direct Freight | `FDM/BDL/MF (AU whs)` | Two-Stage AU Inward Landed Cost + Cross-Border Direct Invoicing. |
| `2.1 [SNG-AU-ONLY]` | **`2.1.3`** | **Factory → AU Warehouse → UK Wayfair** | `old_b1.db` | Factory | Export Transit | `UKWYF (UK virtual whs)` | Two-Stage AU Inward Landed Cost + Long-Haul UK Freight Stack. |
| **GROUP 2.2: HYBRID DBs (CROSS-SYSTEM INTERCOMPANY & TRANS-TASMAN RELAY) — 11 Route Process Variants** | | | | | | | |
| `2.2 [SNG-HYBRID]` | **`2.2.1`** | **Factory → ICC → AU Warehouse → AU Consumer** | `new_b1 + old_b1` | `ICCNGB` | `ICCSIT` | `FDM/BDL/MF (AU whs)` | Two-Stage Stacked Cost (Origin LC + Dest LC Overwrite). |
| `2.2 [SNG-HYBRID]` | **`2.2.2`** | **Factory → ICC → AU Warehouse → NZ Consumer** | `new_b1 + old_b1` | `ICCNGB` | `ICCSIT` | `FDM/BDL/MF (AU whs)` | Two-Stage Stacked Cost at AU DC + Direct Export OINV. |
| `2.2 [SNG-HYBRID]` | **`2.2.3`** | **Factory → ICC → AU Whs → NZ Whs → NZ Consumer** | `new_b1 + old_b1` | `ICCNGB` | `ICCSIT + NZSIT` | `NZNTH/NZSTH (NZ whs)` | Triple-Stacked Cost: Origin LC + AU Landed + NZ Landed. |
| `2.2 [SNG-HYBRID]` | **`2.2.4`** | **Factory → ICC → NZ Whs → AU Whs → AU Consumer** | `new_b1 + old_b1` | `ICCNGB` | `ICCSIT + NZSIT` | `FDM/BDL/MF (AU whs)` | Triple-Stacked Cost: Origin LC + NZ Landed + AU Landed. |
| `2.2 [SNG-HYBRID]` | **`2.2.5`** | **Factory → AU Warehouse → NZ Warehouse → NZ Consumer** | `new_b1 + old_b1` | `FDMSYD` | `NZSIT` | `NZNTH/NZSTH (NZ whs)` | Direct AU Landed Cost + Trans-Tasman Relay at AU MWAG. |
| `2.2 [SNG-HYBRID]` | **`2.2.6`** | **Factory → NZ Warehouse → AU Warehouse → AU Consumer** | `new_b1 + old_b1` | `NZNTH` | `NZSIT` | `FDM/BDL/MF (AU whs)` | Direct NZ Landed Cost + Trans-Tasman Relay at NZ MWAG. |
| `2.2 [SNG-HYBRID]` | **`2.2.7`** | **Factory → ICC → AU Warehouse → UK Wayfair** | `new_b1 + old_b1` | `ICCNGB` | `ICCSIT + UKSIT` | `UKWYF (UK virtual whs)` | Two-Stage Stacked at AU + Long-Haul UK Export Freight. |
| `2.2 [SNG-HYBRID]` | **`2.2.8`** | **Factory → AU Warehouse → NZ Warehouse → UK Wayfair** | `new_b1 + old_b1` | `FDMSYD` | `NZSIT + UKSIT` | `UKWYF (UK virtual whs)` | AU Landed + Trans-Tasman Relay + UK Re-Export Freight. |
| `2.2 [SNG-HYBRID]` | **`2.2.9`** | **Factory → NZ Warehouse → AU Warehouse → UK Wayfair** | `new_b1 + old_b1` | `NZNTH` | `NZSIT + UKSIT` | `UKWYF (UK virtual whs)` | NZ Landed + Trans-Tasman Relay + UK Re-Export Freight. |
| `2.2 [SNG-HYBRID]` | **`2.2.10`**| **Factory → ICC → AU Whs → NZ Whs → UK Wayfair** | `new_b1 + old_b1` | `ICCNGB` | `ICCSIT+NZSIT+UKSIT` | `UKWYF (UK virtual whs)` | Multi-Leg Stacked Costing Across 3 Intercompany Entities. |
| `2.2 [SNG-HYBRID]` | **`2.2.11`**| **Factory → ICC → NZ Whs → AU Whs → UK Wayfair** | `new_b1 + old_b1` | `ICCNGB` | `ICCSIT+NZSIT+UKSIT` | `UKWYF (UK virtual whs)` | Multi-Leg Stacked Costing Across 3 Intercompany Entities. |
| **GROUP 2.3: new_b1.db ONLY (INTERNATIONAL MULTI-LEG, NZ, UK & D2C NETWORK) — 9 Route Process Variants** | | | | | | | |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.1`** | **Factory → NZ Warehouse → NZ Consumer** | `new_b1.db` | Factory | Direct B/L | `NZNTH/NZSTH (NZ whs)` | Two-Stage NZ Destination Landed Cost (`OIPF 'E'` Accrual + `'A'` Overwrite). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.2`** | **Factory → ICC → NZ Warehouse → NZ Consumer** | `new_b1.db` | `ICCNGB` | `ICCSIT + NZSIT` | `NZNTH/NZSTH (NZ whs)` | Two-Stage Stacked Cost (`$424 + $522 + $545 AUD`). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.3`** | **Factory → UK Wayfair** | `new_b1.db` | Factory | Direct Voyage | `UKWYF (UK virtual whs)` | Two-Stage UK Destination Landed Cost (`OIPF 'E'` Accrual + `'A'` Overwrite). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.4`** | **Factory → ICC → UK Wayfair** | `new_b1.db` | `ICCNGB` | `UKSIT` | `UKWYF (UK virtual whs)` | Two-Stage Stacked Cost (`$424 + $424 + $560 AUD`). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.5`** | **Factory → NZ Warehouse → UK Wayfair** | `new_b1.db` | `NZNTH` | `UKSIT` | `UKWYF (UK virtual whs)` | NZ Inbound Landed Cost + UK Maritime Re-Export Freight. |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.6`** | **Factory → ICC → NZ Warehouse → UK Wayfair** | `new_b1.db` | `ICCNGB` | `ICCSIT + UKSIT` | `UKWYF (UK virtual whs)` | Two-Stage Stacked at NZ (`$522`) + UK Freight into UKWYF (`$560 AUD`). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.7`** | **Factory → ICC → AU Consumer (D2C Air Express)** | `new_b1.db` | `ICCNGB` | Air Courier | AU Consumer | Origin Staging & Drop-Ship Landed Cost (Direct Air Courier). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.8`** | **Factory → ICC → NZ Consumer (D2C Air Express)** | `new_b1.db` | `ICCNGB` | Air Courier | NZ Consumer | Origin Staging & Drop-Ship Landed Cost (Direct Air Courier). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.9`** | **Factory → ICC → UK Consumer (D2C Air Express)** | `new_b1.db` | `ICCNGB` | Air Courier | UK Consumer | Origin Staging & Drop-Ship Landed Cost (Direct Air Courier). |
| **GROUP 2.4: EXCEPTION PROCESSES (PO REROUTES & CONTAINER DISCREPANCIES) — 3 Process Variants** | | | | | | | |
| `2.4 [SNG-EXCEPTION]`| **`2.4.1`** | **PO Changes from ICC to AU Warehouse** | `new_b1 → old_b1` | `ICCNGB` | Direct Port | `FDM/BDL/MF (AU whs)` | Cancels `new_b1` PO; re-issues direct import PO in `old_b1.db`. |
| `2.4 [SNG-EXCEPTION]`| **`2.4.2`** | **PO Changes from AU Warehouse to ICC** | `old_b1 → new_b1` | `FDMSYD` | `ICCSIT` | `ICCNGB + AU` | Cancels `old_b1` PO; establishes multi-leg ICC PO in `new_b1.db`. |
| `2.4 [SNG-EXCEPTION]`| **`2.4.3`** | **Intercompany Transfer Quantity Over/Under-Supply** | `new_b1 + old_b1` | `ICCSIT` | Wharf / Port | Any warehouses | Resolves variance: partial GRPO, transit loss write-off, or surplus receipt. |
| **GROUP 2.5: RECONCILIATION PROCESSES (FINANCIAL & LANDED COST AUDIT) — 3 Process Variants** | | | | | | | |
| `2.5 [SNG-RECONCILIATION]`| **`2.5.1`** | **Inventory Valuation Reconciliation** | `new_b1 + old_b1` | All Hubs | In-Transit | Balance Sheet | Monthly audit: Warehouse subledger (`OITW`) vs G/L Control (`100010`/`100050`). |
| `2.5 [SNG-RECONCILIATION]`| **`2.5.2`** | **Landed Cost Entries Reconciliation** | `new_b1 + old_b1` | All Hubs | Accrual Clearing | `G/L 200050` | Reconciles Estimated (`OIPF 'E'`) vs Actual (`OIPF 'A'`) broker invoices to $0. |
| `2.5 [SNG-RECONCILIATION]`| **`2.5.3`** | **Group Report Reconciliation** | `new_b1 + old_b1` | All Hubs | Consolidated Ledgers | Group Financial Statements | Intercompany elimination, group inventory valuation consolidation, and multi-entity profit reporting. |
| **GROUP 2.6: MASTER DATA MAINTENANCE — 2 Process Variants** | | | | | | | |
| `2.6 [MD-MAINTENANCE]`| **`2.6.1`** | **SAP B1 Inventory Item Master Maintenance** | `new_b1 + old_b1` | Master Setup | Warehouse Bins | Item Master Records | Item Code creation, valuation method setup (`OITM` vs `OITW`), purchasing/sales UoM, and barcode cataloging. |
| `2.6 [MD-MAINTENANCE]`| **`2.6.2`** | **SAP B1 Business Partner Master Maintenance** | `new_b1 + old_b1` | Master Setup | Commercial Ledger | BP Master Records | Vendor/Customer setup (`OCRD`/`CRD1`), currency assignment (USD/AUD/NZD/GBP), payment terms (`OCTG`), and tax group mapping. |"""

text = text.replace(old_table, new_table)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully updated Process_Hierarchy_Map.md to 31 processes across 6 Groups!")
