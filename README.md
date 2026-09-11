# SAP Business One (SAP B1) Enterprise Simulation & Supply Chain Architecture

A complete, self-contained SQLite simulation of the **SAP Business One (SAP B1)** enterprise schema, featuring **82 standard ERP tables**, realistic transactional records, dual-database inventory valuation models (`new_b1.db` vs `old_b1.db`), and the complete **Product Supply and Distribution Network Process Hierarchy (31 Process Variants across 6 Node Groups)**.

---

## 📑 Enterprise Documentation Directory

| Document | Description | Format / Path |
| :--- | :--- | :--- |
| 🗺️ **Process Hierarchy Map** | 5-Level Process Classification Framework (PCF), Routing Matrix, & 31 Master Processes | [**`Process_Hierarchy_Map.md`**](file:///Users/billy/SAPB1_Sim/Process_Hierarchy_Map.md) |
| 📋 **Version Control & Changelog** | Release history, versioning governance (v1.0.0 – v2.4.0), and git commit audit | [**`Version_Control.md`**](file:///Users/billy/SAPB1_Sim/Version_Control.md) |
| 🗄️ **Database Schema Reference** | Entity-Relationship Diagrams (ERD), Table Catalog (82 tables), and G/L triggers | [**`Schema.md`**](file:///Users/billy/SAPB1_Sim/Schema.md) |
| 🚢 **Intercompany Process Design** | Multi-currency mechanics, two-stage landed costing, and SIT accounting | [**`ICC_Process_Design.md`**](file:///Users/billy/SAPB1_Sim/ICC_Process_Design.md) |
| 📑 **Process Matrix (Word)** | Formal Enterprise Process Specification Document | [**`SAP_B1_Process_Design_Matrix.docx`**](file:///Users/billy/SAPB1_Sim/SAP_B1_Process_Design_Matrix.docx) |
| 📊 **Process Matrix (Excel)** | Complete 4-Tab Color-Coded Process Workbook (Policies, RACI, 31 Routes) | [**`SAP_B1_Process_Design_Matrix.xlsx`**](file:///Users/billy/SAPB1_Sim/SAP_B1_Process_Design_Matrix.xlsx) |

---

## 🗺️ Product Supply & Distribution Network Process Hierarchy Register
*(Directory of 6 Node Groups and 31 Level 3 Supply Network Routes & Control Workflow Groups — Last Updated 20260905 BL)*

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              5-LEVEL PROCESS ARCHITECTURE HIERARCHY                                    │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 1: Enterprise Value Stream (End-to-End Enterprise Chain)                                         │
│   └── E2E-P2F: Global Factory Procurement to Customer Order Fulfillment                               │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 2: Supply Network Node Groups & Operational Domains (6 Node Groups)                              │
│   ├── 2.1 [SNG-AU-ONLY]: old_b1.db Only (AU Domestic DC Network - 3 Routes)                            │
│   ├── 2.2 [SNG-HYBRID]: old_b1.db + new_b1.db (Cross-System Intercompany & Trans-Tasman - 11 Routes)   │
│   ├── 2.3 [SNG-NEW-ONLY]: new_b1.db Only (International Multi-Leg, NZ, UK & D2C Network - 9 Routes)    │
│   ├── 2.4 [SNG-EXCEPTION]: Exception Processes (PO Reroutes & Container Discrepancies - 3 Routes)      │
│   ├── 2.5 [SNG-RECONCILIATION]: Reconciliation Processes (Financial & Landed Cost Audit - 3 Routes)   │
│   └── 2.6 [MD-MAINTENANCE]: Master Data Maintenance (Item & Business Partner Governance - 2 Routes)    │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 3: Supply Network Route Groups & Lifecycle Control Processes (31 Master Processes)              │
│   └── Discrete route lifecycles (2.1.1 to 2.6.2) governing logistics, valuation, and fulfillment.     │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 4: Procedural Steps per Process (Sequential Procedural Milestones)                               │
│   └── Standard Formula: "[Step]: [Role] Action Document (DocType) @ Loc -> [Milestone/Outcome]"       │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEVEL 5: Transaction Artifacts, System Tables & GL Journal Postings                                    │
│   └── OPOR/POR1, OPDN/PDN1, OIPF/IPF1/IPF2, OWTR/WTR1, ORDR/RDR1, OINV/INV1, OJDT/JDT1, OINM          │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Master Supply Network Routing & Valuation Register (31 Process Variants)

| Level 2 Process Group | Level 3 Code | Process Pathway & Title | Operating DBs | Origin Node | Transit Node | Destination Node | Primary Valuation & Costing Mechanism |
| :--- | :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| **GROUP 2.1: old_b1.db ONLY (AU DOMESTIC DC NETWORK) — 3 Route Process Variants** | | | | | | | |
| `2.1 [SNG-AU-ONLY]` | **`2.1.1`** | **Factory → AU Warehouse → AU Consumer** | `old_b1.db` | Factory | Direct B/L | `AU Warehouses` | Two-Stage Destination Landed Cost (`OIPF 'E'` Accrual + `'A'` Overwrite). |
| `2.1 [SNG-AU-ONLY]` | **`2.1.2`** | **Factory → AU Warehouse → NZ Consumer** | `old_b1.db` | Factory | Direct Freight | `AU Warehouses` | Two-Stage AU Inward Landed Cost + Cross-Border Direct Invoicing. |
| `2.1 [SNG-AU-ONLY]` | **`2.1.3`** | **Factory → AU Warehouse → EuropeMarketPlace** | `old_b1.db` | Factory | Export Transit | `EuropeMarketPlace (EuropeMarketPlace)` | Two-Stage AU Inward Landed Cost + Long-Haul UK Freight Stack. |
| **GROUP 2.2: HYBRID DBs (CROSS-SYSTEM INTERCOMPANY & TRANS-TASMAN RELAY) — 11 Route Process Variants** | | | | | | | |
| `2.2 [SNG-HYBRID]` | **`2.2.1`** | **Factory → ICC → AU Warehouse → AU Consumer** | `new_b1 + old_b1` | `ICCChina` | `ICCSIT` | `AU Warehouses` | Two-Stage Stacked Cost (Origin LC + Dest LC Overwrite). |
| `2.2 [SNG-HYBRID]` | **`2.2.2`** | **Factory → ICC → AU Warehouse → NZ Consumer** | `new_b1 + old_b1` | `ICCChina` | `ICCSIT` | `AU Warehouses` | Two-Stage Stacked Cost at AU DC + Direct Export OINV. |
| `2.2 [SNG-HYBRID]` | **`2.2.3`** | **Factory → ICC → AU Whs → NZ Whs → NZ Consumer** | `new_b1 + old_b1` | `ICCChina` | `ICCSIT + NZSIT` | `NZNTH/NZSTH (NZ whs)` | Triple-Stacked Cost: Origin LC + AU Landed + NZ Landed. |
| `2.2 [SNG-HYBRID]` | **`2.2.4`** | **Factory → ICC → NZ Whs → AU Whs → AU Consumer** | `new_b1 + old_b1` | `ICCChina` | `ICCSIT + NZSIT` | `AU Warehouses` | Triple-Stacked Cost: Origin LC + NZ Landed + AU Landed. |
| `2.2 [SNG-HYBRID]` | **`2.2.5`** | **Factory → AU Warehouse → NZ Warehouse → NZ Consumer** | `new_b1 + old_b1` | `AU Warehouse` | `NZSIT` | `NZNTH/NZSTH (NZ whs)` | Direct AU Landed Cost + Trans-Tasman Relay at AU MWAG. |
| `2.2 [SNG-HYBRID]` | **`2.2.6`** | **Factory → NZ Warehouse → AU Warehouse → AU Consumer** | `new_b1 + old_b1` | `NZNTH` | `NZSIT` | `AU Warehouses` | Direct NZ Landed Cost + Trans-Tasman Relay at NZ MWAG. |
| `2.2 [SNG-HYBRID]` | **`2.2.7`** | **Factory → ICC → AU Warehouse → EuropeMarketPlace** | `new_b1 + old_b1` | `ICCChina` | `ICCSIT + EuropeSIT` | `EuropeMarketPlace (EuropeMarketPlace)` | Two-Stage Stacked at AU + Long-Haul UK Export Freight. |
| `2.2 [SNG-HYBRID]` | **`2.2.8`** | **Factory → AU Warehouse → NZ Warehouse → EuropeMarketPlace** | `new_b1 + old_b1` | `AU Warehouse` | `NZSIT + EuropeSIT` | `EuropeMarketPlace (EuropeMarketPlace)` | AU Landed + Trans-Tasman Relay + UK Re-Export Freight. |
| `2.2 [SNG-HYBRID]` | **`2.2.9`** | **Factory → NZ Warehouse → AU Warehouse → EuropeMarketPlace** | `new_b1 + old_b1` | `NZNTH` | `NZSIT + EuropeSIT` | `EuropeMarketPlace (EuropeMarketPlace)` | NZ Landed + Trans-Tasman Relay + UK Re-Export Freight. |
| `2.2 [SNG-HYBRID]` | **`2.2.10`**| **Factory → ICC → AU Whs → NZ Whs → EuropeMarketPlace** | `new_b1 + old_b1` | `ICCChina` | `ICCSIT+NZSIT+EuropeSIT`| `EuropeMarketPlace (EuropeMarketPlace)` | Multi-Leg Stacked Costing Across 3 Intercompany Entities. |
| `2.2 [SNG-HYBRID]` | **`2.2.11`**| **Factory → ICC → NZ Whs → AU Whs → EuropeMarketPlace** | `new_b1 + old_b1` | `ICCChina` | `ICCSIT+NZSIT+EuropeSIT`| `EuropeMarketPlace (EuropeMarketPlace)` | Multi-Leg Stacked Costing Across 3 Intercompany Entities. |
| **GROUP 2.3: new_b1.db ONLY (INTERNATIONAL MULTI-LEG, NZ, UK & D2C NETWORK) — 9 Route Process Variants** | | | | | | | |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.1`** | **Factory → NZ Warehouse → NZ Consumer** | `new_b1.db` | Factory | Direct B/L | `NZNTH/NZSTH (NZ whs)` | Two-Stage NZ Destination Landed Cost (`OIPF 'E'` Accrual + `'A'` Overwrite). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.2`** | **Factory → ICC → NZ Warehouse → NZ Consumer** | `new_b1.db` | `ICCChina` | `ICCSIT + NZSIT` | `NZNTH/NZSTH (NZ whs)` | Two-Stage Stacked Cost (`$424 + $522 + $545 AUD`). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.3`** | **Factory → EuropeMarketPlace** | `new_b1.db` | Factory | Direct Voyage | `EuropeMarketPlace (EuropeMarketPlace)` | Two-Stage UK Destination Landed Cost (`OIPF 'E'` Accrual + `'A'` Overwrite). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.4`** | **Factory → ICC → EuropeMarketPlace** | `new_b1.db` | `ICCChina` | `EuropeSIT` | `EuropeMarketPlace (EuropeMarketPlace)` | Two-Stage Stacked Cost (`$424 + $424 + $560 AUD`). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.5`** | **Factory → NZ Warehouse → EuropeMarketPlace** | `new_b1.db` | `NZNTH` | `EuropeSIT` | `EuropeMarketPlace (EuropeMarketPlace)` | NZ Inbound Landed Cost + UK Maritime Re-Export Freight. |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.6`** | **Factory → ICC → NZ Warehouse → EuropeMarketPlace** | `new_b1.db` | `ICCChina` | `ICCSIT + EuropeSIT` | `EuropeMarketPlace (EuropeMarketPlace)` | Two-Stage Stacked at NZ (`$522`) + UK Freight into EuropeMarketPlace (`$560 AUD`). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.7`** | **Factory → ICC → AU Consumer (D2C Air Express)** | `new_b1.db` | `ICCChina` | Air Courier | AU Consumer | Origin Staging & Drop-Ship Landed Cost (Direct Air Courier). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.8`** | **Factory → ICC → NZ Consumer (D2C Air Express)** | `new_b1.db` | `ICCChina` | Air Courier | NZ Consumer | Origin Staging & Drop-Ship Landed Cost (Direct Air Courier). |
| `2.3 [SNG-NEW-ONLY]`| **`2.3.9`** | **Factory → ICC → UK Consumer (D2C Air Express)** | `new_b1.db` | `ICCChina` | Air Courier | UK Consumer | Origin Staging & Drop-Ship Landed Cost (Direct Air Courier). |
| **GROUP 2.4: EXCEPTION PROCESSES (PO REROUTES & CONTAINER DISCREPANCIES) — 3 Process Variants** | | | | | | | |
| `2.4 [SNG-EXCEPTION]`| **`2.4.1`** | **PO Changes from ICC to AU Warehouse** | `new_b1 → old_b1` | `ICCChina` | Direct Port | `AU Warehouses` | Cancels `new_b1` PO; re-issues direct import PO in `old_b1.db`. |
| `2.4 [SNG-EXCEPTION]`| **`2.4.2`** | **PO Changes from AU Warehouse to ICC** | `old_b1 → new_b1` | `AU Warehouse` | `ICCSIT` | `ICCChina + AU` | Cancels `old_b1` PO; establishes multi-leg ICC PO in `new_b1.db`. |
| `2.4 [SNG-EXCEPTION]`| **`2.4.3`** | **Intercompany Transfer Quantity Over/Under-Supply** | `new_b1 + old_b1` | `ICCSIT` | Wharf / Port | Any warehouses | Resolves variance: partial GRPO, transit loss write-off, or surplus receipt. |
| **GROUP 2.5: RECONCILIATION PROCESSES (FINANCIAL & LANDED COST AUDIT) — 3 Process Variants** | | | | | | | |
| `2.5 [SNG-RECONCILIATION]`| **`2.5.1`** | **Inventory Valuation Reconciliation** | `new_b1 + old_b1` | All Hubs | In-Transit | Balance Sheet | Monthly audit: Warehouse subledger (`OITW`) vs G/L Control (`100010`/`100050`). |
| `2.5 [SNG-RECONCILIATION]`| **`2.5.2`** | **Landed Cost Entries Reconciliation** | `new_b1 + old_b1` | All Hubs | Accrual Clearing | `G/L 200050` | Reconciles Estimated (`OIPF 'E'`) vs Actual (`OIPF 'A'`) broker invoices to $0. |
| `2.5 [SNG-RECONCILIATION]`| **`2.5.3`** | **Group Report Reconciliation** | `new_b1 + old_b1` | All Hubs | Consolidated Ledgers | Group Financial Statements | Intercompany elimination, group inventory valuation consolidation, and multi-entity profit reporting. |
| **GROUP 2.6: MASTER DATA MAINTENANCE — 2 Process Variants** | | | | | | | |
| `2.6 [MD-MAINTENANCE]`| **`2.6.1`** | **SAP B1 Inventory Item Master Maintenance** | `new_b1 + old_b1` | Master Setup | Warehouse Bins | Item Master Records | Item Code creation, valuation method setup (`OITM` vs `OITW`), purchasing/sales UoM, and barcode cataloging. |
| `2.6 [MD-MAINTENANCE]`| **`2.6.2`** | **SAP B1 Business Partner Master Maintenance** | `new_b1 + old_b1` | Master Setup | Commercial Ledger | BP Master Records | Vendor/Customer setup (`OCRD`/`CRD1`), currency assignment (USD/AUD/NZD/GBP), payment terms (`OCTG`), and tax group mapping. |

---

## 🏛️ RACI Role Accountability & Document Segregation (Policy 9)

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              RACI GOVERNANCE & DOCUMENT OWNERSHIP                                      │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ • [Purchasing]:         OPOR (All Factory & Intercompany POs), OWTQ (All Transfer Requests)            │
│ • [Logistics]:          OPDN (GRPO), OWTR (Transfers), OIGE (Goods Issue),                             │
│                         OINV (Direct AR Invoice creation confirming physical order dispatch)           │
│ • [Finance]:            OIPF 'E'/'A' (Landed Costs), Revenue & COGS Accounting Review,                 │
│                         OJDT G/L Clearing Reconciliations (G/L 200050/100050/110020)                   │
│ • [Sales]:              ORDR (Customer Sales Orders & Inventory Reservation)                           │
│ • [Corporate Treasury]: ORCT (Customer Payment Settlement — Strictly Out of Operational Scope)         │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Architecture & Table Overview (82 Tables)

The simulation provides two full database instances:
1. [**`new_b1.db`**](file:///Users/billy/SAPB1_Sim/new_b1.db): Multi-Warehouse Moving Average Costing (`OITW.AvgPrice` per regional DC & SIT hub).
2. [**`old_b1.db`**](file:///Users/billy/SAPB1_Sim/old_b1.db): Company-Level Moving Average Valuation (`OITM.AvgPrice`).

### 12 Core Business Modules Covered:
1. **Master Data & Chart of Accounts**: `OACT`, `OWHS`, `OCRD`, `CRD1`, `OITM`, `OITW`
2. **Banking & Payments**: `OCTG`, `ODSC`, `ORCT`/`RCT2`, `OVPM`/`VPM2`
3. **Production & Manufacturing**: `OITT`/`ITT1`, `OWOR`/`WOR1`, `OIGN`/`IGN1`, `OIGE`/`IGE1`
4. **Pricing, Tax & Special Conditions**: `OPLN`, `ITM1`, `OSPP`/`SPP1`, `OSTC`
5. **Advanced Inventory**: `OBTN`, `OSRN`, `OITL`/`ITL1`, `OBIN`, `OINC`/`INC1`
6. **Purchasing & AP**: `OPRQ`/`PRQ1`, `OPQT`/`PQT1`, `OPOR`/`POR1`, `OPDN`/`PDN1`, `OPCH`/`PCH1`, `ORPC`/`RPC1`
7. **Sales & AR (Zero-ODLN)**: `OQUT`/`QUT1`, `ORDR`/`RDR1`, `ODLN`/`DLN1`, `OINV`/`INV1`, `ORDN`/`RDN1`, `ORIN`/`RIN1`
8. **CRM & Opportunities**: `OCPR`, `OCRG`, `OOPR`/`OPR1`, `OCLG`
9. **Cost Accounting & Budgets**: `ODIM`, `OPRC`, `OPMG`/`PMG1`, `OBGT`/`BGT1`
10. **Landed Costs**: `OALC`, `OIPF`/`IPF1`/`IPF2` (Provisional `'E'` and Actual `'A'`)
11. **Financial Ledgers**: `OJDT`/`JDT1`, `OITR`/`ITR1`
12. **Inventory Transfers & Audit Log**: `OWTQ`/`WTQ1`, `OWTR`/`WTR1`, `OINM`, `ADOC`/`ADT1`

---

## 🚀 Quick Start Guide

### 1. Launch Interactive Web App UI Simulator
```bash
python3 app.py
```
Open browser at **`http://localhost:5050`** to access:
- 📊 **Executive Cockpit**: KPI tiles for Revenue, Stock Valuation, AR/AP, and Backlog.
- 🏷️ **SAP Golden Arrows (➡️)**: Drill-down modals into Customer 360°, Item 360°, and Document Lines.
- 🕸️ **Document Relationship Map**: Interactive lifecycle flow from Quotations to Settlements.
- 📑 **Document Explorer**: Form viewer for Sales Orders, POs, Invoices, Deliveries, and Work Orders.
- 🛠️ **Live SQL Studio**: Query runner with schema browser across all 82 tables.

### 2. Re-seed or Reset Databases
```bash
python3 init_new_b1.py   # Multi-Warehouse Costing
python3 init_old_b1.py   # Company-Level Valuation
python3 compare_b1_dbs.py # Validate differences
```

### 3. Re-compile Process Matrix Documents
```bash
python3 generate_process_doc.py     # Compiles SAP_B1_Process_Design_Matrix.docx
python3 generate_process_sheets.py  # Compiles SAP_B1_Process_Design_Matrix.xlsx
```

---

## 🔒 Decision-Support Info Pack: Irreversible SAP Business One Database Configurations

When provisioning a fresh SAP Business One database, certain system settings become **permanently irreversible** upon database creation or as soon as the first financial transaction (`OJDT`), inventory movement (`OINM`), or master data record is posted. Making an incorrect decision during initialization often requires an entire database rebuild and full data migration.

The following decision-support matrix and detailed technical briefs outline the architectural impact, business implications, and recommendations for each irreversible setting.

---

### 1. Executive Summary & Configuration Decision Matrix

| Configuration Setting | Navigation Path | Irreversibility Level | Recommended Setting | Primary Decision Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **Chart of Account Template** | `Company Details > Basic Init` | **Strict (At Creation)** | **User-Defined** (or Local Standard) | Standardizes financial structure across entities; cannot change template after accounts are generated. |
| **Local Currency (LC)** | `Company Details > Basic Init` | **100% Absolute Lock** | **Entity Legal Currency** (`AUD`, `NZD`, `GBP`) | Must strictly match the statutory tax filing and statutory reporting currency of the legal entity. |
| **System Currency (SC)** | `Company Details > Basic Init` | **100% Absolute Lock** | **Consolidation Currency** (`USD` or `AUD`) | Enables parallel real-time dual-currency reporting and global corporate group financial consolidation. |
| **Credit Balance with Negative Sign** | `Company Details > Basic Init` | **High (Reporting Impact)** | **Checked (`Yes`)** | Mathematical standard for G/L reporting; ensures credit balances appear with negative `-` signs in trial balance. |
| **Use Segmentation Accounts** | `Company Details > Basic Init` | **100% Irreversible** | **UNCHECKED (`No`)** | Avoids massive G/L code combinatorial explosion; **Cost Accounting Multidimensions (`ODIM`)** is far superior. |
| **Permit >1 Doc Type per Series** | `Company Details > Basic Init` | **Irreversible once used** | **UNCHECKED (`No`)** | Preserves separate, audit-compliant, unbroken sequential numbering series per document type (`OINV`, `ORDR`, `OPDN`). |
| **Use Continuous Stock (Perpetual)** | `Company Details > Basic Init` | **100% Absolute Lock** | **CHECKED (`Yes`)** | **Mandatory** for real-time balance sheet inventory valuation, landed cost allocation (`OIPF`), and live COGS postings. |
| **Manage Cost per Warehouse** | `Company Details > Basic Init` | **100% Irreversible** | **CHECKED (`Yes` / StockByWhs='Y')** | **Mandatory** for multi-warehouse and intercompany supply chains to track localized landed costs per hub (`OITW.AvgPrice`). |
| **Purchase Accounts Posting System** | `Company Details > Basic Init` | **100% Irreversible** | **UNCHECKED (`No`)** | Required only for continental Europe legal accounting; standard Anglo-Saxon/AU/UK accounting uses GRPO clearing. |
| **Enable Fixed Assets** | `Company Details > Basic Init` | **Permanent Schema Embed** | **CHECKED (`Yes`)** | Embeds native fixed asset register, depreciation schedules (`ODPV`), and capitalization workflows inside SAP B1. |
| **Mask Credit Card Number** | `Company Details > Basic Init` | **Compliance Requirement** | **CHECKED (`Yes`)** | PCI-DSS data security compliance; permanently prevents raw credit card storage in clear text. |
| **Enable Multiple Branches** | `Company Details > Basic Init` | **100% Irreversible** | **Evaluate Entity Structure** | Unlocks multiple tax registrations / ABNs in a single DB; forces all documents to require a Branch ID (`BPLId`). |
| **Enable Approval Process** | `General Settings > BP` | **Audit Trailing Lock** | **CHECKED (`Yes`)** | Enables corporate governance, spend approval tiers, and credit limit exception workflows (`OWST`, `OWDD`). |
| **Exchange Rate Posting** | `General Settings > Display` | **Calculation Engine Lock** | **Direct (`1 FC = X LC`)** | Adopts regional standard quotation convention matching domestic central bank exchange rates. |
| **Decimal Places** | `General Settings > Display` | **Increase Only (No Decrease)** | **Price: 4, Qty: 2-3, Rate: 4-6, Amt: 2** | **Extreme Caution**: Decimal precision can never be decreased once saved. |
| **Use Multidimensions** | `General Settings > Cost Accounting` | **100% Irreversible** | **CHECKED (`Yes`)** | Enables up to 5 concurrent reporting dimensions (Cost Center, Sales Channel, Region, Project) without G/L bloat. |
| **Posting Periods Setup** | `System Init > Posting Period` | **Permanent First Period** | **12 Monthly Sub-Periods** | First fiscal year start and monthly sub-period structure cannot be modified after initial posting. |
| **Manage Freight in Documents** | `Document Settings > General` | **Permanent Doc Structure** | **CHECKED (`Yes`)** | Required for allocating freight revenue, transport charges, and courier surcharges (`OEXD`) on commercial documents. |
| **Master Data Deletion Immutability** | `Item & BP Master Data` | **Permanent Audit Retention** | **Enforce Strict Staging** | Records with transaction history (`OINM`/`OJDT`) cannot be deleted; must use "Inactive / Freeze" flags instead. |

---

### 2. Deep-Dive Technical Decision Support & Guidance

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                      SAP BUSINESS ONE INITIALIZATION ARCHITECTURE & DECISION PATH                      │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Legal Entity & Currency Foundation:  [Local Currency] ───► [System Currency] ───► [Branch Strategy] │
│ 2. Financial & Accounting Framework:    [COA Structure]  ───► [Dimensions ODIM] ───► [Posting Periods] │
│ 3. Inventory Valuation & Landed Cost:   [Perpetual Stock]───► [Manage by Whs]  ───► [Freight in Docs] │
│ 4. System Ergonomics & Precision:       [Decimals Lock]  ───► [Approval W/F]   ───► [Fixed Assets]     │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### A. Company Details & Basic Initialization

##### 1. Chart of Account Template
* **Technical Impact**: Dictates the primary structure of table `OACT` (Levels 1 to 5: Drawers, Title Accounts, and Active Postable Accounts).
* **Options**: Standard Predefined Localization (e.g. Australia Standard) vs. **User-Defined**.
* **Decision Guide**:
  * Select **User-Defined** if your enterprise operates a standardized corporate Chart of Accounts or consolidates reporting across multiple regional subsidiaries (AU, NZ, UK, Asia).
  * Select **Standard Localization** if you require out-of-the-box statutory tax reporting tailored to a single jurisdiction.
* **Warning**: You cannot swap or re-apply a different template once accounts are generated and transaction postings exist.

##### 2. Local Currency (LC) vs. System Currency (SC)
* **Local Currency (`LC`)**: The functional legal operating currency of the database (e.g. `AUD` for Australia, `NZD` for New Zealand, `GBP` for UK). All statutory tax returns (GST/BAS/VAT) are strictly generated in LC. **Cannot be altered once set.**
* **System Currency (`SC`)**: A parallel secondary currency in which SAP Business One calculates and stores every single journal line (`JDT1.SysCred`, `JDT1.SysDeb`).
* **Decision Guide**:
  * If corporate HQ reports in `USD`, configure **Local Currency = `AUD`** and **System Currency = `USD`**.
  * This provides automated, real-time balance sheet and P&L reporting in both currencies simultaneously without manual exchange rate conversion.

##### 3. Display Credit Balance with Negative Sign
* **Technical Impact**: Configures whether G/L credit balances (Liabilities, Equity, Revenue) are formatted with a negative `-` sign or positive values in trial balances and queries.
* **Decision Guide**: Enable (`Yes`). Modern financial practice and automated reporting pipelines rely on mathematical sign conventions (Debits = Positive, Credits = Negative) for net-sum reconciliation.

##### 4. Use Segmentation Accounts vs. Cost Accounting Dimensions
* **Technical Impact**: Splits G/L codes into rigid segments (e.g. `100010-01-002-05` = `Natural-Division-Department-Region`).
* **Decision Guide**: **DO NOT ENABLE Segmentation.**
  * *Why?* Account segmentation causes a combinatorial explosion of the Chart of Accounts (thousands of redundant G/L accounts).
  * *Superior Alternative*: Use **Cost Accounting Multidimensions (`ODIM` / `OPRC`)**. Multidimensions allow dynamic, matrix-based slice-and-dice reporting across 5 independent axes without adding a single extra G/L account.

##### 5. Permit More Than One Document Type per Series
* **Technical Impact**: Allows different document objects (e.g. Sales Invoices `OINV` and Delivery Notes `ODLN`) to share a unified sequential numbering sequence.
* **Decision Guide**: **Keep UNCHECKED (`No`).** Statutory audit standards in Australia, New Zealand, and the UK require discrete, unbroken, auditable numbering series per document category.

##### 6. Use Continuous Stock (Perpetual Inventory)
* **Technical Impact**: Controls whether inventory movements write real-time balancing double-entry transactions to the General Ledger (`OJDT`).
* **Decision Guide**: **MUST BE ENABLED (`Yes`).**
  * Essential for automated Landed Cost capitalization (`OIPF`), live COGS recognition upon Direct AR Invoicing (`OINV`), and real-time Balance Sheet stock asset valuation (`G/L 100010` / `100050`).
  * If left unchecked, the company is placed on periodic inventory, requiring manual month-end stock count adjustments. **This setting can NEVER be enabled later once non-perpetual transactions exist.**

##### 7. Manage Item Cost per Warehouse (`StockByWhs`)
* **Technical Impact**:
  * **`StockByWhs = 'Y'`**: Moving average cost / FIFO is calculated independently per warehouse (`OITW.AvgPrice`).
  * **`StockByWhs = 'N'`**: A single blended average cost is applied company-wide (`OITM.AvgPrice`); `OITW.AvgPrice` is forced to `0.0`.
* **Decision Guide**: **MUST BE ENABLED (`Yes`).**
  * Crucial for supply chain architectures featuring multiple regional hubs (e.g. Origin `ICCChina` at $424 AUD vs. Inbound DC `AU Warehouse` at $522 AUD vs. European DC `EuropeMarketPlace` at $560 AUD).
  * Prevents cross-warehouse inventory valuation distortion.

##### 8. Use Purchase Accounts Posting System
* **Technical Impact**: Routes vendor invoices through separate Purchase (`5xxxx`) and Purchase Return accounts.
* **Decision Guide**: **Keep UNCHECKED (`No`)** unless operating in specific continental European jurisdictions (e.g. France, Italy, Belgium, Spain). Anglo-Saxon accounting (AU, NZ, UK, US) utilizes standard GRPO Allocation / Landed Cost Clearing (`G/L 200030` / `200050`).

##### 9. Enable Fixed Assets
* **Technical Impact**: Activates the native Fixed Asset subledger (`OAAQ`, `OAFM`, `ODPV`), asset classes, depreciation areas, and fiscal depreciation run engines.
* **Decision Guide**: Enable (`Yes`) if managing capital assets, warehouse automation machinery, IT hardware, or facility improvements within SAP B1.

---

#### B. Multi-Branch Architecture (`Enable Multiple Branches`)

* **Technical Impact**: Alters the entire database schema to enforce a Branch ID (`BPLId`) foreign key across all documents (`ORDR`, `OPOR`, `OINV`), journal entries (`OJDT`), warehouse master records (`OWHS.BPLid`), and user authorizations.
* **Architectural Evaluation**:
  * **Single DB with Multi-Branch**:
    * *Pros*: Single login; unified Business Partner and Item Master data; consolidated reporting; simplified inter-branch transfers.
    * *Cons*: Shared Chart of Accounts structure; shared base currency; increased complexity in user data separation and branch clearing.
  * **Multiple Discrete Databases (e.g. `new_b1.db` vs `old_b1.db`)**:
    * *Pros*: 100% legal, currency, and fiscal separation; tailored Chart of Accounts and localized tax engines per country.
    * *Cons*: Requires master data synchronization across databases; intercompany trade executed via export/import or integration middleware.
* **Decision Guide**: Enable Multi-Branch if all operational entities share the same primary operating currency and accounting standards under one legal parent. If operating across distinct legal entities with different functional currencies (e.g. AU vs UK vs NZ), deploy separate localized databases with intercompany integration.

---

#### C. Display Settings & Decimal Precision Governance

* **Decimal Places Rule**: **DECIMALS CAN BE INCREASED AT ANY TIME, BUT CAN NEVER BE DECREASED.**
* **Recommended Enterprise Standard**:
  * **Prices**: Set to **`4` Decimals** (e.g. `$12.3450`). Critical for high-volume consumables, electronic components, freight rate brackets, and currency conversions where rounding at 2 decimals causes massive aggregate errors.
  * **Amounts**: Set to **`2` Decimals** (e.g. `$1,250.50`). Standard currency denomination.
  * **Quantities**: Set to **`2` or `3` Decimals** (e.g. `10.500 kg` or `1.00 EA`). Accommodates fractional UoM, weight, volume, or length measurements.
  * **Percentages**: Set to **`2` to `4` Decimals** (e.g. `10.00%` GST, `3.7525%` landed cost factor).
  * **Exchange Rates**: Set to **`4` or `6` Decimals** (e.g. `1 USD = 1.543210 AUD`). Mandatory for minimizing foreign exchange rounding variances.

---

#### D. Cost Accounting & Analytical Multidimensions

* **Technical Impact**: Unlocks table `ODIM` and provides up to 5 concurrent dimensions on every line of every transaction (`PRC1` through `PRC5`).
* **Recommended Dimension Framework**:
  * **Dimension 1 (`Cost Center`)**: Departmental OpEx (e.g. Logistics, Warehousing, Executive, Sales, IT).
  * **Dimension 2 (`Sales Channel`)**: Revenue Channels (e.g. Direct Consumer D2C, Wholesale B2B, Marketplace `EuropeMarketPlace`).
  * **Dimension 3 (`Geographic Region`)**: Physical distribution territory (e.g. Australia East, Australia West, New Zealand, Europe).
  * **Dimension 4 (`Product Category`)**: Business unit / product division (e.g. Robotics, AI Vision, Industrial Hardware).
  * **Dimension 5 (`Project / Initiative`)**: Capital expenditure, warehouse expansion, or strategic client projects.
* **Decision Guide**: **MUST BE ENABLED (`Yes`).** Delivers granular P&L reporting without restructuring the Chart of Accounts.

---

#### E. Posting Periods Setup & Fiscal Governance

* **Technical Impact**: Establishes the fundamental calendar against which all transactional date validations (`DocDate`, `TaxDate`, `DueDate`) operate.
* **Decision Guide**:
  * Define the correct **Financial Year Start Date** (e.g. `01/07/2026` for Australian fiscal year July–June, or `01/01/2026` for calendar year).
  * Select **Sub-Periods = Months** (producing 12 distinct postable period buckets `2026-01` through `2026-12`).
  * Never initialize a production database with `Sub-Periods = Year`, as financial period locking and month-end close controls cannot be retrofitted to past periods.

---

#### F. Master Data Lifecycle & Immutability Governance

* **Transaction Lock Rule**: Once a single document, opening balance, or journal entry is linked to an Item Code (`OITM`) or Business Partner (`OCRD`):
  * The record **CANNOT BE DELETED** from the database (maintains relational audit integrity for table `OINM`, `JDT1`).
  * The Item Valuation System (`OITM.EvalSystem` / `OITW.EvalSystem` Moving Average vs. FIFO vs. Standard) **CANNOT BE MODIFIED** if stock on hand exists.
  * Business Partner Category (`CardType` `'C'` Customer vs. `'S'` Vendor) is permanently frozen.
* **Pre-Go-Live Governance Checklist**:
  1. Audit and sanitize all legacy item catalogs before executing initial data migration.
  2. Enforce standardized coding conventions (`ITM-[GRP]-[SEQ]`, `V-[VENDOR]`, `C-[CUSTOMER]`).
  3. Validate Valuation Method (`Moving Average` vs `FIFO`) per item group prior to opening stock balance entry.
  4. For decommissioned products or inactive suppliers post-Go-Live, flag records as **`Inactive = 'Y'`** / **`Freeze`** rather than attempting deletion.

---
