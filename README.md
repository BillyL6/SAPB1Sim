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
