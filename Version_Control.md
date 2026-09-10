# SAP Business One Enterprise Architecture — Version Control Reference (`Version_Control.md`)
## Release Changelog, Process Governance Evolution & Version History

---

| Governance Attribute | Specification |
| :--- | :--- |
| **Document Code** | **`E2E-P2F-VCR`** |
| **System Standard** | **Semantic Versioning for Process Architecture (SemVer 2.0.0 Adapted)** |
| **Current Active Release** | **`v2.4.0` (Master Data Maintenance & Group Reporting Reconciliation — 20260905 BL)** |
| **Total Process Scope** | **6 Node Groups / Domains (`2.1` – `2.6`) & 31 Level 3 Process Variants** |
| **Operating Databases** | [**`new_b1.db`**](file:///Users/billy/SAPB1_Sim/new_b1.db) *(Multi-Warehouse Costing)* & [**`old_b1.db`**](file:///Users/billy/SAPB1_Sim/old_b1.db) *(Company-Level Valuation)* |

---

## 1. Versioning Philosophy & Change Governance Standard

The enterprise process architecture evolves under strict semantic versioning guidelines:
* **MAJOR (`X.0.0`)**: Architectural changes, introduction of new ERP database engines, or fundamental shifts in inventory valuation standards.
* **MINOR (`x.Y.0`)**: Addition of new Level 2 Node Groups, Level 3 Process Variants, or enterprise policy amendments (e.g. RACI updates, Zero-ODLN policy).
* **PATCH (`x.y.Z`)**: Field refinements, G/L account mapping corrections, formatting updates, and procedural step metadata enhancements.

---

## 2. Comprehensive Version Release History

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               ENTERPRISE ARCHITECTURE RELEASE TIMELINE                                 │
├──────────────┬────────────┬────────────────────────────────────────────────────────────────────────────┤
│ Version      │ Date       │ Core Architectural Milestone & Scope                                       │
├──────────────┼────────────┼────────────────────────────────────────────────────────────────────────────┤
│ v2.4.0       │ 2026-09-05 │ • Added Group 2.6: Master Data Maintenance (2.6.1 Item & 2.6.2 BP Setup).   │
│ (CURRENT)    │ (BL Rev)   │ • Added Group 2.5.3: Group Report Reconciliation (Consolidation & Elim).   │
│              │            │ • Expanded master topology to 6 Node Groups & 31 Level 3 Process Variants. │
├──────────────┼────────────┼────────────────────────────────────────────────────────────────────────────┤
│ v2.3.0       │ 2026-09-05 │ • Formalized Group 2.4 Exception Management (2.4.1 - 2.4.3 PO Reroutes).   │
│              │            │ • Added Group 2.5 Financial Landed Cost Reconciliation (2.5.1 - 2.5.2).    │
│              │            │ • Established 28 Master Level 3 Processes across 5 Node Groups.            │
├──────────────┼────────────┼────────────────────────────────────────────────────────────────────────────┤
│ v2.2.0       │ 2026-09-04 │ • RACI Policy 9 Alignment: Assigned Direct AR Invoicing (OINV) to         │
│              │            │   [Logistics] as order dispatch confirmation mechanism.                    │
│              │            │ • Enforced Zero-ODLN universal direct invoicing across all 28 routes.      │
├──────────────┼────────────┼────────────────────────────────────────────────────────────────────────────┤
│ v2.1.0       │ 2026-09-04 │ • Benchmark Standard 2.2.2: Standardized semantic naming taxonomy:         │
│              │            │   "[Step Code]: [Role] Action Document (DocType) @ Loc -> [Milestone]".   │
│              │            │ • Rewrote all Level 4 procedural steps to standard 12-step model.          │
├──────────────┼────────────┼────────────────────────────────────────────────────────────────────────────┤
│ v2.0.0       │ 2026-09-01 │ • Established 5-Level Process Classification Framework (PCF).              │
│              │            │ • Implemented Dual-Database Simulation (new_b1.db vs old_b1.db).           │
│              │            │ • Multi-Leg In-Transit (SIT) & Two-Stage Landed Cost Architecture (OIPF).  │
├──────────────┼────────────┼────────────────────────────────────────────────────────────────────────────┤
│ v1.0.0       │ 2026-08-15 │ • Initial baseline SQLite simulation of SAP Business One 82 ERP tables.    │
└──────────────┴────────────┴────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Release Changelogs

### Release `v2.4.0` — Master Data Governance & Group Financial Reporting
* **Release Date**: 2026-09-05 (Baseline Update `20260905 (BL)`)
* **Key Enhancements**:
  1. **New Level 2 Group `2.6` [MD-MAINTENANCE]**:
     * **`2.6.1`**: *SAP B1 Inventory Item Master Maintenance* (`OITM`, `OITW`, `ITM1`, `OWHS`, `OBIN`). Configures item codes, unit of measures, valuation methods (`OITM` vs `OITW.AvgPrice`), and warehouse bin thresholds.
     * **`2.6.2`**: *SAP B1 Business Partner Master Maintenance* (`OCRD`, `CRD1`, `OCPR`, `OCTG`, `OSTC`). Configures customer/vendor codes, multi-currency locks (USD/AUD/NZD/GBP), payment terms, and tax groups.
  2. **Expanded Level 2 Group `2.5` [SNG-RECONCILIATION]**:
     * **`2.5.3`**: *Group Report Reconciliation*. Multi-entity consolidation, intercompany trade elimination (matching `G/L 110020` AR against `G/L 200030` AP), and group inventory asset consolidation.
  3. **Repository Updates**:
     * Synchronized [**`Process_Hierarchy_Map.md`**](file:///Users/billy/SAPB1_Sim/Process_Hierarchy_Map.md), [**`process_data.py`**](file:///Users/billy/SAPB1_Sim/process_data.py), [**`Schema.md`**](file:///Users/billy/SAPB1_Sim/Schema.md), and [**`README.md`**](file:///Users/billy/SAPB1_Sim/README.md).
     * Recompiled Excel workbook [**`SAP_B1_Process_Design_Matrix.xlsx`**](file:///Users/billy/SAPB1_Sim/SAP_B1_Process_Design_Matrix.xlsx) with 31 process routes.

---

### Release `v2.3.0` — Exception Routing & Financial Audit Extensions
* **Release Date**: 2026-09-05
* **Key Enhancements**:
  1. Formalized **`2.4.1`** (PO Reroute: ICC to AU DC), **`2.4.2`** (PO Reroute: AU DC to ICC), and **`2.4.3`** (Intercompany Container Variance & Physical Loss Write-Off via `OIGE`/`OIGN`).
  2. Formalized **`2.5.1`** (Subledger `OITW` vs Balance Sheet Control `G/L 100010/100050` reconciliation) and **`2.5.2`** (Landed Cost clearing `G/L 200050` net-zero reconciliation).

---

### Release `v2.2.0` — RACI Policy 9 Alignment & Logistics OINV Ownership
* **Release Date**: 2026-09-04
* **Key Enhancements**:
  1. Updated RACI Governance Policy 9: **`[Logistics]`** is designated Accountable & Responsible for creating and posting Direct AR Tax Invoices (`OINV`) directly from Sales Orders (`ORDR`) as part of physical order dispatch confirmation.
  2. Strict Zero-ODLN Policy enforcement: Outbound Delivery Notes (`ODLN`) are eliminated across all 28 route variants.

---

### Release `v2.1.0` — Standard 2.2.2 Benchmark Harmonization
* **Release Date**: 2026-09-04
* **Key Enhancements**:
  1. Established Process `2.2.2` (12-step model) as the canonical enterprise blueprint.
  2. Structured all 280+ Level 4 procedural steps with mandatory 5-attribute metadata (Document/Table, OnHand Snapshot, Valuation Algorithm, CoA Journal Entry `OJDT`).

---

## 4. Master Topology Process Scope (31 Process Variants)

| Group | Group Classification | Level 3 Process Variants Included | Operating DBs |
| :---: | :--- | :--- | :---: |
| **`2.1`** | **`[SNG-AU-ONLY]`** (AU Domestic DC) | `2.1.1`, `2.1.2`, `2.1.3` (3 Routes) | `old_b1.db` |
| **`2.2`** | **`[SNG-HYBRID]`** (Intercompany & Trans-Tasman Relay) | `2.2.1`, `2.2.2`, `2.2.3`, `2.2.4`, `2.2.5`, `2.2.6`, `2.2.7`, `2.2.8`, `2.2.9`, `2.2.10`, `2.2.11` (11 Routes) | `new_b1` + `old_b1` |
| **`2.3`** | **`[SNG-NEW-ONLY]`** (Int'l Multi-Leg, NZ, UK & D2C) | `2.3.1`, `2.3.2`, `2.3.3`, `2.3.4`, `2.3.5`, `2.3.6`, `2.3.7`, `2.3.8`, `2.3.9` (9 Routes) | `new_b1.db` |
| **`2.4`** | **`[SNG-EXCEPTION]`** (PO Reroutes & Discrepancies) | `2.4.1`, `2.4.2`, `2.4.3` (3 Processes) | `new_b1` ↔ `old_b1` |
| **`2.5`** | **`[SNG-RECONCILIATION]`** (Financial & Landed Cost Audit) | `2.5.1`, `2.5.2`, `2.5.3` (3 Processes) | `new_b1` + `old_b1` |
| **`2.6`** | **`[MD-MAINTENANCE]`** (Master Data Maintenance) | `2.6.1`, `2.6.2` (2 Processes) | `new_b1` + `old_b1` |

---

## 5. Git Commit Traceability & Synchronization Log

| Commit Hash | Author | Milestone Narrative | Modified Core Files |
| :--- | :---: | :--- | :--- |
| `b4552c2` | BL | Initial commit of SAP Business One enterprise process architecture, simulation models, and documentation | Full Workspace Initial Commit |
| `29848c7` | BL | Add enterprise SAP Business One database Schema.md reference | `Schema.md` |
| `[HEAD]` | BL | Expand process architecture to 6 Node Groups & 31 Level 3 routes (20260905 Register) | `Process_Hierarchy_Map.md`, `process_data.py`, `README.md`, `Version_Control.md`, `SAP_B1_Process_Design_Matrix.xlsx` |
