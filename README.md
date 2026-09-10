# SAP Business One (SAP B1) Enterprise Database Simulation

A complete, self-contained SQLite simulation of the **SAP Business One (SAP B1)** enterprise schema, featuring **82 standard ERP tables** and realistic sample records with full relational foreign-key integrity across all core business modules.

---

## 📑 Project Artifacts & Documentation
- 📋 **Implementation Plan**: [implementation_plan.md](file:///Users/billy/.gemini/antigravity-ide/brain/6515debb-477e-4f5d-b674-003b5e0f4bf9/implementation_plan.md)
- 🚶 **Walkthrough & Verification**: [walkthrough.md](file:///Users/billy/.gemini/antigravity-ide/brain/6515debb-477e-4f5d-b674-003b5e0f4bf9/walkthrough.md)

---

## 🗄️ Database Architecture & Table Overview (82 Tables)

### 1. Master Data & Chart of Accounts
- **`OACT`**: Chart of Accounts Master (Assets, Liabilities, Equity, Revenue, COGS, Operating Expenses).
- **`OWHS`**: Warehouses Master Data (Primary Distribution Center, Regional Hubs, Storage Depots).
- **`OCRD`**: Business Partner Master (`CardType` `'C'` for Customers, `'S'` for Suppliers/Vendors).
- **`OITM`**: Item Master Data (`OnHand`, `IsCommited`, `OnOrder`, `AvgPrice`, `DfltWH`).
- **`OITW`**: Item Warehouse Inventory Data (Stock levels distributed per warehouse).

### 2. Banking & Payments (Order-to-Cash & Procure-to-Pay Settlement)
- **`OCTG`**: Payment Terms Master (Net 30, Net 60, COD, Discounts).
- **`ODSC`**: Bank Master Codes & House Banks (CBA, ANZ, Westpac, NAB, Macquarie).
- **`ORCT` / `RCT2`**: Incoming Payments Header & Paid Invoices Line (Customer AR settlements).
- **`OVPM` / `VPM2`**: Outgoing Payments Header & Paid Invoices Line (Vendor AP disbursements).

### 3. Production & Manufacturing (BOM & Work Orders)
- **`OITT` / `ITT1`**: Bill of Materials (BOM) Product Trees (Parent assembly & child components).
- **`OWOR` / `WOR1`**: Production Orders Header & Component Issue Lines.
- **`OIGN` / `IGN1`**: Goods Receipt from Production (Finished goods inward receipt).
- **`OIGE` / `IGE1`**: Goods Issue to Production (Raw material consumption).

### 4. Pricing, Tax Engine & Special Conditions
- **`OPLN`**: Price Lists Master (Wholesale, Retail, Key Account, Clearance).
- **`ITM1`**: Item Price List Matrix (Multi-tier pricing matrix per item).
- **`OSPP` / `SPP1`**: Business Partner Special Prices & Volume Discount Tiers.
- **`OSTC`**: Sales & Purchase Tax Codes (GST 10%, GST Free, Duty, Luxury Tax).

### 5. Advanced Inventory: Batches, Serials, Bins & Cycle Counting
- **`OBTN`**: Batch Numbers Master (Batch numbers, expiration dates, manufacturing dates).
- **`OSRN`**: Serial Numbers Master (Individual serial number tracking per item).
- **`OITL` / `ITL1`**: Inventory Transaction Log & Batch/Serial Allocation history.
- **`OBIN`**: Warehouse Bin Locations (Aisle, rack, and shelf location hierarchy).
- **`OINC` / `INC1`**: Physical Inventory Cycle Counting (Recorded vs counted variance).

### 6. Purchasing & Accounts Payable (AP Pipeline)
- **`OPRQ` / `PRQ1`**: Purchase Requests (Internal departmental requisition).
- **`OPQT` / `PQT1`**: Purchase Quotations (Supplier price quote requests).
- **`OPOR` / `POR1`**: Purchase Orders (Header & Lines).
- **`OPDN` / `PDN1`**: Goods Receipt PO (GRPO - Inward inventory receipt).
- **`OPCH` / `PCH1`**: AP Invoices (Vendor tax invoices & payables).
- **`ORPC` / `RPC1`**: AP Credit Memos (Supplier returns and credit notes).

### 7. Sales & Accounts Receivable (AR Pipeline)
- **`OQUT` / `QUT1`**: Sales Quotations (Customer price quotes).
- **`ORDR` / `RDR1`**: Sales Orders (Header & Lines).
- **`ODLN` / `DLN1`**: Delivery Notes (Outward inventory dispatch).
- **`ORDN` / `RDN1`**: Sales Returns (Goods return before credit memo).
- **`OINV` / `INV1`**: AR Invoices (Customer tax invoices & receivables).
- **`ORIN` / `RIN1`**: AR Credit Memos (Customer returns and credit adjustments).

### 8. CRM & Business Partner Sub-Masters
- **`OCPR`**: Contact Persons Master (Names, positions, emails, direct numbers).
- **`CRD1`**: Business Partner Addresses (Multiple Bill-to and Ship-to addresses).
- **`OCRG`**: Business Partner Groups (Customer & Vendor classifications).
- **`OOPR` / `OPR1`**: Sales Opportunities & Sales Pipeline Stage Tracking.
- **`OCLG`**: CRM Activities Master (Calls, meetings, tasks linked to BP).

### 9. Cost Accounting, Projects & Financial Budgets
- **`ODIM`**: Cost Dimensions (Departments, Territories, Channels, Programs).
- **`OPRC`**: Cost Centers / Profit Centers Master.
- **`OPMG` / `PMG1`**: Project Management Master & Milestone Stages.
- **`OBGT` / `BGT1`**: Financial Budget Scenarios & G/L Account Budgets.

### 10. Landed Costs & Customs
- **`OALC`**: Landed Cost Allocation Master (Customs duty, ocean freight, port wharfage, air cargo surcharge, interstate cartage).
- **`OIPF` / `IPF1` / `IPF2`**: Landed Cost Document Header, Items Allocation & Fee Breakdown (explicitly linked to Goods Receipt POs `OPDN`/`PDN1` via `BaseType=20`, `BaseEntry`, `BaseLine`, supporting both Estimated `DocType='E'` and Actual `DocType='A'` landed costs).

### 11. Financial Journal Entries & Reconciliation
- **`OJDT` / `JDT1`**: Financial Journal Entries (Balanced Debit/Credit Lines).
- **`OITR` / `ITR1`**: Internal Reconciliation (G/L and BP transaction settlements).

### 12. Inventory Transfers, Intercompany Movements & Valuation Audit Log
- **`OWTQ` / `WTQ1`**: Inventory Transfer Requests across origin, sea-transit, and destination hubs.
- **`OWTR` / `WTR1`**: Inventory Transfers between Warehouses (e.g. `ICC` -> `SIT` -> `AUWHS`).
- **`OIGE` / `IGE1`**: Goods Issues (e.g. clearing stock out of transit `SIT`).
- **`OINM`**: Warehouse Journal & Valuation Audit Trail (Logging GRPO `TransType=20`, Transfers `TransType=67`, Goods Issue `TransType=60`, and Landed Cost Revaluations `TransType=69`).
- **`ADOC` / `ADT1`**: Field-Level Change Log & System Audit History.

### 🌟 10-Step Intercompany Transfer & Stacked Landed Cost Journey
The database models the complete multi-warehouse intercompany supply chain:
1. **Factory GRPO at `ICC`**: Goods received on GRPO (`OPDN`/`PDN1`) from external factory vendor at FOB cost ($C_{\text{FOB}}$).
2. **Estimated Origin Landed Cost at `ICC`**: `OIPF` (`DocType='E'`) adds origin terminal handling, export brokerage, and factory cartage (+$24/unit).
3. **Inventory Valuation at `ICC`**: `OITW.AvgPrice('ICC')` = $C_{\text{FOB}} + \$24.00$.
4. **Transfer `ICC` → `SIT`**: `OWTR`/`WTR1` transfers stock into Sea In-Transit at $C_{\text{ICC}}$ (`OITW.AvgPrice('SIT')` = $C_{\text{ICC}}$).
5. **Transfer Request `SIT` → `AUWHS`**: `OWTQ`/`WTQ1` initiates port arrival transfer.
6. **Intercompany GRPO at `AUWHS`**: Goods received into Australian DC at `SIT` transferred cost.
7. **Goods Issue at `SIT`**: `OIGE`/`IGE1` issues goods out of `SIT` at `SIT` cost.
8. **Estimated Destination Landed Cost at `AUWHS`**: `OIPF` (`DocType='E'`) calculates estimated ocean freight, estimated import tariff, and port wharfage (+$80/unit → temporary cost $C_{\text{SIT}} + \$80.00$).
9. **Actual Landed Cost Posted at `AUWHS`**: `OIPF` (`DocType='A'`) reconciles actual carrier bunker adjustments and final customs invoices (+$98/unit), overwriting estimated cost to establish final $\text{AUWHS Cost} = C_{\text{SIT}} + \$98.00$.
10. **Stacked Landed Cost Distribution**: `OITW.AvgPrice` across every warehouse retains its distinct accumulated value along the journey.

---

## 🚀 Quick Start Guide

### 1. Launch Interactive Web App UI Simulator (Recommended)
To run the full SAP Fiori / Horizon Web Application UI Simulator:
```bash
python3 app.py
```
Open your browser at **`http://localhost:5050`** to access:
- 📊 **Executive Cockpit**: Real-time KPI tiles for Revenue, Stock Valuation, AR/AP balances, and Open Order Backlog.
- 🏷️ **SAP Golden Arrows (➡️)**: Drill-down modals into Customer 360°, Item 360°, and Document Lines.
- 🕸️ **Document Relationship Map**: Interactive lifecycle flow from Quotations to Settlements.
- 📑 **Document Explorer**: Form viewer for Sales Orders, POs, Invoices, Deliveries, and Work Orders.
- 🛠️ **Live SQL Studio**: Query runner with schema browser across all 82 tables and 12 built-in analytical presets.

### 2. Re-seed or Reset Databases
- To regenerate **`new_b1.db`** (Multi-Warehouse Costing):
  ```bash
  python3 init_new_b1.py
  ```
- To regenerate **`old_b1.db`** (Single-Level Company Valuation):
  ```bash
  python3 init_old_b1.py
  ```
- To compare valuations between **`new_b1.db`** and **`old_b1.db`**:
  ```bash
  python3 compare_b1_dbs.py
  ```

### 3. Run Showcase Queries (CLI)
To execute 12 multi-module analytical queries in terminal:
```bash
python3 query_sap_b1.py           # Queries new_b1.db by default
python3 query_sap_b1.py old_b1.db # Queries old_b1.db
```

### 4. Interactive SQL Console (CLI)
To query tables interactively in terminal:
```bash
python3 run_sql.py                # Connects to new_b1.db
python3 run_sql.py old_b1.db      # Connects to old_b1.db
```
*(Type any SQL statement like `SELECT * FROM OITT LIMIT 5;` at the `SQL> ` prompt)*

---

## 💡 Example Practice Queries

### 1. Order-to-Cash Settlement Reconciliation
```sql
SELECT 
    T0.DocNum AS Payment_Num,
    T0.DocDate,
    T0.CardName AS Customer,
    T2.DocNum AS Invoice_Num,
    T1.SumApplied AS Amount_Settled,
    T0.DocTotal AS Payment_Total
FROM ORCT T0
INNER JOIN RCT2 T1 ON T0.DocEntry = T1.DocEntry
LEFT JOIN OINV T2 ON T1.InvoiceId = T2.DocEntry
ORDER BY T0.DocNum LIMIT 5;
```

### 2. Bill of Materials (BOM) Explosion with Costing
```sql
SELECT 
    T0.Code AS Parent_Item,
    T1.ItemName AS Parent_Description,
    T2.Code AS Child_Component,
    T3.ItemName AS Component_Description,
    T2.Quantity,
    T2.Price AS Component_Unit_Cost,
    (T2.Quantity * T2.Price) AS Total_Cost
FROM OITT T0
INNER JOIN OITM T1 ON T0.Code = T1.ItemCode
INNER JOIN ITT1 T2 ON T0.Code = T2.Father
INNER JOIN OITM T3 ON T2.Code = T3.ItemCode
ORDER BY T0.Code, T2.ChildNum LIMIT 5;
```

### 3. Batch Inventory Expiration Audit
```sql
SELECT 
    T0.DistNumber AS Batch_Number,
    T0.ItemCode,
    T1.ItemName,
    T0.WhsCode,
    T0.Quantity AS Batch_Stock,
    T0.InDate,
    T0.ExpDate
FROM OBTN T0
INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
ORDER BY T0.ExpDate ASC LIMIT 5;
```
