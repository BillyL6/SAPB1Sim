# Scratch script to generate updated process_data.py with canonical role names and 2.2.2 standard across all 28 processes

import sys
import os

# We will construct the entire process_data.py content cleanly.
content = '''# Master Process Data Definition for SAP Business One Enterprise Supply Chain Simulation
# Standardized Naming Convention for Level 4 Steps:
# '[Step Code]: [Role] Action/Verb Document (DocType) @ Location → [Milestone/Outcome]'
# Canonical RACI Roles: [Purchasing], [Logistics], [Finance], [Sales], [Corporate Treasury]

PRINCIPLES_DATA = [
    ("Currency Isolation",
     "Isolate foreign factory purchase commitments in USD (DocCur='USD') from domestic statutory balance sheets.",
     "Protects operating ledgers from foreign exchange volatility while preserving exact contractual vendor agreement pricing.",
     "OPOR PriceFC locked in foreign subledger; deterministic spot FX conversion occurs at OPDN date into AUD."),
    
    ("Perpetual Asset Custody",
     "Eliminate blind transit periods by routing all multi-node international movements through dedicated In-Transit (SIT) warehouses.",
     "Ensures 100% legal ownership and physical custody visibility on financial statements throughout ocean and coastal transit legs.",
     "OWTR transfers stock from source DC to SIT (Dr 100050 SIT Asset / Cr 100040); open intercompany OPOR tracks vessel B/L & ETA."),
    
    ("Zero Profit Distortion",
     "Execute all intercompany transfers strictly at the source ship-from moving average cost (OITW.AvgPrice / MWAG).",
     "Prevents artificial internal margin buildup, transfer pricing tax anomalies, and intercompany profit elimination complexities.",
     "Origin DB records Intercompany AR (110020) at exact source cost ($424.00 AUD); Destination DB capitalizes inventory (100010) at $424.00 AUD."),
    
    ("Zero-ODLN Standard & Direct Financial Consolidation (Lean Order-to-Cash)",
     "Enforce Universal Direct AR Invoicing (OINV based on ORDR) across all sales orders, strictly eliminating standalone Delivery Notes (ODLN) across all outbound processes. In intercompany transfers, replace outbound delivery with Goods Issue (OIGE) out from SIT synchronized with destination Goods Receipt PO (OPDN) at AU DC.",
     "Streamlines fulfillment velocity, eliminates redundant unbilled delivery holding accounts (G/L 100030), and provides strict zero-ODLN compliance across the entire ERP ecosystem.",
     "• Outbound Customer Sales: Direct OINV based on ORDR (Dr 110010 AR / Dr 500010 COGS / Cr 400010 Rev / Cr 100010 Inv / Cr 200020 GST).\\n• Cross-DB Intercompany Transfer: Origin posts OIGE out from SIT (Dr 110020 IC AR / Cr 100050 SIT) ↔ Destination posts OPDN at AU DC (Dr 100010 Inv / Cr 200030 IC AP)."),
    
    ("Two-Stage Landed Cost Valuation (Provisional Accrual & Actual Overwrite)",
     "Mandate that every Goods Receipt PO (OPDN) immediately posts an Estimated Landed Cost (OIPF DocType 'E') upon receipt, followed subsequently by an Actual Landed Cost (OIPF DocType 'A') to overwrite the estimate when final carrier and broker invoices arrive.",
     "Guarantees that moving average inventory valuation (OITW.AvgPrice) and customer shipment COGS reflect estimated landed costs from Day 1, preventing margin inflation prior to invoice arrival and automating reconciliation of freight accrual liabilities (G/L 200050) to $0.00.",
     "OPDN immediately triggers OIPF 'E' (Dr 100010/100040 Inventory / Cr 200050 Estimated Clearing); subsequent OIPF 'A' overwrites the estimate (Dr 200050 Estimated Clearing / Dr/Cr 100010/100040 Inventory Variance / Cr 200010 Carrier AP), netting G/L 200050 to $0.00."),
    
    ("Standardized Step Naming Taxonomy",
     "Always construct process steps using the rigid semantic taxonomy: '[Step Code]: [Role] Action/Verb Document (DocType) @ Location → [Milestone/Outcome]'.",
     "Ensures absolute operational clarity, cross-functional role accountability, ERP document transparency, and consistent procedural governance across the enterprise.",
     "Canonical Reference: '2.2.1.1: [Purchasing] Issue Factory PO in USD (OPOR) @ ICCNGB → [Vendor Production Commitment]'."),
    
    ("Role-Based RACI Governance & Document Segregation",
     "Enforce strict functional segregation of duties across Purchasing, Logistics, and Finance across all supply chain transaction lifecycles.",
     "Eliminates operational ambiguity, prevents unauthorized commitments, ensures audit compliance, and establishes deterministic document ownership across the enterprise.",
     "• [Purchasing] = OPOR (All Purchase Orders) & OWTQ (All Transfer Requests)\\n• [Logistics] = All Material Movements (OIGE Goods Issue, OPDN Goods Receipt, OWTR Transfers)\\n• [Finance] = All Cost Accounting, OIPF Landed Costs, Direct OINV Invoicing & G/L Reconciliations.")
]

POLICIES_DATA = [
    ("POLICY 1\\n(Rule 1.1)", "Factory Purchase Orders Strictly in USD (Foreign Currency Isolation)", "Procurement / External Factory POs",
     "• All external factory Purchase Orders (OPOR/POR1) are issued strictly in USD (DocCur='USD', PriceFC).\\n• Overseas supplier price lists remain locked in USD FOB terms to isolate contractual obligations from domestic currency shifts.",
     "• OPOR: DocCur='USD', PriceFC locked in POR1.\\n• Off-balance sheet commitment in foreign subledger.\\n• Preserves exact vendor agreement pricing without ERP exchange noise."),
    
    ("POLICY 2\\n(Rule 2.1)", "Functional Currency (AUD) for Downstream Documents & Transfers", "All Downstream Operations (OPDN to OINV)",
     "• All downstream documents (OPDN, OIPF, OWTQ, OWTR, OIGE, ORDR, OINV, OJDT) are posted in Australian Dollars (AUD).\\n• Spot FX conversion (AUD/USD DocRate = 0.65) occurs deterministically at Goods Receipt PO (OPDN) posting date.",
     "• OPDN: Converts FOB USD to AUD base inventory cost (AUD = USD / 0.65).\\n• G/L Dr Inventory (100040/100010) / Cr Goods Receipt Clearing (200060/200010) in AUD.\\n• Locks inventory valuation in statutory local currency."),
    
    ("POLICY 3\\n(Rule 3.1)", "Mandatory In-Transit (SIT) Warehouse for Intercompany Transfers", "Inter-Warehouse & Intercompany Legs",
     "• Every international/intercompany movement between supply chain nodes (ICC, AU Whs, NZ Whs, UK) must route through an In-Transit (SIT) warehouse node (ICCSIT, NZSIT, UKSIT).\\n• Perpetual tracking of on-the-water stock.",
     "• OWTR: Moves OnHand from Origin Whs to SIT Whs.\\n• G/L Dr Goods In Transit Asset (100050) / Cr Warehouse Stock (100040).\\n• Eliminates blind transit periods on balance sheets."),
    
    ("POLICY 4\\n(Rule 4.1)", "Intercompany Goods Issue from SIT Synchronized with Destination GRPO at Source MWAG", "Cross-DB & Trans-Tasman Transfers",
     "• In cross-database intercompany transfers (e.g. ICCSIT in new_b1.db → FDMSYD/BDLMEL in old_b1.db), stock is discharged from SIT via Goods Issue (OIGE) in the origin database, synchronized with an Inbound Goods Receipt PO (OPDN) at the destination AU Warehouse.\\n• Outbound Delivery Notes (ODLN) are strictly prohibited for intercompany transfers.\\n• Intercompany transfers execute strictly at source unit moving average cost (OITW.AvgPrice / MWAG), preserving zero internal profit/loss distortion.",
     "• Base Transfer Price = Source OITW.AvgPrice ($424.00 AUD).\\n• Origin DB (new_b1.db): OIGE out from ICCSIT: Dr Intercompany AR (110020) $42,400 / Cr SIT Asset (100050) $42,400.\\n• Dest DB (old_b1.db): OPDN at FDMSYD: Dr Inventory Asset (100010) $42,400 / Cr Intercompany AP (200030) $42,400.\\n• Zero profit distortion; Delivery Notes (ODLN) bypassed completely."),
    
    ("POLICY 5\\n(Rule 5.1)", "Mandatory Two-Stage Landed Cost Accrual & Actual Overwrite", "All Goods Receipt POs (OPDN)",
     "• Every Goods Receipt PO (OPDN) must immediately have an Estimated Landed Cost (OIPF DocType 'E') posted upon receipt to accrue provisional freight, duties, and handling into moving average cost (OITW.AvgPrice).\\n• When final carrier and customs broker AP invoices arrive, an Actual Landed Cost (OIPF DocType 'A') is posted to overwrite the estimated landed cost, adjust inventory valuation for actual variance, and reconcile the estimated clearing account (G/L 200050) to exactly $0.00.",
     "• Stage 1 (Estimate at OPDN): Dr 100010/100040 (Inventory Asset) / Cr 200050 (Estimated Landed Cost Clearing).\\n• Stage 2 (Actual Overwrite at AP Invoice): Dr 200050 (Estimated Clearing) / Dr/Cr 100010/100040 (Inventory Variance) / Cr 200010 (Carrier & Broker AP).\\n• Fully clears G/L 200050 balance to $0.00."),
    
    ("POLICY 6\\n(Rule 6.1)", "Universal Direct AR Invoicing & Zero Outbound Delivery Notes (Customer Settlement Out of Scope)", "All Customer & Wholesale Fulfillment (Global)",
     "• Delivery Notes (ODLN) are strictly forbidden as outbound documents across ALL sales order fulfillment processes (AU domestic, NZ domestic, AU-to-NZ export, UK Wayfair, and D2C Drop-Ship).\\n• Outbound customer orders must generate Direct AR Tax Invoices (OINV) created directly against the Sales Order (ORDR).\\n• Customer receivable settlement (Incoming Payments / ORCT) and banking cash reconciliation are strictly OUT OF SCOPE of all operational supply chain processes.\\n• The Direct AR Tax Invoice (OINV) concurrently consolidates stock deduction (OnHand), COGS recognition, revenue posting, and tax into a single unified financial journal entry (OJDT), establishing the open customer receivable for downstream corporate treasury.",
     "• Outbound Rule: ORDR → Direct OINV (No ODLN permitted).\\n• Final Milestone G/L Entry (OJDT):\\n  Dr Accounts Receivable (110010) [Gross Incl Tax]\\n  Dr Cost of Goods Sold - COGS (500010) [OnHand x AvgPrice]\\n  Cr Sales Revenue (400010) [Net Price]\\n  Cr GST / VAT Output Tax (200020) [Applicable Tax]\\n  Cr Inventory Asset (100010/100040) [OnHand x AvgPrice]\\n• Customer payment settlement (ORCT) is managed independently by corporate treasury outside the operational supply chain lifecycle."),
    
    ("POLICY 7\\n(Rule 7.1)", "Mandatory Inventory Transfer Request (OWTQ) & Picking for In-Transit Movements (OWTR to SIT)", "All Warehouse-to-SIT Transfer Legs",
     "• For all stock movements transferring from a physical warehouse to a Stock-in-Transit (SIT) warehouse node (ICCSIT, NZSIT, UKSIT), an Inventory Transfer Request (OWTQ) must always be created first to reserve stock (OITW.IsCommited) and transmit picking instructions to the warehouse.\\n• The warehouse operator completes physical picking and staging against the OWTQ.\\n• Successful picking completion triggers the generation of the Inventory Transfer (OWTR) based directly on the OWTQ, executing the balance sheet transfer to In-Transit stock.",
     "• Step 1: Logistics Coordinator creates OWTQ (OITW.IsCommited = +Qty at source warehouse, no financial entry).\\n• Step 2: Warehouse Operator completes physical picking & inspection.\\n• Step 3: Warehouse Operator / System posts OWTR based on OWTQ: Dr 100050 (Goods In Transit Asset) / Cr 100040 (Warehouse Stock Asset), moving OnHand to SIT and clearing IsCommited."),
    
    ("POLICY 8\\n(Rule 8.1)", "Zero-ODLN Architecture for Intra-Company & Cross-Database Transfers", "System Architecture (new_b1.db vs old_b1.db)",
     "• Single DB transfers (e.g. ICCNGB → ICCSIT or NZNTH → NZSTH): Use native OWTQ (Picking Request) → OWTR (Stock Transfer).\\n• Cross-DB transfers (e.g. ICCSIT in new_b1.db → BDLMEL/FDMSYD in old_b1.db): Use Origin Goods Issue (OIGE) from SIT in new_b1.db synchronized with Inbound Goods Receipt PO (OPDN) in old_b1.db (strictly bypassing ODLN).\\n• Outbound customer sales in any DB: Use Direct AR Invoice (OINV) directly based on Sales Order (ORDR).",
     "• Single-DB: OWTQ (Commitment) → OWTR (Dr 100050 SIT / Cr 100040 Stock).\\n• Cross-DB: Origin new_b1 posts OIGE (Dr 110020 IC AR / Cr 100050 SIT) ↔ Dest old_b1 posts OPDN (Dr 100010 Stock / Cr 200030 IC AP).\\n• Customer Sales: Direct OINV based on ORDR (Dr 110010 AR / Dr 500010 COGS / Cr 400010 Rev / Cr 100010 Stock)."),
    
    ("POLICY 9\\n(Rule 9.1)", "Operational RACI Governance: Role Accountability & Document Segregation", "Enterprise-Wide Governance",
     "• [Purchasing] is strictly Responsible & Accountable (R/A) for all Purchase Orders (OPOR in USD/AUD) and all Inventory/Intercompany Transfer Requests (OWTQ).\\n• [Logistics] is strictly Responsible & Accountable (R/A) for all material movements, physical picking, Goods Issue (OIGE), Goods Receipt POs (OPDN), and Inventory Transfers (OWTR).\\n• [Finance] is strictly Responsible & Accountable (R/A) for all Cost Accounting, Landed Cost accruals and actual overwrites (OIPF 'E'/'A'), Direct AR Invoices (OINV), and G/L clearing reconciliations (200050/100050/110020).\\n• [Sales] manages Sales Orders (ORDR); [Corporate Treasury] manages Customer Settlements (ORCT) outside operational P2F scope.",
     "• Document Segregation Matrix:\\n  - [Purchasing]: OPOR (POR1), OWTQ (WTQ1)\\n  - [Logistics]: OWTR (WTR1), OIGE (IGE1), OPDN (PDN1)\\n  - [Finance]: OIPF (IPF1/IPF2), OINV (INV1), OJDT (JDT1)\\n  - [Sales]: ORDR (RDR1)\\n  - [Treasury]: ORCT (RCT1 - Out of Scope)")
]

RACI_DATA = [
    ("Factory Purchase Orders", "OPOR", "USD", "Purchasing", "Accountable (A) / Responsible (R)", "Logistics (C), Finance (I), Sales (I)",
     "• [Purchasing] Issues factory purchase orders (OPOR in USD FOB) to commit vendor manufacturing.\\n• Locks foreign price list (PriceFC) without generating financial entries until receipt."),
     
    ("Intercompany Inbound Purchase Orders", "OPOR", "AUD", "Purchasing", "Accountable (A) / Responsible (R)", "Logistics (C), Finance (I)",
     "• [Purchasing] Issues destination intercompany POs tracking ocean container shipments & B/L.\\n• Establishes inbound on-order quantity commitment in destination ERP database."),
     
    ("Intercompany & Stock Transfer Requests", "OWTQ", "AUD", "Purchasing", "Accountable (A) / Responsible (R)", "Logistics (R), Finance (I)",
     "• [Purchasing] Generates all Inventory Transfer Requests (OWTQ) for intercompany stock rebalancing.\\n• Sets source/destination warehouses and commits inventory (OITW.IsCommited) for warehouse picking queue."),
     
    ("Warehouse Picking & Staging", "OWTQ / Pick List", "N/A", "Logistics", "Accountable (A) / Responsible (R)", "Purchasing (I), Finance (I)",
     "• [Logistics] Executes physical bin/aisle picking, quantity verification, export carton labeling, and container staging against active OWTQ transfer requests."),
     
    ("Inventory Transfers to In-Transit (SIT)", "OWTR", "AUD", "Logistics", "Accountable (A) / Responsible (R)", "Purchasing (I), Finance (I)",
     "• [Logistics] Posts Inventory Transfer (OWTR) based on completed OWTQ.\\n• Executes physical dispatch and balance sheet transfer: Dr 100050 SIT Asset / Cr 100040 Warehouse Stock."),
     
    ("Material Movement: Goods Issue from SIT", "OIGE", "AUD", "Logistics", "Accountable (A) / Responsible (R)", "Purchasing (I), Finance (C/I)",
     "• [Logistics] Posts Goods Issue (OIGE) discharging stock out from SIT (ICCSIT) upon ocean port arrival / vessel unlading.\\n• Synchronizes with destination GRPO; origin posts Dr 110020 Intercompany AR / Cr 100050 SIT Asset."),
     
    ("Material Movement: Inbound Goods Receipt", "OPDN", "AUD", "Logistics", "Accountable (A) / Responsible (R)", "Purchasing (I), Finance (C/I)",
     "• [Logistics] Receives physical delivery at warehouse dock, performs count/quality inspection, and posts Goods Receipt PO (OPDN).\\n• Dr 100010/100040 Inventory Asset / Cr 200060/200030 Goods Receipt Clearing/AP."),
     
    ("Provisional Estimated Landed Cost Accrual", "OIPF ('E')", "AUD", "Finance", "Accountable (A) / Responsible (R)", "Purchasing (C), Logistics (C)",
     "• [Finance] Posts Estimated Landed Cost (OIPF DocType 'E') immediately following every OPDN.\\n• Accrues estimated freight, duty, and wharfage into inventory moving average (OITW.AvgPrice): Dr 100010/100040 / Cr 200050."),
     
    ("Actual Landed Cost Overwrite & Cost Accounting", "OIPF ('A')", "AUD", "Finance", "Accountable (A) / Responsible (R)", "Purchasing (I), Logistics (C)",
     "• [Finance] Matches actual customs broker & freight carrier AP invoices (OPCH).\\n• Posts Actual Landed Cost (OIPF DocType 'A') to overwrite provisional estimates, adjust inventory valuation, and reconcile G/L 200050 to exactly $0.00."),
     
    ("Customer Sales Order Booking", "ORDR", "AUD", "Sales", "Accountable (A) / Responsible (R)", "Purchasing (I), Logistics (I), Finance (I)",
     "• [Sales] Books customer sales order (ORDR), allocating available finished goods stock (OITW.IsCommited)."),
     
    ("Direct AR Invoicing & Revenue/COGS Accounting", "OINV", "AUD", "Finance", "Accountable (A) / Responsible (R)", "Sales (I), Logistics (C)",
     "• [Finance] Posts Direct AR Tax Invoice (OINV) created directly against Sales Order (ORDR).\\n• Concurrently relieves inventory (100010), recognizes COGS (500010), posts Revenue (400010), tax (200020), and establishes AR (110010) in single unified journal entry."),
     
    ("Customer Payment Settlement & Banking", "ORCT", "AUD", "Corporate Treasury", "Accountable (A) / Responsible (R) [Out of Scope]", "Finance (C), Purchasing (I), Logistics (I)",
     "• [Corporate Treasury] Manages incoming customer payments, bank reconciliation, and receivable collections.\\n• Explicitly OUT OF SCOPE of operational P2F supply chain value stream.")
]

INDEX_DATA = [
    ("2.1 [SNG-AU-ONLY]", "2.1.1", "Factory → AU Warehouse → AU Consumer", "old_b1.db", "Factory", "Direct B/L", "FDMSYD", "Two-Stage Destination Landed Cost (OIPF 'E' Accrual + 'A' Overwrite)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.1 [SNG-AU-ONLY]", "2.1.2", "Factory → AU Warehouse → NZ Consumer", "old_b1.db", "Factory", "Direct Freight", "FDMSYD", "Two-Stage AU Inward Landed Cost + Cross-Border Direct Invoicing", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.1 [SNG-AU-ONLY]", "2.1.3", "Factory → AU Warehouse → UK Wayfair", "old_b1.db", "Factory", "Export Transit", "UKWYF", "Two-Stage AU Inward Landed Cost + Long-Haul UK Freight Stack", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    
    ("2.2 [SNG-HYBRID]", "2.2.1", "Factory → ICC → AU Warehouse → AU Consumer", "new_b1 + old_b1", "ICCNGB", "ICCSIT", "FDMSYD", "Two-Stage Stacked Cost (Origin LC + Dest LC Overwrite)", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.2", "Factory → ICC → AU Warehouse → NZ Consumer", "new_b1 + old_b1", "ICCNGB", "ICCSIT", "FDMSYD", "Two-Stage Stacked Cost at AU DC + Direct Export OINV", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.3", "Factory → ICC → AU Whs → NZ Whs → NZ Consumer", "new_b1 + old_b1", "ICCNGB", "ICCSIT + NZSIT", "NZNTH", "Triple-Stacked Cost: Origin LC + AU Landed + NZ Landed", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.4", "Factory → ICC → NZ Whs → AU Whs → AU Consumer", "new_b1 + old_b1", "ICCNGB", "ICCSIT + NZSIT", "FDMSYD", "Triple-Stacked Cost: Origin LC + NZ Landed + AU Landed", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.5", "Factory → AU Warehouse → NZ Warehouse → NZ Consumer", "new_b1 + old_b1", "FDMSYD", "NZSIT", "NZNTH", "Direct AU Landed Cost + Trans-Tasman Relay at AU MWAG", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.6", "Factory → NZ Warehouse → AU Warehouse → AU Consumer", "new_b1 + old_b1", "NZNTH", "NZSIT", "FDMSYD", "Direct NZ Landed Cost + Trans-Tasman Relay at NZ MWAG", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.7", "Factory → ICC → AU Warehouse → UK Wayfair", "new_b1 + old_b1", "ICCNGB", "ICCSIT + UKSIT", "UKWYF", "Two-Stage Stacked at AU + Long-Haul UK Export Freight", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.8", "Factory → AU Warehouse → NZ Warehouse → UK Wayfair", "new_b1 + old_b1", "FDMSYD", "NZSIT + UKSIT", "UKWYF", "AU Landed + Trans-Tasman Relay + UK Re-Export Freight", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.9", "Factory → NZ Warehouse → AU Warehouse → UK Wayfair", "new_b1 + old_b1", "NZNTH", "NZSIT + UKSIT", "UKWYF", "NZ Landed + Trans-Tasman Relay + UK Re-Export Freight", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.10", "Factory → ICC → AU Whs → NZ Whs → UK Wayfair", "new_b1 + old_b1", "ICCNGB", "ICCSIT + NZSIT + UKSIT", "UKWYF", "Multi-Leg Stacked Costing Across 3 Intercompany Entities", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2.11 [SNG-HYBRID]", "2.2.11", "Factory → ICC → NZ Whs → AU Whs → UK Wayfair", "new_b1 + old_b1", "ICCNGB", "ICCSIT + NZSIT + UKSIT", "UKWYF", "Multi-Leg Stacked Costing Across 3 Intercompany Entities", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    
    ("2.3 [SNG-NEW-ONLY]", "2.3.1", "Factory → NZ Warehouse → NZ Consumer", "new_b1.db", "Factory", "Direct B/L", "NZNTH / NZSTH", "Two-Stage NZ Destination Landed Cost (OIPF 'E' Accrual + 'A' Overwrite)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.2", "Factory → ICC → NZ Warehouse → NZ Consumer", "new_b1.db", "ICCNGB", "ICCSIT + NZSIT", "NZNTH / NZSTH", "Two-Stage Stacked Cost ($424 → $522 → $545 AUD)", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.3", "Factory → UK Wayfair", "new_b1.db", "Factory", "Direct Voyage", "UKWYF", "Two-Stage UK Destination Landed Cost (OIPF 'E' Accrual + 'A' Overwrite)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.4", "Factory → ICC → UK Wayfair", "new_b1.db", "ICCNGB", "UKSIT", "UKWYF", "Two-Stage Stacked Cost ($424 → $424 → $560 AUD)", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.5", "Factory → NZ Warehouse → UK Wayfair", "new_b1.db", "NZNTH", "UKSIT", "UKWYF", "NZ Inbound Landed Cost + UK Maritime Re-Export Freight", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.6", "Factory → ICC → NZ Warehouse → UK Wayfair", "new_b1.db", "ICCNGB", "ICCSIT + UKSIT", "UKWYF", "Two-Stage Stacked at NZ ($522) + UK Freight into UKWYF ($560)", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.7", "Factory → ICC → AU Consumer (D2C Air Express)", "new_b1.db", "ICCNGB", "Air Courier", "AU Consumer", "Origin Staging & Drop-Ship Landed Cost (Direct Air Courier)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.8", "Factory → ICC → NZ Consumer (D2C Air Express)", "new_b1.db", "ICCNGB", "Air Courier", "NZ Consumer", "Origin Staging & Drop-Ship Landed Cost (Direct Air Courier)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.9", "Factory → ICC → UK Consumer (D2C Air Express)", "new_b1.db", "ICCNGB", "Air Courier", "UK Consumer", "Origin Staging & Drop-Ship Landed Cost (Direct Air Courier)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    
    ("2.4 [SNG-EXCEPTION]", "2.4.1", "PO Changes from ICC to AU Warehouse", "new_b1 → old_b1", "ICCNGB", "Direct Port", "FDMSYD / BDLMEL", "Cancels new_b1 PO; re-issues direct import PO in old_b1.db", "OPOR (Cancel), OPOR (New), OPDN, OIPF"),
    ("2.4 [SNG-EXCEPTION]", "2.4.2", "PO Changes from AU Warehouse to ICC", "old_b1 → new_b1", "FDMSYD", "ICCSIT", "ICCNGB → AU", "Cancels old_b1 PO; establishes multi-leg ICC PO in new_b1.db", "OPOR (Cancel), OPOR (New), OPDN, OIPF, OWTQ, OWTR"),
    ("2.4 [SNG-EXCEPTION]", "2.4.3", "Intercompany Transfer Quantity Over/Under-Supply", "new_b1 + old_b1", "ICCSIT", "Wharf / Port", "FDMSYD / NZNTH", "Resolves variance: partial GRPO, transit loss write-off, or surplus receipt", "OPDN, OIGE (Write-Off), OIGN, OINV/OPCH Adj"),
    
    ("2.5 [SNG-RECON]", "2.5.1", "Inventory Valuation Reconciliation", "new_b1 + old_b1", "All Hubs", "In-Transit", "Balance Sheet", "Monthly audit: Warehouse subledger (OITW) vs G/L Control (100010/100050)", "OITW, OINM, OJDT, JDT1, Trial Balance"),
    ("2.5 [SNG-RECON]", "2.5.2", "Landed Cost Entries Reconciliation", "new_b1 + old_b1", "All Hubs", "Accrual Clearing", "G/L 200050", "Reconciles Estimated (OIPF 'E') vs Actual (OIPF 'A') broker invoices to $0", "OIPF, IPF1, IPF2, OPCH, OJDT (200050)")
]
'''
print("Header generated.")
'''
