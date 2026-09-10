# Master Process Data Definition for SAP Business One Enterprise Supply Chain Simulation
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
     "• Outbound Customer Sales: Direct OINV based on ORDR (Dr 110010 AR / Dr 500010 COGS / Cr 400010 Rev / Cr 100010 Inv / Cr 200020 GST).\n• Cross-DB Intercompany Transfer: Origin posts OIGE out from SIT (Dr 110020 IC AR / Cr 100050 SIT) ↔ Destination posts OPDN at AU DC (Dr 100010 Inv / Cr 200030 IC AP)."),
    
    ("Two-Stage Landed Cost Valuation (Provisional Accrual & Actual Overwrite)",
     "Mandate that every Goods Receipt PO (OPDN) immediately posts an Estimated Landed Cost (OIPF DocType 'E') upon receipt, followed subsequently by an Actual Landed Cost (OIPF DocType 'A') to overwrite the estimate when final carrier and broker invoices arrive.",
     "Guarantees that moving average inventory valuation (OITW.AvgPrice) and customer shipment COGS reflect estimated landed costs from Day 1, preventing margin inflation prior to invoice arrival and automating reconciliation of freight accrual liabilities (G/L 200050) to $0.00.",
     "OPDN immediately triggers OIPF 'E' (Dr 100010/100040 Inventory / Cr 200050 Estimated Clearing); subsequent OIPF 'A' overwrites the estimate (Dr 200050 Estimated Clearing / Dr/Cr 100010/100040 Inventory Variance / Cr 200010 Carrier AP), netting G/L 200050 to $0.00."),
    
    ("Standardized Step Naming Taxonomy",
     "Always construct process steps using the rigid semantic taxonomy: '[Step Code]: [Role] Action/Verb Document (DocType) @ Location → [Milestone/Outcome]'.",
     "Ensures absolute operational clarity, cross-functional role accountability, ERP document transparency, and consistent procedural governance across the enterprise.",
     "Canonical Reference: '2.2.1.1: [Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]'."),
    
    ("Role-Based RACI Governance & Document Segregation",
     "Enforce strict functional segregation of duties across Purchasing, Logistics, and Finance across all supply chain transaction lifecycles.",
     "Eliminates operational ambiguity, prevents unauthorized commitments, ensures audit compliance, and establishes deterministic document ownership across the enterprise.",
     "• [Purchasing] = OPOR (All Purchase Orders) & OWTQ (All Transfer Requests)\n• [Logistics] = All Material Movements (OIGE Goods Issue, OPDN Goods Receipt, OWTR Transfers)\n• [Finance] = All Cost Accounting, OIPF Landed Costs, Direct OINV Invoicing & G/L Reconciliations.")
]

POLICIES_DATA = [
    ("POLICY 1\n(Rule 1.1)", "Factory Purchase Orders Strictly in USD (Foreign Currency Isolation)", "Procurement / External Factory POs",
     "• All external factory Purchase Orders (OPOR/POR1) are issued strictly in USD (DocCur='USD', PriceFC).\n• Overseas supplier price lists remain locked in USD FOB terms to isolate contractual obligations from domestic currency shifts.",
     "• OPOR: DocCur='USD', PriceFC locked in POR1.\n• Off-balance sheet commitment in foreign subledger.\n• Preserves exact vendor agreement pricing without ERP exchange noise."),
    
    ("POLICY 2\n(Rule 2.1)", "Functional Currency (AUD) for Downstream Documents & Transfers", "All Downstream Operations (OPDN to OINV)",
     "• All downstream documents (OPDN, OIPF, OWTQ, OWTR, OIGE, ORDR, OINV, OJDT) are posted in Australian Dollars (AUD).\n• Spot FX conversion (AUD/USD DocRate = 0.65) occurs deterministically at Goods Receipt PO (OPDN) posting date.",
     "• OPDN: Converts FOB USD to AUD base inventory cost (AUD = USD / 0.65).\n• G/L Dr Inventory (100040/100010) / Cr Goods Receipt Clearing (200060/200010) in AUD.\n• Locks inventory valuation in statutory local currency."),
    
    ("POLICY 3\n(Rule 3.1)", "Mandatory In-Transit (SIT) Warehouse for Intercompany Transfers", "Inter-Warehouse & Intercompany Legs",
     "• Every international/intercompany movement between supply chain nodes (ICC, AU Whs, NZ Whs, UK) must route through an In-Transit (SIT) warehouse node (ICCSIT, NZSIT, EuropeSIT).\n• Perpetual tracking of on-the-water stock.",
     "• OWTR: Moves OnHand from Origin Whs to SIT Whs.\n• G/L Dr Goods In Transit Asset (100050) / Cr Warehouse Stock (100040).\n• Eliminates blind transit periods on balance sheets."),
    
    ("POLICY 4\n(Rule 4.1)", "Intercompany Goods Issue from SIT Synchronized with Destination GRPO at Source MWAG", "Cross-DB & Trans-Tasman Transfers",
     "• In cross-database intercompany transfers (e.g. ICCSIT in new_b1.db → AU Warehouses in old_b1.db), stock is discharged from SIT via Goods Issue (OIGE) in the origin database, synchronized with an Inbound Goods Receipt PO (OPDN) at the destination AU Warehouse.\n• Outbound Delivery Notes (ODLN) are strictly prohibited for intercompany transfers.\n• Intercompany transfers execute strictly at source unit moving average cost (OITW.AvgPrice / MWAG), preserving zero internal profit/loss distortion.",
     "• Base Transfer Price = Source OITW.AvgPrice ($424.00 AUD).\n• Origin DB (new_b1.db): OIGE out from ICCSIT: Dr Intercompany AR (110020) $42,400 / Cr SIT Asset (100050) $42,400.\n• Dest DB (old_b1.db): OPDN at AU Warehouse: Dr Inventory Asset (100010) $42,400 / Cr Intercompany AP (200030) $42,400.\n• Zero profit distortion; Delivery Notes (ODLN) bypassed completely."),
    
    ("POLICY 5\n(Rule 5.1)", "Mandatory Two-Stage Landed Cost Accrual & Actual Overwrite", "All Goods Receipt POs (OPDN)",
     "• Every Goods Receipt PO (OPDN) must immediately have an Estimated Landed Cost (OIPF DocType 'E') posted upon receipt to accrue provisional freight, duties, and handling into moving average cost (OITW.AvgPrice).\n• When final carrier and customs broker AP invoices arrive, an Actual Landed Cost (OIPF DocType 'A') is posted to overwrite the estimated landed cost, adjust inventory valuation for actual variance, and reconcile the estimated clearing account (G/L 200050) to exactly $0.00.",
     "• Stage 1 (Estimate at OPDN): Dr 100010/100040 (Inventory Asset) / Cr 200050 (Estimated Landed Cost Clearing).\n• Stage 2 (Actual Overwrite at AP Invoice): Dr 200050 (Estimated Clearing) / Dr/Cr 100010/100040 (Inventory Variance) / Cr 200010 (Carrier & Broker AP).\n• Fully clears G/L 200050 balance to $0.00."),
    
    ("POLICY 6\n(Rule 6.1)", "Universal Direct AR Invoicing & Zero Outbound Delivery Notes (Customer Settlement Out of Scope)", "All Customer & Wholesale Fulfillment (Global)",
     "• Delivery Notes (ODLN) are strictly forbidden as outbound documents across ALL sales order fulfillment processes (AU domestic, NZ domestic, AU-to-NZ export, EuropeMarketPlace, and D2C Drop-Ship).\n• Outbound customer orders must generate Direct AR Tax Invoices (OINV) created directly against the Sales Order (ORDR).\n• Customer receivable settlement (Incoming Payments / ORCT) and banking cash reconciliation are strictly OUT OF SCOPE of all operational supply chain processes.\n• The Direct AR Tax Invoice (OINV) concurrently consolidates stock deduction (OnHand), COGS recognition, revenue posting, and tax into a single unified financial journal entry (OJDT), establishing the open customer receivable for downstream corporate treasury.",
     "• Outbound Rule: ORDR → Direct OINV (No ODLN permitted).\n• Final Milestone G/L Entry (OJDT):\n  Dr Accounts Receivable (110010) [Gross Incl Tax]\n  Dr Cost of Goods Sold - COGS (500010) [OnHand x AvgPrice]\n  Cr Sales Revenue (400010) [Net Price]\n  Cr GST / VAT Output Tax (200020) [Applicable Tax]\n  Cr Inventory Asset (100010/100040) [OnHand x AvgPrice]\n• Customer payment settlement (ORCT) is managed independently by corporate treasury outside the operational supply chain lifecycle."),
    
    ("POLICY 7\n(Rule 7.1)", "Mandatory Inventory Transfer Request (OWTQ) & Picking for In-Transit Movements (OWTR to SIT)", "All Warehouse-to-SIT Transfer Legs",
     "• For all stock movements transferring from a physical warehouse to a Stock-in-Transit (SIT) warehouse node (ICCSIT, NZSIT, EuropeSIT), an Inventory Transfer Request (OWTQ) must always be created first to reserve stock (OITW.IsCommited) and transmit picking instructions to the warehouse.\n• The warehouse operator completes physical picking and staging against the OWTQ.\n• Successful picking completion triggers the generation of the Inventory Transfer (OWTR) based directly on the OWTQ, executing the balance sheet transfer to In-Transit stock.",
     "• Step 1: Logistics Coordinator creates OWTQ (OITW.IsCommited = +Qty at source warehouse, no financial entry).\n• Step 2: Warehouse Operator completes physical picking & inspection.\n• Step 3: Warehouse Operator / System posts OWTR based on OWTQ: Dr 100050 (Goods In Transit Asset) / Cr 100040 (Warehouse Stock Asset), moving OnHand to SIT and clearing IsCommited."),
    
    ("POLICY 8\n(Rule 8.1)", "Zero-ODLN Architecture for Intra-Company & Cross-Database Transfers", "System Architecture (new_b1.db vs old_b1.db)",
     "• Single DB transfers (e.g. ICCChina → ICCSIT or NZNTH → NZSTH): Use native OWTQ (Picking Request) → OWTR (Stock Transfer).\n• Cross-DB transfers (e.g. ICCSIT in new_b1.db → AU Warehouse/AU Warehouse in old_b1.db): Use Origin Goods Issue (OIGE) from SIT in new_b1.db synchronized with Inbound Goods Receipt PO (OPDN) in old_b1.db (strictly bypassing ODLN).\n• Outbound customer sales in any DB: Use Direct AR Invoice (OINV) directly based on Sales Order (ORDR).",
     "• Single-DB: OWTQ (Commitment) → OWTR (Dr 100050 SIT / Cr 100040 Stock).\n• Cross-DB: Origin new_b1 posts OIGE (Dr 110020 IC AR / Cr 100050 SIT) ↔ Dest old_b1 posts OPDN (Dr 100010 Stock / Cr 200030 IC AP).\n• Customer Sales: Direct OINV based on ORDR (Dr 110010 AR / Dr 500010 COGS / Cr 400010 Rev / Cr 100010 Stock)."),
    
    ("POLICY 9\n(Rule 9.1)", "Operational RACI Governance: Role Accountability & Document Segregation", "Enterprise-Wide Governance",
     "• [Purchasing] is strictly Responsible & Accountable (R/A) for all Purchase Orders (OPOR in USD/AUD) and all Inventory/Intercompany Transfer Requests (OWTQ).\n• [Logistics] is strictly Responsible & Accountable (R/A) for all material movements, physical picking, Goods Issue (OIGE), Goods Receipt POs (OPDN), and Inventory Transfers (OWTR).\n• [Finance] is strictly Responsible & Accountable (R/A) for all Cost Accounting, Landed Cost accruals and actual overwrites (OIPF 'E'/'A'), Direct AR Invoices (OINV), and G/L clearing reconciliations (200050/100050/110020).\n• [Sales] manages Sales Orders (ORDR); [Corporate Treasury] manages Customer Settlements (ORCT) outside operational P2F scope.",
     "• Document Segregation Matrix:\n  - [Purchasing]: OPOR (POR1), OWTQ (WTQ1)\n  - [Logistics]: OWTR (WTR1), OIGE (IGE1), OPDN (PDN1)\n  - [Finance]: OIPF (IPF1/IPF2), OINV (INV1), OJDT (JDT1)\n  - [Sales]: ORDR (RDR1)\n  - [Treasury]: ORCT (RCT1 - Out of Scope)")
]

RACI_DATA = [
    ("Factory Purchase Orders", "OPOR", "USD", "Purchasing", "Accountable (A) / Responsible (R)", "Logistics (C), Finance (I), Sales (I)",
     "• [Purchasing] Issues factory purchase orders (OPOR in USD FOB) to commit vendor manufacturing.\n• Locks foreign price list (PriceFC) without generating financial entries until receipt."),
     
    ("Intercompany Inbound Purchase Orders", "OPOR", "AUD", "Purchasing", "Accountable (A) / Responsible (R)", "Logistics (C), Finance (I)",
     "• [Purchasing] Issues destination intercompany POs tracking ocean container shipments & B/L.\n• Establishes inbound on-order quantity commitment in destination ERP database."),
     
    ("Intercompany & Stock Transfer Requests", "OWTQ", "AUD", "Purchasing", "Accountable (A) / Responsible (R)", "Logistics (R), Finance (I)",
     "• [Purchasing] Generates all Inventory Transfer Requests (OWTQ) for intercompany stock rebalancing.\n• Sets source/destination warehouses and commits inventory (OITW.IsCommited) for warehouse picking queue."),
     
    ("Warehouse Picking & Staging", "OWTQ / Pick List", "N/A", "Logistics", "Accountable (A) / Responsible (R)", "Purchasing (I), Finance (I)",
     "• [Logistics] Executes physical bin/aisle picking, quantity verification, export carton labeling, and container staging against active OWTQ transfer requests."),
     
    ("Inventory Transfers to In-Transit (SIT)", "OWTR", "AUD", "Logistics", "Accountable (A) / Responsible (R)", "Purchasing (I), Finance (I)",
     "• [Logistics] Posts Inventory Transfer (OWTR) based on completed OWTQ.\n• Executes physical dispatch and balance sheet transfer: Dr 100050 SIT Asset / Cr 100040 Warehouse Stock."),
     
    ("Material Movement: Goods Issue from SIT", "OIGE", "AUD", "Logistics", "Accountable (A) / Responsible (R)", "Purchasing (I), Finance (C/I)",
     "• [Logistics] Posts Goods Issue (OIGE) discharging stock out from SIT (ICCSIT) upon ocean port arrival / vessel unlading.\n• Synchronizes with destination GRPO; origin posts Dr 110020 Intercompany AR / Cr 100050 SIT Asset."),
     
    ("Material Movement: Inbound Goods Receipt", "OPDN", "AUD", "Logistics", "Accountable (A) / Responsible (R)", "Purchasing (I), Finance (C/I)",
     "• [Logistics] Receives physical delivery at warehouse dock, performs count/quality inspection, and posts Goods Receipt PO (OPDN).\n• Dr 100010/100040 Inventory Asset / Cr 200060/200030 Goods Receipt Clearing/AP."),
     
    ("Provisional Estimated Landed Cost Accrual", "OIPF ('E')", "AUD", "Finance", "Accountable (A) / Responsible (R)", "Purchasing (C), Logistics (C)",
     "• [Finance] Posts Estimated Landed Cost (OIPF DocType 'E') immediately following every OPDN.\n• Accrues estimated freight, duty, and wharfage into inventory moving average (OITW.AvgPrice): Dr 100010/100040 / Cr 200050."),
     
    ("Actual Landed Cost Overwrite & Cost Accounting", "OIPF ('A')", "AUD", "Finance", "Accountable (A) / Responsible (R)", "Purchasing (I), Logistics (C)",
     "• [Finance] Matches actual customs broker & freight carrier AP invoices (OPCH).\n• Posts Actual Landed Cost (OIPF DocType 'A') to overwrite provisional estimates, adjust inventory valuation, and reconcile G/L 200050 to exactly $0.00."),
     
    ("Customer Sales Order Booking", "ORDR", "AUD", "Sales", "Accountable (A) / Responsible (R)", "Purchasing (I), Logistics (I), Finance (I)",
     "• [Sales] Books customer sales order (ORDR), allocating available finished goods stock (OITW.IsCommited)."),
     
    ("Direct AR Invoicing & Order Dispatch Confirmation", "OINV", "AUD", "Logistics", "Accountable (A) / Responsible (R)", "Finance (A/I - Accounting & Receivables), Sales (I)",
     "• [Logistics] Creates & posts Direct AR Tax Invoice (OINV) directly against Sales Order (ORDR) as part of the physical logistics process confirming order dispatch.\n• Concurrently executes physical stock deduction (OnHand relief), triggers automatic COGS (500010) and Revenue (400010) recognition, and establishes AR (110010) in unified journal entry."),
     
    ("Customer Payment Settlement & Banking", "ORCT", "AUD", "Corporate Treasury", "Accountable (A) / Responsible (R) [Out of Scope]", "Finance (C), Purchasing (I), Logistics (I)",
     "• [Corporate Treasury] Manages incoming customer payments, bank reconciliation, and receivable collections.\n• Explicitly OUT OF SCOPE of operational P2F supply chain value stream.")
]

INDEX_DATA = [
    ("2.1 [SNG-AU-ONLY]", "2.1.1", "Factory → AU Warehouse → AU Consumer", "old_b1.db", "Factory", "Direct B/L", "AU Warehouse", "Two-Stage Destination Landed Cost (OIPF 'E' Accrual + 'A' Overwrite)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.1 [SNG-AU-ONLY]", "2.1.2", "Factory → AU Warehouse → NZ Consumer", "old_b1.db", "Factory", "Direct Freight", "AU Warehouse", "Two-Stage AU Inward Landed Cost + Cross-Border Direct Invoicing", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.1 [SNG-AU-ONLY]", "2.1.3", "Factory → AU Warehouse → EuropeMarketPlace", "old_b1.db", "Factory", "Export Transit", "EuropeMarketPlace", "Two-Stage AU Inward Landed Cost + Long-Haul UK Freight Stack", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    
    ("2.2 [SNG-HYBRID]", "2.2.1", "Factory → ICC → AU Warehouse → AU Consumer", "new_b1 + old_b1", "ICCChina", "ICCSIT", "AU Warehouse", "Two-Stage Stacked Cost (Origin LC + Dest LC Overwrite)", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.2", "Factory → ICC → AU Warehouse → NZ Consumer", "new_b1 + old_b1", "ICCChina", "ICCSIT", "AU Warehouse", "Two-Stage Stacked Cost at AU DC + Direct Export OINV", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.3", "Factory → ICC → AU Whs → NZ Whs → NZ Consumer", "new_b1 + old_b1", "ICCChina", "ICCSIT + NZSIT", "NZNTH", "Triple-Stacked Cost: Origin LC + AU Landed + NZ Landed", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.4", "Factory → ICC → NZ Whs → AU Whs → AU Consumer", "new_b1 + old_b1", "ICCChina", "ICCSIT + NZSIT", "AU Warehouse", "Triple-Stacked Cost: Origin LC + NZ Landed + AU Landed", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.5", "Factory → AU Warehouse → NZ Warehouse → NZ Consumer", "new_b1 + old_b1", "AU Warehouse", "NZSIT", "NZNTH", "Direct AU Landed Cost + Trans-Tasman Relay at AU MWAG", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.6", "Factory → NZ Warehouse → AU Warehouse → AU Consumer", "new_b1 + old_b1", "NZNTH", "NZSIT", "AU Warehouse", "Direct NZ Landed Cost + Trans-Tasman Relay at NZ MWAG", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.7", "Factory → ICC → AU Warehouse → EuropeMarketPlace", "new_b1 + old_b1", "ICCChina", "ICCSIT + EuropeSIT", "EuropeMarketPlace", "Two-Stage Stacked at AU + Long-Haul UK Export Freight", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.8", "Factory → AU Warehouse → NZ Warehouse → EuropeMarketPlace", "new_b1 + old_b1", "AU Warehouse", "NZSIT + EuropeSIT", "EuropeMarketPlace", "AU Landed + Trans-Tasman Relay + UK Re-Export Freight", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.9", "Factory → NZ Warehouse → AU Warehouse → EuropeMarketPlace", "new_b1 + old_b1", "NZNTH", "NZSIT + EuropeSIT", "EuropeMarketPlace", "NZ Landed + Trans-Tasman Relay + UK Re-Export Freight", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.10", "Factory → ICC → AU Whs → NZ Whs → EuropeMarketPlace", "new_b1 + old_b1", "ICCChina", "ICCSIT + NZSIT + EuropeSIT", "EuropeMarketPlace", "Multi-Leg Stacked Costing Across 3 Intercompany Entities", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.2 [SNG-HYBRID]", "2.2.11", "Factory → ICC → NZ Whs → AU Whs → EuropeMarketPlace", "new_b1 + old_b1", "ICCChina", "ICCSIT + NZSIT + EuropeSIT", "EuropeMarketPlace", "Multi-Leg Stacked Costing Across 3 Intercompany Entities", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    
    ("2.3 [SNG-NEW-ONLY]", "2.3.1", "Factory → NZ Warehouse → NZ Consumer", "new_b1.db", "Factory", "Direct B/L", "NZNTH / NZSTH", "Two-Stage NZ Destination Landed Cost (OIPF 'E' Accrual + 'A' Overwrite)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.2", "Factory → ICC → NZ Warehouse → NZ Consumer", "new_b1.db", "ICCChina", "ICCSIT + NZSIT", "NZNTH / NZSTH", "Two-Stage Stacked Cost ($424 → $522 → $545 AUD)", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.3", "Factory → EuropeMarketPlace", "new_b1.db", "Factory", "Direct Voyage", "EuropeMarketPlace", "Two-Stage UK Destination Landed Cost (OIPF 'E' Accrual + 'A' Overwrite)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.4", "Factory → ICC → EuropeMarketPlace", "new_b1.db", "ICCChina", "EuropeSIT", "EuropeMarketPlace", "Two-Stage Stacked Cost ($424 → $424 → $560 AUD)", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.5", "Factory → NZ Warehouse → EuropeMarketPlace", "new_b1.db", "NZNTH", "EuropeSIT", "EuropeMarketPlace", "NZ Inbound Landed Cost + UK Maritime Re-Export Freight", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.6", "Factory → ICC → NZ Warehouse → EuropeMarketPlace", "new_b1.db", "ICCChina", "ICCSIT + EuropeSIT", "EuropeMarketPlace", "Two-Stage Stacked at NZ ($522) + UK Freight into EuropeMarketPlace ($560)", "OPOR, OPDN, OIPF, OWTQ, OWTR, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.7", "Factory → ICC → AU Consumer (D2C Air Express)", "new_b1.db", "ICCChina", "Air Courier", "AU Consumer", "Origin Staging & Drop-Ship Landed Cost (Direct Air Courier)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.8", "Factory → ICC → NZ Consumer (D2C Air Express)", "new_b1.db", "ICCChina", "Air Courier", "NZ Consumer", "Origin Staging & Drop-Ship Landed Cost (Direct Air Courier)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    ("2.3 [SNG-NEW-ONLY]", "2.3.9", "Factory → ICC → UK Consumer (D2C Air Express)", "new_b1.db", "ICCChina", "Air Courier", "UK Consumer", "Origin Staging & Drop-Ship Landed Cost (Direct Air Courier)", "OPOR, OPDN, OIPF, ORDR, OINV"),
    
    ("2.4 [SNG-EXCEPTION]", "2.4.1", "PO Changes from ICC to AU Warehouse", "new_b1 → old_b1", "ICCChina", "Direct Port", "AU Warehouses", "Cancels new_b1 PO; re-issues direct import PO in old_b1.db", "OPOR (Cancel), OPOR (New), OPDN, OIPF"),
    ("2.4 [SNG-EXCEPTION]", "2.4.2", "PO Changes from AU Warehouse to ICC", "old_b1 → new_b1", "AU Warehouse", "ICCSIT", "ICCChina → AU", "Cancels old_b1 PO; establishes multi-leg ICC PO in new_b1.db", "OPOR (Cancel), OPOR (New), OPDN, OIPF, OWTQ, OWTR"),
    ("2.4 [SNG-EXCEPTION]", "2.4.3", "Intercompany Transfer Quantity Over/Under-Supply", "new_b1 + old_b1", "ICCSIT", "Wharf / Port", "AU Warehouse / NZNTH", "Resolves variance: partial GRPO, transit loss write-off, or surplus receipt", "OPDN, OIGE (Write-Off), OIGN, OINV/OPCH Adj"),
    
    ("2.5 [SNG-RECONCILIATION]", "2.5.1", "Inventory Valuation Reconciliation", "new_b1 + old_b1", "All Hubs", "In-Transit", "Balance Sheet", "Monthly audit: Warehouse subledger (OITW) vs G/L Control (100010/100050)", "OITW, OINM, OJDT, JDT1, Trial Balance"),
    ("2.5 [SNG-RECONCILIATION]", "2.5.2", "Landed Cost Entries Reconciliation", "new_b1 + old_b1", "All Hubs", "Accrual Clearing", "G/L 200050", "Reconciles Estimated (OIPF 'E') vs Actual (OIPF 'A') broker invoices to $0", "OIPF, IPF1, IPF2, OPCH, OJDT (200050)"),
    ("2.5 [SNG-RECONCILIATION]", "2.5.3", "Group Report Reconciliation", "new_b1 + old_b1", "All Hubs", "Consolidated Ledgers", "Group Financial Statements", "Intercompany elimination, group inventory valuation consolidation, and multi-entity profit reporting", "OJDT, JDT1, OACT, Group Balance Sheet"),
    
    ("2.6 [MD-MAINTENANCE]", "2.6.1", "SAP B1 Inventory Item Master Maintenance", "new_b1 + old_b1", "Master Setup", "Warehouse Bins", "Item Master Records", "Item Code creation, valuation method setup (OITM vs OITW), purchasing/sales UoM, and barcode cataloging", "OITM, OITW, ITM1, OPLN, OWHS, OBIN"),
    ("2.6 [MD-MAINTENANCE]", "2.6.2", "SAP B1 Business Partner Master Maintenance", "new_b1 + old_b1", "Master Setup", "Commercial Ledger", "BP Master Records", "Vendor/Customer setup (OCRD/CRD1), currency assignment (USD/AUD/NZD/GBP), payment terms (OCTG), and tax group mapping", "OCRD, CRD1, OCPR, OCRG, OCTG, OSTC")
]

ALL_SECTIONS = [
    # =========================================================
    # SECTION 2.1: old_b1.db ONLY (AU DOMESTIC DC NETWORK)
    # =========================================================
    {
        "section_banner": "SECTION 2.1: old_b1.db ONLY (AU DOMESTIC DC NETWORK) — 3 Routes",
        "processes": [
            {
                "l3_banner": "Process 2.1.1: Factory → AU Warehouse → AU Consumer (Direct AU Import & Domestic Direct Invoicing)",
                "steps": [
                    ("2.1.1", "2.1.1.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ AU Warehouse → [Vendor Production Commitment]", "OPOR / POR1", "old_b1.db", "AU Warehouse",
                     "None (OnHand = 0)\n[At Vendor Site]",
                     "• Direct PO issued in USD (DocCur='USD', PriceFC=$260.00 USD)\n• POR1.OnOrder = +100 units at AU Warehouse\n• Unit Valuation: $0.00 (Purchase commitment)",
                     "Off-Balance Sheet Purchase Commitment\n(No financial journal entries in OJDT)"),
                    
                    ("2.1.1", "2.1.1.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ AU Warehouse → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse (old_b1.db)\n[OnHand = 100]",
                     "• Spot FX conversion: $260.00 USD / 0.65 DocRate = $400.00 AUD\n• Initial OITW.AvgPrice('AU Warehouse') = $400.00 AUD\n• PDN1.LineTotal = $40,000.00 AUD",
                     "Dr 100010 (Inventory Asset - AU Warehouse) $40,000.00\nCr 200010 (Goods Receipt Allocation Clearing) $40,000.00"),
                    
                    ("2.1.1", "2.1.1.3", "[Finance] Accrue Destination Estimated Landed Cost (OIPF 'E') @ AU Warehouse → [Provisional Ocean Freight & Tariff Allocation]", "OIPF (DocType 'E')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse (old_b1.db)\n[OnHand = 100]",
                     "• Inbound provisional ocean freight, AU duty & wharfage (+ $122.00 AUD/unit)\n• Provisional OITW.AvgPrice('AU Warehouse') = $400 + $122 = $522.00 AUD\n• Accrued against G/L 200050",
                     "Dr 100010 (Inventory Asset - AU Warehouse) $12,200.00\nCr 200050 (Estimated Landed Cost Clearing) $12,200.00"),
                    
                    ("2.1.1", "2.1.1.4", "[Finance] Overwrite Destination Actual Landed Cost (OIPF 'A') @ AU Warehouse → [Final Stock Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse (old_b1.db)\n[OnHand = 100]",
                     "• Overwrites provisional estimate upon carrier & customs broker invoice arrival\n• Final OITW.AvgPrice('AU Warehouse') locked at $522.00 AUD\n• Reconciles G/L 200050 clearing balance to $0.00",
                     "Dr 200050 (Estimated Landed Cost Clearing) $12,200.00\nCr 200010 (Carrier & Customs Broker AP) $12,200.00"),
                    
                    ("2.1.1", "2.1.1.5", "[Sales] Book Domestic Customer Sales Order (ORDR) @ AU Warehouse → [Finished Goods Inventory Allocation]", "ORDR / RDR1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse (old_b1.db)\n[Reserved: IsCommited = +100]",
                     "• Selling price = $850.00 AUD, stock reserved in AU Warehouse\n• Inventory unit cost remains $522.00 AUD",
                     "Sales Order Commitment\n(No financial journal entries in OJDT)"),
                    
                    ("2.1.1", "2.1.1.6", "[Logistics] Post Direct AR Tax Invoice (OINV) @ AU Warehouse → [Customer Dispatch & Revenue Recognition]", "OINV / INV1", "old_b1.db", "AU Warehouse",
                     "Customer Custody\n[AU Warehouse OnHand = 0]",
                     "• Created directly from ORDR (bypasses standalone ODLN)\n• Realized COGS: 100 x $522.00 = $52,200.00 AUD\n• Gross Revenue: $85,000 + GST ($8,500) = $93,500.00 AUD",
                     "Consolidated Inventory + Revenue Entry (OJDT):\nDr 110010 (Accounts Receivable) $93,500.00\nDr 500010 (Cost of Goods Sold - COGS) $52,200.00\nCr 400010 (Sales Revenue) $85,000.00\nCr 200020 (GST Output Tax) $8,500.00\nCr 100010 (Inventory Asset - AU Warehouse) $52,200.00")
                ]
            },
            {
                "l3_banner": "Process 2.1.2: Factory → AU Warehouse → NZ Consumer (Trans-Tasman Cross-Border Direct Invoicing)",
                "steps": [
                    ("2.1.2", "2.1.2.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ AU Warehouse → [Vendor Production Commitment]", "OPOR / POR1", "old_b1.db", "AU Warehouse",
                     "None (OnHand = 0)\n[At Vendor Site]",
                     "• Direct PO issued in USD (DocCur='USD', PriceFC=$260.00 USD)\n• POR1.OnOrder = +100 units at AU Warehouse\n• Unit Valuation: $0.00 (Purchase commitment)",
                     "Off-Balance Sheet Purchase Commitment\n(No financial journal entries in OJDT)"),
                    
                    ("2.1.2", "2.1.2.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ AU Warehouse → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse (old_b1.db)\n[OnHand = 100]",
                     "• Spot FX conversion: $260.00 USD / 0.65 DocRate = $400.00 AUD\n• Initial OITW.AvgPrice('AU Warehouse') = $400.00 AUD\n• PDN1.LineTotal = $40,000.00 AUD",
                     "Dr 100010 (Inventory Asset - AU Warehouse) $40,000.00\nCr 200010 (Goods Receipt Allocation Clearing) $40,000.00"),
                    
                    ("2.1.2", "2.1.2.3", "[Finance] Accrue Destination Estimated Landed Cost (OIPF 'E') @ AU Warehouse → [Provisional Ocean Freight & Tariff Allocation]", "OIPF (DocType 'E')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse (old_b1.db)\n[OnHand = 100]",
                     "• Inbound provisional ocean freight, AU duty & wharfage (+ $122.00 AUD/unit)\n• Provisional OITW.AvgPrice('AU Warehouse') = $400 + $122 = $522.00 AUD",
                     "Dr 100010 (Inventory Asset - AU Warehouse) $12,200.00\nCr 200050 (Estimated Landed Cost Clearing) $12,200.00"),
                    
                    ("2.1.2", "2.1.2.4", "[Finance] Overwrite Destination Actual Landed Cost (OIPF 'A') @ AU Warehouse → [Final Stock Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse (old_b1.db)\n[OnHand = 100]",
                     "• Overwrites provisional estimate upon broker invoice arrival\n• Final OITW.AvgPrice('AU Warehouse') locked at $522.00 AUD\n• Reconciles G/L 200050 clearing balance to $0.00",
                     "Dr 200050 (Estimated Landed Cost Clearing) $12,200.00\nCr 200010 (Carrier & Customs Broker AP) $12,200.00"),
                    
                    ("2.1.2", "2.1.2.5", "[Sales] Book Cross-Border Customer Sales Order (ORDR) @ AU Warehouse → [NZ Export Stock Allocation]", "ORDR / RDR1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse (old_b1.db)\n[Reserved: IsCommited = +100]",
                     "• Cross-border export price = $920.00 AUD (incl trans-tasman courier)\n• Stock reserved in AU Warehouse; Unit valuation = $522.00 AUD",
                     "Sales Order Commitment\n(No financial journal entries in OJDT)"),
                    
                    ("2.1.2", "2.1.2.6", "[Logistics] Post Direct Export AR Tax Invoice (OINV) @ AU Warehouse → [Cross-Border Dispatch & Zero-Rated Revenue Recognition]", "OINV / INV1", "old_b1.db", "AU Warehouse",
                     "Customer Custody\n[AU Warehouse OnHand = 0]",
                     "• Created directly from ORDR (bypasses standalone ODLN)\n• Realized COGS: 100 x $522.00 = $52,200.00 AUD\n• Zero-rated export revenue (GST-free) = $92,000.00 AUD",
                     "Consolidated Inventory + Export Revenue Entry (OJDT):\nDr 110010 (Accounts Receivable - Export) $92,000.00\nDr 500010 (Cost of Goods Sold - COGS) $52,200.00\nCr 400010 (Sales Revenue - Cross-Border) $92,000.00\nCr 100010 (Inventory Asset - AU Warehouse) $52,200.00")
                ]
            },
            {
                "l3_banner": "Process 2.1.3: Factory → AU Warehouse → EuropeMarketPlace (AU Hub Long-Haul Direct Wholesale Invoicing)",
                "steps": [
                    ("2.1.3", "2.1.3.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ AU Warehouse → [Vendor Production Commitment]", "OPOR / POR1", "old_b1.db", "AU Warehouse",
                     "None (OnHand = 0)", "Direct factory PO in USD ($260.00 USD @ 0.65 rate)", "Off-Balance Sheet Commitment"),
                    ("2.1.3", "2.1.3.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ AU Warehouse → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base inventory cost = $400.00 AUD", "Dr 100010 ($40,000) / Cr 200010 ($40,000)"),
                    ("2.1.3", "2.1.3.3", "[Finance] Accrue AU Inward Estimated Landed Cost (OIPF 'E') @ AU Warehouse → [Provisional Ocean Freight Allocation]", "OIPF (DocType 'E')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "AU handling (+ $122.00 AUD) → Provisional AvgPrice = $522.00 AUD", "Dr 100010 ($12,200) / Cr 200050 ($12,200)"),
                    ("2.1.3", "2.1.3.4", "[Finance] Overwrite AU Inward Actual Landed Cost (OIPF 'A') @ AU Warehouse → [AU Stock Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Overwrites estimate from broker invoices; AvgPrice = $522.00 AUD", "Dr 200050 ($12,200) / Cr 200010 ($12,200)"),
                    ("2.1.3", "2.1.3.5", "[Purchasing] Create Export Inventory Transfer Request (OWTQ) @ AU Warehouse → [UK Voyage Picking Allocation]", "OWTQ / WTQ1", "old_b1.db", "AU Warehouse → EuropeSIT",
                     "AU Warehouse [Reserved: IsCommited = +100]", "Reserves stock at AU MWAG ($522.00 AUD) and sends picking instruction to warehouse floor", "Stock Allocation Queue (No G/L entry)"),
                    ("2.1.3", "2.1.3.6", "[Logistics] Post Long-Haul Maritime Transfer (OWTR) based on OWTQ @ AU Warehouse to EuropeSIT → [UK Ocean Transit Balance Sheet Capitalization]", "OWTR / WTR1", "old_b1.db", "AU Warehouse → EuropeSIT",
                     "EuropeSIT (Transit)\n[OnHand = 100]", "Transferred at AU MWAG ($522.00 AUD); leaves AU port", "Dr 100050 (In-Transit UK) $52,200 / Cr 100010 $52,200"),
                    ("2.1.3", "2.1.3.7", "[Logistics] Post UK Port Inward GRPO (OPDN) @ EuropeMarketPlace → [UK Port Arrival Inbound Clearance]", "OPDN / PDN1", "old_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Receives stock from EuropeSIT at $522.00 AUD base cost", "Dr 100010 (EuropeMarketPlace) $52,200 / Cr 100050 (EuropeSIT) $52,200"),
                    ("2.1.3", "2.1.3.8", "[Finance] Accrue UK Port Estimated Landed Cost (OIPF 'E') @ EuropeMarketPlace → [Provisional UK Duty & Wharfage Allocation]", "OIPF (DocType 'E')", "old_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Provisional UK duty & wharfage (+ $38.00 AUD) → Cost = $560.00 AUD", "Dr 100010 (EuropeMarketPlace) $3,800 / Cr 200050 $3,800"),
                    ("2.1.3", "2.1.3.9", "[Finance] Overwrite UK Port Actual Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final UK Warehouse Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Reconciles Felixstowe broker AP invoices; locks Final AvgPrice = $560.00 AUD", "Dr 200050 ($3,800) / Cr 200010 (UK Carrier AP) $3,800"),
                    ("2.1.3", "2.1.3.10", "[Sales] Book Wholesale Customer Sales Order (ORDR) @ EuropeMarketPlace → [EuropeMarketPlace Channel Stock Allocation]", "ORDR / RDR1", "old_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale agreement: Unit Price = $750.00 AUD FOB UK", "Sales Order Commitment"),
                    ("2.1.3", "2.1.3.11", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Dispatch & Channel Revenue Recognition]", "OINV / INV1", "old_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Hub Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000, Revenue = $75,000", "Consolidated Wholesale Entry (OJDT):\nDr 110010 (AR) $75,000\nDr 500010 (COGS) $56,000\nCr 400010 (Revenue) $75,000\nCr 100010 (EuropeMarketPlace) $56,000")
                ]
            }
        ]
    },
    
    # =========================================================
    # SECTION 2.2: HYBRID DBs (CROSS-SYSTEM INTERCOMPANY & TRANS-TASMAN)
    # =========================================================
    {
        "section_banner": "SECTION 2.2: HYBRID DBs (CROSS-SYSTEM INTERCOMPANY & TRANS-TASMAN RELAY) — 11 Routes",
        "processes": [
            {
                "l3_banner": "Process 2.2.1: Factory → ICC → AU Warehouse → AU Consumer (Consolidated Multi-Leg AU Direct Invoicing)",
                "steps": [
                    ("2.2.1", "2.2.1.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)\n[At Vendor Site]", "DocCur = 'USD', PriceFC = $260.00 USD, OnOrder = +100", "Off-Balance Sheet Commitment"),
                    ("2.2.1", "2.2.1.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $260 USD / 0.65 rate = $400.00 AUD", "Dr 100040 (ICCChina) $40,000 / Cr 200060 $40,000"),
                    ("2.2.1", "2.2.1.3", "[Finance] Accrue Origin Estimated Landed Cost (OIPF 'E') @ ICCChina → [Provisional Origin Handling Allocation]", "OIPF (DocType 'E')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Origin handling (+ $24.00 AUD) → Provisional = $424.00 AUD", "Dr 100040 (ICCChina) $2,400 / Cr 200060 $2,400"),
                    ("2.2.1", "2.2.1.4", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Reconciles actual origin invoices; locks OITW.AvgPrice = $424.00 AUD", "Dr 200060 ($2,400) / Cr 200010 (Vendor AP) $2,400"),
                    ("2.2.1", "2.2.1.5", "[Purchasing] Create Inventory Transfer Request (OWTQ) @ ICCChina → [Sea Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCChina [Allocated:\nIsCommited = +100,\nOnHand = 100]", "Reserves origin stock at source MWAG ($424.00 AUD) and sends picking instruction to warehouse floor", "Warehouse Allocation Commitment\n(No financial journal entries in OJDT)"),
                    ("2.2.1", "2.2.1.6", "[Logistics] Post In-Transit Stock Transfer (OWTR) based on OWTQ @ ICCChina to ICCSIT → [Goods In-Transit Balance Sheet Capitalization]", "OWTR / WTR1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCSIT (new_b1.db)\n[On the Water:\nOnHand = 100,\nICCChina IsCommited = 0]", "Transferred at source MWAG ($424.00 AUD); moves stock to ocean transit", "Dr 100050 (In-Transit Asset - ICCSIT) $42,400.00\nCr 100040 (Inventory Asset - ICCChina) $42,400.00"),
                    ("2.2.1", "2.2.1.7", "[Purchasing] Issue Intercompany Tracking PO in AUD (OPOR) @ AU Warehouse → [Vessel Voyage & Container Inbound Tracking]", "OPOR / POR1", "old_b1.db", "AU Warehouses",
                     "AU Warehouse (old_b1.db)\n[Tracking Open PO:\nOnOrder = +100]", "old_b1: Intercompany PO issued at source MWAG ($424.00 AUD); tracks U_BOLNo, U_ContainerNo, U_ETD, U_RevisedETA", "Off-Balance Sheet Tracking Commitment\n(POR1.OnOrder = +100, no financial journal entries in OJDT)"),
                    ("2.2.1", "2.2.1.8", "[Logistics] Post Cross-DB Intercompany GRPO (OPDN) Synchronized with Origin Goods Issue (OIGE) @ AU Warehouse → [AU Port Arrival Inbound Clearance]", "OPDN (old_b1)\n↔ OIGE (new_b1)", "new_b1.db\n↔ old_b1.db", "ICCSIT → AU Warehouses",
                     "AU Warehouses\n[OnHand = 100; ICCSIT = 0]", "old_b1: Inbound OPDN closes Step 7 PO at $424.00 AUD\nnew_b1: Origin Goods Issue (OIGE) discharges ICCSIT", "Origin (new_b1): Dr 110020 (IC AR) $42,400 / Cr 100050 (SIT Asset) $42,400\nDest (old_b1): Dr 100010 (AU DC) $42,400 / Cr 200030 (IC AP) $42,400"),
                    ("2.2.1", "2.2.1.9", "[Finance] Accrue Destination Estimated Landed Cost (OIPF 'E') @ AU Warehouse → [Provisional Ocean Freight Allocation]", "OIPF (DocType 'E')", "old_b1.db", "AU Warehouses",
                     "AU Warehouses\n[OnHand = 100]", "Provisional ocean freight & duty (+ $80.00 AUD) → Cost = $504.00 AUD", "Dr 100010 (AU DC) $8,000 / Cr 200050 (Clearing) $8,000"),
                    ("2.2.1", "2.2.1.10", "[Finance] Overwrite Destination Actual Landed Cost (OIPF 'A') @ AU Warehouse → [Final Stacked Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouses",
                     "AU Warehouses\n[OnHand = 100]", "Actual carrier invoices (+ $98.00 total) → Final AvgPrice = $522.00 AUD", "Dr 100010 $1,800 / Dr 200050 $8,000 / Cr 200010 $9,800"),
                    ("2.2.1", "2.2.1.11", "[Sales] Book Domestic Customer Sales Order (ORDR) @ AU Warehouse → [Finished Goods Inventory Allocation]", "ORDR / RDR1", "old_b1.db", "AU Warehouses",
                     "AU Warehouses\n[Reserved = +100]", "Selling Price = $850.00 AUD; Inventory valuation remains $522.00 AUD", "Sales Order Commitment"),
                    ("2.2.1", "2.2.1.12", "[Logistics] Post Direct AR Tax Invoice (OINV) @ AU Warehouse → [Customer Dispatch & Revenue Recognition]", "OINV / INV1", "old_b1.db", "AU Warehouses",
                     "Customer Custody\n[AU OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $52,200 AUD, Revenue = $85,000 + GST ($8,500)", "Dr 110010 (AR) $93,500\nDr 500010 (COGS) $52,200\nCr 400010 (Revenue) $85,000\nCr 200020 (GST) $8,500\nCr 100010 (AU DC) $52,200")
                ]
            },
            {
                "l3_banner": "Process 2.2.2: Factory → ICC → AU Warehouse → NZ Consumer (Consolidated AU Hub Direct Export Invoicing)",
                "steps": [
                    ("2.2.2", "2.2.2.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)\n[At Vendor Site]",
                     "• DocCur = 'USD', PriceFC = $260.00 USD, POR1.OnOrder = +100\n• Purchase commitment in USD",
                     "Off-Balance Sheet Purchase Commitment\n(No financial journal entries in OJDT)"),
                    
                    ("2.2.2", "2.2.2.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina (new_b1.db)\n[OnHand = 100]",
                     "• Converted Base Cost = $260.00 USD / 0.65 = $400.00 AUD\n• Initial OITW.AvgPrice('ICCChina') = $400.00 AUD",
                     "Dr 100040 (Inventory Asset - ICCChina) $40,000.00\nCr 200060 (Goods Receipt Allocation Clearing) $40,000.00"),
                    
                    ("2.2.2", "2.2.2.3", "[Finance] Accrue Origin Estimated Landed Cost (OIPF 'E') @ ICCChina → [Provisional Origin Handling Allocation]", "OIPF (DocType 'E')", "new_b1.db", "ICCChina",
                     "ICCChina (new_b1.db)\n[OnHand = 100]",
                     "• Origin handling, customs & cartage (+ $24.00 AUD/unit)\n• Provisional OITW.AvgPrice = $424.00 AUD",
                     "Dr 100040 (Inventory Asset - ICCChina) $2,400.00\nCr 200060 (Origin Landed Cost Clearing) $2,400.00"),
                    
                    ("2.2.2", "2.2.2.4", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina (new_b1.db)\n[OnHand = 100]",
                     "• Reconciles actual origin broker invoices\n• Locks OITW.AvgPrice('ICCChina') = $424.00 AUD",
                     "Dr 200060 (Origin Landed Cost Clearing) $2,400.00\nCr 200010 (Origin Freight & Customs AP) $2,400.00"),
                    
                    ("2.2.2", "2.2.2.5", "[Purchasing] Create Inventory Transfer Request (OWTQ) @ ICCChina → [Sea Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCChina (new_b1.db)\n[Allocated:\nIsCommited = +100,\nOnHand = 100]",
                     "• Reserves origin stock at source MWAG ($424.00 AUD)\n• Transmits picking & staging instructions to warehouse floor",
                     "Warehouse Stock Reservation\n(No financial journal entries in OJDT)"),
                    
                    ("2.2.2", "2.2.2.6", "[Logistics] Post In-Transit Stock Transfer (OWTR) based on OWTQ @ ICCChina to ICCSIT → [Goods In-Transit Balance Sheet Capitalization]", "OWTR / WTR1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCSIT (new_b1.db)\n[On the Water:\nOnHand = 100,\nICCChina IsCommited = 0]",
                     "• new_b1: Transferred at source MWAG ($424.00 AUD)\n• Moves stock from Ningbo warehouse to ocean in-transit asset",
                     "Dr 100050 (In-Transit Asset - ICCSIT) $42,400.00\nCr 100040 (Inventory Asset - ICCChina) $42,400.00"),
                    
                    ("2.2.2", "2.2.2.7", "[Purchasing] Issue Intercompany Tracking PO in AUD (OPOR) @ AU Warehouse → [Vessel Voyage & Container Inbound Tracking]", "OPOR / POR1", "old_b1.db", "AU Warehouses",
                     "AU Warehouse (old_b1.db)\n[Tracking Open PO:\nOnOrder = +100]",
                     "• old_b1: Intercompany PO issued at source MWAG ($424.00 AUD)\n• Tracks U_BOLNo, U_ContainerNo, U_VesselVoyage, U_ETD, U_RevisedETA",
                     "Off-Balance Sheet Tracking Commitment\n(POR1.OnOrder = +100, no financial journal entries in OJDT)"),
                    
                    ("2.2.2", "2.2.2.8", "[Logistics] Post Cross-DB Intercompany GRPO (OPDN) Synchronized with Origin Goods Issue (OIGE) @ AU Warehouse → [AU Port Arrival Inbound Clearance]", "OPDN (old_b1)\n↔ OIGE (new_b1)", "new_b1.db\n↔ old_b1.db", "ICCSIT → AU Warehouses",
                     "AU Warehouses\n[OnHand = 100; ICCSIT = 0]",
                     "• old_b1: Inbound OPDN closes Step 7's Intercompany OPOR\n• Base Receipt Cost = $424.00 AUD\n• new_b1: Origin Goods Issue (OIGE) discharges ICCSIT",
                     "Origin (new_b1.db):\nDr 110020 (Intercompany AR - AU) $42,400.00\nCr 100050 (In-Transit Asset - ICCSIT) $42,400.00\n\nDest (old_b1.db):\nDr 100010 (Inventory Asset - AU DC) $42,400.00\nCr 200030 (Intercompany AP - ICC Entity) $42,400.00"),
                    
                    ("2.2.2", "2.2.2.9", "[Finance] Accrue Destination Estimated Landed Cost (OIPF 'E') @ AU Warehouse → [Provisional Ocean Freight Allocation]", "OIPF (DocType 'E')", "old_b1.db", "AU Warehouses",
                     "AU Warehouses\n[OnHand = 100]",
                     "• Provisional ocean freight & duty (+ $80.00 AUD/unit)\n• Provisional Cost = $424 + $80 = $504.00 AUD",
                     "Dr 100010 (Inventory Asset - AU DC) $8,000.00\nCr 200050 (Estimated Freight/Duty Clearing) $8,000.00"),
                    
                    ("2.2.2", "2.2.2.10", "[Finance] Overwrite Destination Actual Landed Cost (OIPF 'A') @ AU Warehouse → [Final Stacked Cost & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouses",
                     "AU Warehouses\n[OnHand = 100]",
                     "• Reconciles actual carrier invoices (+ $98.00 AUD total)\n• Stacked Moving Average = $424 + $98 = $522.00 AUD",
                     "Dr 100010 (Inventory Asset - AU DC) $1,800.00 (Variance)\nDr 200050 (Estimated Freight/Duty Clearing) $8,000.00\nCr 200010 (Customs Broker & Carrier AP) $9,800.00"),
                    
                    ("2.2.2", "2.2.2.11", "[Sales] Book Cross-Border Customer Sales Order (ORDR) @ AU Warehouse → [NZ Export Stock Allocation]", "ORDR / RDR1", "old_b1.db", "AU Warehouses",
                     "AU Warehouses\n[Reserved: IsCommited = +100]",
                     "• Cross-border export price = $920.00 AUD (incl trans-tasman courier)\n• Stock reserved in AU Warehouse; Unit valuation = $522.00 AUD",
                     "Sales Order Commitment\n(No financial journal entries in OJDT)"),
                    
                    ("2.2.2", "2.2.2.12", "[Logistics] Post Direct Export AR Tax Invoice (OINV) @ AU Warehouse → [Cross-Border Dispatch & Zero-Rated Revenue Recognition]", "OINV / INV1", "old_b1.db", "AU Warehouses",
                     "Customer Custody\n[OnHand = 0]",
                     "• Created directly from ORDR (bypasses standalone ODLN)\n• Realized COGS: 100 x $522.00 = $52,200.00 AUD\n• Zero-rated export revenue (GST-free) = $92,000.00 AUD",
                     "Consolidated Inventory + Export Revenue Entry (OJDT):\nDr 110010 (Accounts Receivable - Export) $92,000.00\nDr 500010 (Cost of Goods Sold - COGS) $52,200.00\nCr 400010 (Sales Revenue - Cross-Border) $92,000.00\nCr 100010 (Inventory Asset - AU DC) $52,200.00")
                ]
            },
            {
                "l3_banner": "Process 2.2.3: Factory → ICC → AU Whs → NZ Whs → NZ Consumer (Consolidated AU Relay to NZ DC Direct Invoicing)",
                "steps": [
                    ("2.2.3", "2.2.3.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur = 'USD', PriceFC = $260.00 USD, OnOrder = +100", "Off-Balance Sheet Commitment"),
                    ("2.2.3", "2.2.3.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.2.3", "2.2.3.3", "[Finance] Accrue Origin Estimated Landed Cost (OIPF 'E') @ ICCChina → [Provisional Origin Handling Allocation]", "OIPF (DocType 'E')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Origin handling (+ $24.00 AUD) → Provisional = $424.00 AUD", "Dr 100040 ($2,400) / Cr 200060 ($2,400)"),
                    ("2.2.3", "2.2.3.4", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Origin handling (+ $24) → AvgPrice = $424.00 AUD", "Dr 200060 ($2,400) / Cr 200010 ($2,400)"),
                    ("2.2.3", "2.2.3.5", "[Purchasing] Create Inventory Transfer Request (OWTQ) @ ICCChina → [Sea Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCChina [IsCommited = +100]", "Reserves stock at $424.00 AUD for sea voyage picking", "Stock Reservation Queue"),
                    ("2.2.3", "2.2.3.6", "[Logistics] Post In-Transit Stock Transfer (OWTR) based on OWTQ @ ICCChina to ICCSIT → [Goods In-Transit Balance Sheet Capitalization]", "OWTR / WTR1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCSIT [OnHand = 100]", "Sea transit @ $424 AUD; old_b1 tracks vessel ETA", "new_b1: Dr 100050 ($42,400) / Cr 100040 ($42,400)"),
                    ("2.2.3", "2.2.3.7", "[Purchasing] Issue Intercompany Tracking PO in AUD (OPOR) @ AU Warehouse → [AU Port Arrival Inbound Tracking]", "OPOR / POR1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnOrder = +100]", "AU tracking PO at source MWAG ($424.00 AUD)", "Off-Balance Sheet Tracking"),
                    ("2.2.3", "2.2.3.8", "[Logistics] Post Cross-DB Intercompany GRPO (OPDN) Synchronized with Origin Goods Issue (OIGE) @ AU Warehouse → [AU Port Arrival Inbound Clearance]", "OPDN (old_b1) ↔ OIGE (new_b1)", "new_b1 ↔ old_b1", "ICCSIT → AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base receipt cost = $424.00 AUD", "Origin: Dr 110020 ($42,400) / Cr 100050 ($42,400)\nDest: Dr 100010 ($42,400) / Cr 200030 (IC AP) $42,400"),
                    ("2.2.3", "2.2.3.9", "[Finance] Overwrite AU Stacked Landed Cost (OIPF 'A') @ AU Warehouse → [AU Stock Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "AU landed (+ $98) → Final AvgPrice = $522.00 AUD", "Dr 100010 ($9,800) / Cr 200010 ($9,800)"),
                    ("2.2.3", "2.2.3.10", "[Purchasing] Create Trans-Tasman Transfer Request (OWTQ) @ AU Warehouse → [NZ Voyage Picking Allocation]", "OWTQ / WTQ1", "old_b1.db", "AU Warehouse → NZSIT",
                     "AU Warehouse [IsCommited = +100]", "Trans-Tasman picking reservation at $522.00 AUD", "Stock Allocation Queue"),
                    ("2.2.3", "2.2.3.11", "[Logistics] Post Trans-Tasman Stock Transfer (OWTR) based on OWTQ @ AU Warehouse to NZSIT → [Trans-Tasman Sea Voyage Tracking]", "OWTR / WTR1", "old_b1 & new_b1", "AU Warehouse → NZSIT",
                     "NZSIT [OnHand = 100]", "Transferred at AU MWAG ($522.00 AUD)", "old_b1: Dr 110020 (IC AR) $52,200 / Cr 100010 $52,200"),
                    ("2.2.3", "2.2.3.12", "[Logistics] Post NZ Inward Intercompany GRPO (OPDN) @ NZNTH → [NZ Port Arrival Inbound Clearance]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Dr 100040 (NZNTH) $52,200 / Cr 200030 (IC AP) $52,200"),
                    ("2.2.3", "2.2.3.13", "[Finance] Capitalize NZ Inbound Landed Cost (OIPF 'A') @ NZNTH → [Final Stacked Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Trans-Tasman freight & duty (+ $23 AUD) → AvgPrice = $545.00 AUD", "Dr 100040 (NZNTH) $2,300 / Cr 200010 ($2,300)"),
                    ("2.2.3", "2.2.3.14", "[Sales] Book Domestic NZ Customer Sales Order (ORDR) @ NZNTH → [NZ Domestic Stock Allocation]", "ORDR / RDR1", "new_b1.db", "NZNTH",
                     "NZNTH [Reserved = +100]", "Domestic NZ customer sales order", "Sales Order Commitment"),
                    ("2.2.3", "2.2.3.15", "[Logistics] Post Direct AR Tax Invoice (OINV) @ NZNTH → [Domestic NZ Customer Dispatch & Revenue Recognition]", "OINV / INV1", "new_b1.db", "NZNTH",
                     "Customer Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $54,500 AUD, Revenue = $95,000", "Consolidated Entry (OJDT):\nDr 110010 (AR NZ) $95,000\nDr 500010 (COGS NZ) $54,500\nCr 400010 (Revenue) $95,000\nCr 100040 (NZNTH) $54,500")
                ]
            },
            {
                "l3_banner": "Process 2.2.4: Factory → ICC → NZ Whs → AU Whs → AU Consumer (Consolidated NZ Relay to AU DC Direct Invoicing)",
                "steps": [
                    ("2.2.4", "2.2.4.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur = 'USD', PriceFC = $260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.2.4", "2.2.4.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.2.4", "2.2.4.3", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Origin capitalized cost = $424.00 AUD", "Dr 100040 ($2,400) / Cr 200010 ($2,400)"),
                    ("2.2.4", "2.2.4.4", "[Purchasing] Create Inventory Transfer Request (OWTQ) @ ICCChina → [NZ Sea Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCChina [IsCommited = +100]", "Reserves origin stock at $424.00 AUD", "Stock Reservation Queue"),
                    ("2.2.4", "2.2.4.5", "[Logistics] Post In-Transit Stock Transfer (OWTR) based on OWTQ @ ICCChina to ICCSIT → [Ocean Transit Balance Sheet Capitalization]", "OWTR / WTR1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCSIT [OnHand = 100]", "Sea transit @ $424.00 AUD", "Dr 100050 ($42,400) / Cr 100040 ($42,400)"),
                    ("2.2.4", "2.2.4.6", "[Logistics] Post NZ Inward GRPO (OPDN) @ NZNTH → [NZ Port Arrival Clearance]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base receipt cost = $424.00 AUD", "Dr 100040 ($42,400) / Cr 100050 ($42,400)"),
                    ("2.2.4", "2.2.4.7", "[Finance] Overwrite NZ Destination Landed Cost (OIPF 'A') @ NZNTH → [NZ Regional Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "NZ DC unit moving average = $522.00 AUD", "Dr 100040 ($9,800) / Cr 200010 ($9,800)"),
                    ("2.2.4", "2.2.4.8", "[Purchasing] Create Reverse Trans-Tasman Transfer Request (OWTQ) @ NZNTH → [AU Relay Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "NZNTH → NZSIT",
                     "NZNTH [IsCommited = +100]", "Reserves NZ DC stock at $522.00 AUD", "Stock Allocation Queue"),
                    ("2.2.4", "2.2.4.9", "[Logistics] Post Reverse Trans-Tasman Transfer (OWTR) based on OWTQ @ NZNTH to NZSIT → [Maritime Relay Tracking]", "OWTR / WTR1", "new_b1 & old_b1", "NZNTH → NZSIT",
                     "NZSIT [OnHand = 100]", "Transferred at NZ MWAG ($522.00 AUD)", "new_b1: Dr 110020 (IC AR) $52,200 / Cr 100040 $52,200"),
                    ("2.2.4", "2.2.4.10", "[Logistics] Post AU Cross-DB Intercompany GRPO (OPDN) Synchronized with Origin Goods Issue (OIGE) @ AU Warehouse → [AU Port Inbound Clearance]", "OPDN (old_b1) ↔ OIGE (new_b1)", "new_b1 ↔ old_b1", "NZSIT → AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Origin: Dr 110020 ($52,200) / Cr 100050 ($52,200)\nDest: Dr 100010 ($52,200) / Cr 200030 ($52,200)"),
                    ("2.2.4", "2.2.4.11", "[Finance] Overwrite AU Inbound Landed Cost (OIPF 'A') @ AU Warehouse → [Final AU Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Trans-Tasman freight (+ $23 AUD) → Final AvgPrice = $545.00 AUD", "Dr 100010 ($2,300) / Cr 200010 ($2,300)"),
                    ("2.2.4", "2.2.4.12", "[Sales] Book Domestic Customer Sales Order (ORDR) @ AU Warehouse → [Finished Goods Inventory Allocation]", "ORDR / RDR1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [Reserved = +100]", "Order booked at $850.00 AUD", "Sales Order Commitment"),
                    ("2.2.4", "2.2.4.13", "[Logistics] Post Direct AR Tax Invoice (OINV) @ AU Warehouse → [Customer Dispatch & Revenue Recognition]", "OINV / INV1", "old_b1.db", "AU Warehouse",
                     "Customer Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $54,500 AUD, Revenue = $85,000 + GST", "Dr 110010 ($93,500) / Dr 500010 ($54,500) / Cr 400010 ($85,000) / Cr 200020 ($8,500) / Cr 100010 ($54,500)")
                ]
            },
            {
                "l3_banner": "Process 2.2.5: Factory → AU Warehouse → NZ Warehouse → NZ Consumer (Direct AU Hub to NZ DC Direct Invoicing)",
                "steps": [
                    ("2.2.5", "2.2.5.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ AU Warehouse → [Vendor Production Commitment]", "OPOR / POR1", "old_b1.db", "AU Warehouse",
                     "None (OnHand = 0)", "DocCur = 'USD', PriceFC = $260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.2.5", "2.2.5.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ AU Warehouse → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base inventory cost = $400.00 AUD @ 0.65 rate", "Dr 100010 ($40,000) / Cr 200010 ($40,000)"),
                    ("2.2.5", "2.2.5.3", "[Finance] Overwrite AU Destination Landed Cost (OIPF 'A') @ AU Warehouse → [AU DC Stock Capitalization]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Direct AU landed cost = $522.00 AUD", "Dr 100010 ($12,200) / Cr 200010 ($12,200)"),
                    ("2.2.5", "2.2.5.4", "[Purchasing] Create Trans-Tasman Transfer Request (OWTQ) @ AU Warehouse → [NZ Relay Picking Allocation]", "OWTQ / WTQ1", "old_b1.db", "AU Warehouse → NZSIT",
                     "AU Warehouse [IsCommited = +100]", "Reserves stock at AU MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.5", "2.2.5.5", "[Logistics] Post Trans-Tasman Transfer (OWTR) based on OWTQ @ AU Warehouse to NZSIT → [Maritime Transit Tracking]", "OWTR / WTR1", "old_b1 & new_b1", "AU Warehouse → NZSIT",
                     "NZSIT [OnHand = 100]", "Transferred at AU MWAG ($522.00 AUD)", "old_b1: Dr 110020 ($52,200) / Cr 100010 ($52,200)"),
                    ("2.2.5", "2.2.5.6", "[Logistics] Post NZ Inward Intercompany GRPO (OPDN) @ NZNTH → [Port Arrival Inbound Clearance]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Dr 100040 (NZNTH) $52,200 / Cr 200030 (IC AP) $52,200"),
                    ("2.2.5", "2.2.5.7", "[Finance] Capitalize NZ Inbound Landed Cost (OIPF 'A') @ NZNTH → [Final Stacked Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Trans-Tasman freight (+ $23 AUD) → AvgPrice = $545.00 AUD", "Dr 100040 (NZNTH) $2,300 / Cr 200010 ($2,300)"),
                    ("2.2.5", "2.2.5.8", "[Sales] Book Domestic NZ Sales Order (ORDR) @ NZNTH → [NZ Customer Stock Allocation]", "ORDR / RDR1", "new_b1.db", "NZNTH",
                     "NZNTH [Reserved = +100]", "Domestic sales order booking", "Sales Order Commitment"),
                    ("2.2.5", "2.2.5.9", "[Logistics] Post Direct AR Tax Invoice (OINV) @ NZNTH → [Domestic Customer Dispatch & Revenue Recognition]", "OINV / INV1", "new_b1.db", "NZNTH",
                     "Customer Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $54,500 AUD, Revenue = $95,000", "Dr 110010 (AR) $95,000 / Dr 500010 (COGS) $54,500 / Cr 400010 (Revenue) $95,000 / Cr 100040 ($54,500)")
                ]
            },
            {
                "l3_banner": "Process 2.2.6: Factory → NZ Warehouse → AU Warehouse → AU Consumer (Direct NZ Hub to AU DC Direct Invoicing)",
                "steps": [
                    ("2.2.6", "2.2.6.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ NZNTH → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "NZNTH",
                     "None (OnHand = 0)", "DocCur = 'USD', PriceFC = $260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.2.6", "2.2.6.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ NZNTH → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base inventory cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.2.6", "2.2.6.3", "[Finance] Overwrite NZ Destination Landed Cost (OIPF 'A') @ NZNTH → [NZ DC Stock Capitalization]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Direct NZ landed cost = $522.00 AUD", "Dr 100040 ($12,200) / Cr 200010 ($12,200)"),
                    ("2.2.6", "2.2.6.4", "[Purchasing] Create Reverse Trans-Tasman Transfer Request (OWTQ) @ NZNTH → [AU Relay Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "NZNTH → NZSIT",
                     "NZNTH [IsCommited = +100]", "Reserves stock at NZ MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.6", "2.2.6.5", "[Logistics] Post Reverse Trans-Tasman Transfer (OWTR) based on OWTQ @ NZNTH to NZSIT → [Maritime Transit Tracking]", "OWTR / WTR1", "new_b1 & old_b1", "NZNTH → NZSIT",
                     "NZSIT [OnHand = 100]", "Transferred at NZ MWAG ($522.00 AUD)", "new_b1: Dr 110020 ($52,200) / Cr 100040 ($52,200)"),
                    ("2.2.6", "2.2.6.6", "[Logistics] Post AU Inward Intercompany GRPO (OPDN) @ AU Warehouse → [Port Arrival Inbound Clearance]", "OPDN / PDN1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Dr 100010 (AU Warehouse) $52,200 / Cr 200030 (IC AP) $52,200"),
                    ("2.2.6", "2.2.6.7", "[Finance] Capitalize AU Inbound Landed Cost (OIPF 'A') @ AU Warehouse → [Final Stacked Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Trans-Tasman freight (+ $23 AUD) → Final AvgPrice = $545.00 AUD", "Dr 100010 (AU Warehouse) $2,300 / Cr 200010 ($2,300)"),
                    ("2.2.6", "2.2.6.8", "[Sales] Book Domestic Customer Sales Order (ORDR) @ AU Warehouse → [AU Customer Stock Allocation]", "ORDR / RDR1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [Reserved = +100]", "Domestic sales order booking", "Sales Order Commitment"),
                    ("2.2.6", "2.2.6.9", "[Logistics] Post Direct AR Tax Invoice (OINV) @ AU Warehouse → [Customer Dispatch & Revenue Recognition]", "OINV / INV1", "old_b1.db", "AU Warehouse",
                     "Customer Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $54,500 AUD, Revenue = $85,000 + GST", "Dr 110010 ($93,500) / Dr 500010 ($54,500) / Cr 400010 ($85,000) / Cr 200020 ($8,500) / Cr 100010 ($54,500)")
                ]
            },
            {
                "l3_banner": "Process 2.2.7: Factory → ICC → AU Warehouse → EuropeMarketPlace (Consolidated AU Re-Export Direct Invoicing)",
                "steps": [
                    ("2.2.7", "2.2.7.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.2.7", "2.2.7.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.2.7", "2.2.7.3", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Origin handling (+ $24.00 AUD) → AvgPrice = $424.00 AUD", "Dr 100040 ($2,400) / Cr 200010 ($2,400)"),
                    ("2.2.7", "2.2.7.4", "[Purchasing] Create Inventory Transfer Request (OWTQ) @ ICCChina → [AU Sea Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCChina [IsCommited = +100]", "Reserves stock at $424.00 AUD", "Stock Reservation Queue"),
                    ("2.2.7", "2.2.7.5", "[Logistics] Post In-Transit Stock Transfer (OWTR) based on OWTQ @ ICCChina to ICCSIT → [Goods In-Transit Balance Sheet Capitalization]", "OWTR / WTR1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCSIT [OnHand = 100]", "Capitalized origin cost = $424.00 AUD", "Dr 100050 ($42,400) / Cr 100040 ($42,400)"),
                    ("2.2.7", "2.2.7.6", "[Logistics] Post AU Port Intercompany GRPO (OPDN) Synchronized with Origin Goods Issue (OIGE) @ AU Warehouse → [AU Port Inbound Clearance]", "OPDN ↔ OIGE", "new_b1 ↔ old_b1", "ICCSIT → AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base receipt cost = $424.00 AUD", "Origin: Dr 110020 ($42,400) / Cr 100050 ($42,400)\nDest: Dr 100010 ($42,400) / Cr 200030 ($42,400)"),
                    ("2.2.7", "2.2.7.7", "[Finance] Overwrite AU Destination Landed Cost (OIPF 'A') @ AU Warehouse → [AU Stock Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "AU DC moving average = $522.00 AUD", "Dr 100010 ($9,800) / Cr 200010 ($9,800)"),
                    ("2.2.7", "2.2.7.8", "[Purchasing] Create UK Export Transfer Request (OWTQ) @ AU Warehouse → [UK Voyage Picking Allocation]", "OWTQ / WTQ1", "old_b1.db", "AU Warehouse → EuropeSIT",
                     "AU Warehouse [IsCommited = +100]", "Reserves stock at AU MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.7", "2.2.7.9", "[Logistics] Post Re-Export Maritime Transfer (OWTR) based on OWTQ @ AU Warehouse to EuropeSIT → [UK Transit Voyage Tracking]", "OWTR / WTR1", "old_b1.db", "AU Warehouse → EuropeSIT",
                     "EuropeSIT [OnHand = 100]", "Transferred at AU MWAG ($522.00 AUD)", "Dr 100050 (In-Transit UK) $52,200 / Cr 100010 ($52,200)"),
                    ("2.2.7", "2.2.7.10", "[Logistics] Post UK Inward GRPO (OPDN) @ EuropeMarketPlace → [UK Port Arrival Inbound Clearance]", "OPDN / PDN1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Dr 100040 (EuropeMarketPlace) $52,200 / Cr 100050 ($52,200)"),
                    ("2.2.7", "2.2.7.11", "[Finance] Capitalize UK Port Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final Stacked Cost & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "UK port duty & cartage (+ $38 AUD) → Final AvgPrice = $560.00 AUD", "Dr 100040 (EuropeMarketPlace) $3,800 / Cr 200010 ($3,800)"),
                    ("2.2.7", "2.2.7.12", "[Sales] Book Wholesale Sales Order (ORDR) @ EuropeMarketPlace → [EuropeMarketPlace Channel Allocation]", "ORDR / RDR1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale order booking @ $750.00 AUD", "Sales Order Commitment"),
                    ("2.2.7", "2.2.7.13", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Channel Revenue Recognition]", "OINV / INV1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000 AUD, Revenue = $75,000", "Dr 110010 (AR) $75,000 / Dr 500010 (COGS UK) $56,000 / Cr 400010 (Revenue) $75,000 / Cr 100040 (EuropeMarketPlace) $56,000")
                ]
            },
            {
                "l3_banner": "Process 2.2.8: Factory → AU Warehouse → NZ Warehouse → EuropeMarketPlace (AU to NZ Transshipment Direct Invoicing)",
                "steps": [
                    ("2.2.8", "2.2.8.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ AU Warehouse → [Vendor Production Commitment]", "OPOR / POR1", "old_b1.db", "AU Warehouse",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.2.8", "2.2.8.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ AU Warehouse → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100010 ($40,000) / Cr 200010 ($40,000)"),
                    ("2.2.8", "2.2.8.3", "[Finance] Overwrite AU Landed Cost (OIPF 'A') @ AU Warehouse → [Direct AU DC Capitalization]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Direct AU landed cost = $522.00 AUD", "Dr 100010 ($12,200) / Cr 200010 ($12,200)"),
                    ("2.2.8", "2.2.8.4", "[Purchasing] Create Trans-Tasman Transfer Request (OWTQ) @ AU Warehouse → [NZ Relay Picking Allocation]", "OWTQ / WTQ1", "old_b1.db", "AU Warehouse → NZSIT",
                     "AU Warehouse [IsCommited = +100]", "Reserves stock at AU MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.8", "2.2.8.5", "[Logistics] Post Trans-Tasman Relay Transfer (OWTR) based on OWTQ @ AU Warehouse to NZSIT → [Trans-Tasman Sea Voyage Tracking]", "OWTR / WTR1", "old_b1 & new_b1", "AU Warehouse → NZSIT",
                     "NZSIT [OnHand = 100]", "Transferred at AU MWAG ($522.00 AUD)", "old_b1: Dr 110020 ($52,200) / Cr 100010 ($52,200)"),
                    ("2.2.8", "2.2.8.6", "[Logistics] Post NZ Inward Intercompany GRPO (OPDN) @ NZNTH → [NZ Port Arrival Clearance]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Dr 100040 (NZNTH) $52,200 / Cr 200030 ($52,200)"),
                    ("2.2.8", "2.2.8.7", "[Finance] Capitalize NZ Landed Cost (OIPF 'A') @ NZNTH → [NZ Regional Moving Average Lock]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Trans-Tasman landed cost at NZ = $545.00 AUD", "Dr 100040 (NZNTH) $2,300 / Cr 200010 ($2,300)"),
                    ("2.2.8", "2.2.8.8", "[Purchasing] Create UK Export Transfer Request (OWTQ) @ NZNTH → [UK Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "NZNTH → EuropeSIT",
                     "NZNTH [IsCommited = +100]", "Reserves stock at NZ MWAG ($545.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.8", "2.2.8.9", "[Logistics] Post UK Maritime Transfer (OWTR) based on OWTQ @ NZNTH to EuropeSIT → [Long-Haul Transit Tracking]", "OWTR / WTR1", "new_b1.db", "NZNTH → EuropeSIT",
                     "EuropeSIT [OnHand = 100]", "Transferred at NZ MWAG ($545.00 AUD)", "Dr 100050 (EuropeSIT) $54,500 / Cr 100040 ($54,500)"),
                    ("2.2.8", "2.2.8.10", "[Logistics] Post UK Inward GRPO (OPDN) @ EuropeMarketPlace → [UK Port Arrival Clearance]", "OPDN / PDN1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Base receipt cost = $545.00 AUD", "Dr 100040 (EuropeMarketPlace) $54,500 / Cr 100050 ($54,500)"),
                    ("2.2.8", "2.2.8.11", "[Finance] Capitalize UK Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final Stacked Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "UK duty & handling (+ $15 AUD) → Final AvgPrice = $560.00 AUD", "Dr 100040 (EuropeMarketPlace) $1,500 / Cr 200010 ($1,500)"),
                    ("2.2.8", "2.2.8.12", "[Sales] Book Wholesale Sales Order (ORDR) @ EuropeMarketPlace → [EuropeMarketPlace Channel Allocation]", "ORDR / RDR1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale agreement @ $750.00 AUD", "Sales Order Commitment"),
                    ("2.2.8", "2.2.8.13", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Channel Revenue Recognition]", "OINV / INV1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000, Revenue = $75,000", "Dr 110010 ($75,000) / Dr 500010 ($56,000) / Cr 400010 ($75,000) / Cr 100040 ($56,000)")
                ]
            },
            {
                "l3_banner": "Process 2.2.9: Factory → NZ Warehouse → AU Warehouse → EuropeMarketPlace (NZ to AU Transshipment Direct Invoicing)",
                "steps": [
                    ("2.2.9", "2.2.9.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ NZNTH → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "NZNTH",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.2.9", "2.2.9.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ NZNTH → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.2.9", "2.2.9.3", "[Finance] Overwrite NZ Landed Cost (OIPF 'A') @ NZNTH → [Direct NZ DC Capitalization]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Direct NZ landed cost = $522.00 AUD", "Dr 100040 ($12,200) / Cr 200010 ($12,200)"),
                    ("2.2.9", "2.2.9.4", "[Purchasing] Create Reverse Trans-Tasman Transfer Request (OWTQ) @ NZNTH → [AU Relay Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "NZNTH → NZSIT",
                     "NZNTH [IsCommited = +100]", "Reserves stock at NZ MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.9", "2.2.9.5", "[Logistics] Post Reverse Trans-Tasman Relay Transfer (OWTR) based on OWTQ @ NZNTH to NZSIT → [Trans-Tasman Sea Voyage Tracking]", "OWTR / WTR1", "new_b1 & old_b1", "NZNTH → NZSIT",
                     "NZSIT [OnHand = 100]", "Transferred at NZ MWAG ($522.00 AUD)", "new_b1: Dr 110020 ($52,200) / Cr 100040 ($52,200)"),
                    ("2.2.9", "2.2.9.6", "[Logistics] Post AU Inward Intercompany GRPO (OPDN) @ AU Warehouse → [AU Port Arrival Clearance]", "OPDN / PDN1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Dr 100010 (AU Warehouse) $52,200 / Cr 200030 ($52,200)"),
                    ("2.2.9", "2.2.9.7", "[Finance] Capitalize AU Landed Cost (OIPF 'A') @ AU Warehouse → [AU Regional Moving Average Lock]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Trans-Tasman landed cost at AU = $545.00 AUD", "Dr 100010 (AU Warehouse) $2,300 / Cr 200010 ($2,300)"),
                    ("2.2.9", "2.2.9.8", "[Purchasing] Create UK Export Transfer Request (OWTQ) @ AU Warehouse → [UK Voyage Picking Allocation]", "OWTQ / WTQ1", "old_b1.db", "AU Warehouse → EuropeSIT",
                     "AU Warehouse [IsCommited = +100]", "Reserves stock at AU MWAG ($545.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.9", "2.2.9.9", "[Logistics] Post UK Maritime Transfer (OWTR) based on OWTQ @ AU Warehouse to EuropeSIT → [Long-Haul Transit Tracking]", "OWTR / WTR1", "old_b1.db", "AU Warehouse → EuropeSIT",
                     "EuropeSIT [OnHand = 100]", "Transferred at AU MWAG ($545.00 AUD)", "Dr 100050 (EuropeSIT) $54,500 / Cr 100010 ($54,500)"),
                    ("2.2.9", "2.2.9.10", "[Logistics] Post UK Inward GRPO (OPDN) @ EuropeMarketPlace → [UK Port Arrival Clearance]", "OPDN / PDN1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Base receipt cost = $545.00 AUD", "Dr 100040 (EuropeMarketPlace) $54,500 / Cr 100050 ($54,500)"),
                    ("2.2.9", "2.2.9.11", "[Finance] Capitalize UK Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final Stacked Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "UK duty & handling (+ $15 AUD) → Final AvgPrice = $560.00 AUD", "Dr 100040 (EuropeMarketPlace) $1,500 / Cr 200010 ($1,500)"),
                    ("2.2.9", "2.2.9.12", "[Sales] Book Wholesale Sales Order (ORDR) @ EuropeMarketPlace → [EuropeMarketPlace Channel Allocation]", "ORDR / RDR1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale agreement @ $750.00 AUD", "Sales Order Commitment"),
                    ("2.2.9", "2.2.9.13", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Channel Revenue Recognition]", "OINV / INV1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000, Revenue = $75,000", "Dr 110010 ($75,000) / Dr 500010 ($56,000) / Cr 400010 ($75,000) / Cr 100040 ($56,000)")
                ]
            },
            {
                "l3_banner": "Process 2.2.10: Factory → ICC → AU Whs → NZ Whs → EuropeMarketPlace (Multi-Hub Intercompany Re-Export Direct Invoicing)",
                "steps": [
                    ("2.2.10", "2.2.10.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.2.10", "2.2.10.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.2.10", "2.2.10.3", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Capitalized origin cost = $424.00 AUD", "Dr 100040 ($2,400) / Cr 200010 ($2,400)"),
                    ("2.2.10", "2.2.10.4", "[Purchasing] Create Inventory Transfer Request (OWTQ) @ ICCChina → [Sea Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCChina [IsCommited = +100]", "Reserves stock at $424.00 AUD", "Stock Reservation Queue"),
                    ("2.2.10", "2.2.10.5", "[Logistics] Post In-Transit Stock Transfer (OWTR) based on OWTQ @ ICCChina to ICCSIT → [Goods In-Transit Balance Sheet Capitalization]", "OWTR / WTR1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCSIT [OnHand = 100]", "Sea transit @ $424.00 AUD", "Dr 100050 ($42,400) / Cr 100040 ($42,400)"),
                    ("2.2.10", "2.2.10.6", "[Logistics] Post AU Port Intercompany GRPO (OPDN) Synchronized with Origin Goods Issue (OIGE) @ AU Warehouse → [AU Port Arrival Inbound Clearance]", "OPDN ↔ OIGE", "new_b1 ↔ old_b1", "ICCSIT → AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base receipt cost = $424.00 AUD", "Origin: Dr 110020 ($42,400) / Cr 100050 ($42,400)\nDest: Dr 100010 ($42,400) / Cr 200030 ($42,400)"),
                    ("2.2.10", "2.2.10.7", "[Finance] Overwrite AU Destination Landed Cost (OIPF 'A') @ AU Warehouse → [AU DC Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "AU DC moving average = $522.00 AUD", "Dr 100010 ($9,800) / Cr 200010 ($9,800)"),
                    ("2.2.10", "2.2.10.8", "[Purchasing] Create Trans-Tasman Transfer Request (OWTQ) @ AU Warehouse → [NZ Relay Picking Allocation]", "OWTQ / WTQ1", "old_b1.db", "AU Warehouse → NZSIT",
                     "AU Warehouse [IsCommited = +100]", "Reserves stock at AU MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.10", "2.2.10.9", "[Logistics] Post Trans-Tasman Relay Transfer (OWTR) based on OWTQ @ AU Warehouse to NZSIT → [Regional Transit Tracking]", "OWTR / WTR1", "old_b1 & new_b1", "AU Warehouse → NZSIT",
                     "NZSIT [OnHand = 100]", "Transferred at AU MWAG ($522.00 AUD)", "old_b1: Dr 110020 ($52,200) / Cr 100010 ($52,200)"),
                    ("2.2.10", "2.2.10.10", "[Logistics] Post NZ Inward Intercompany GRPO (OPDN) @ NZNTH → [NZ Port Arrival Clearance]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Dr 100040 (NZNTH) $52,200 / Cr 200030 ($52,200)"),
                    ("2.2.10", "2.2.10.11", "[Finance] Capitalize NZ Landed Cost (OIPF 'A') @ NZNTH → [NZ DC Moving Average Lock]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "NZ DC moving average = $545.00 AUD", "Dr 100040 (NZNTH) $2,300 / Cr 200010 ($2,300)"),
                    ("2.2.10", "2.2.10.12", "[Purchasing] Create UK Export Transfer Request (OWTQ) @ NZNTH → [UK Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "NZNTH → EuropeSIT",
                     "NZNTH [IsCommited = +100]", "Reserves stock at NZ MWAG ($545.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.10", "2.2.10.13", "[Logistics] Post UK Maritime Transfer (OWTR) based on OWTQ @ NZNTH to EuropeSIT → [Long-Haul Transit Tracking]", "OWTR / WTR1", "new_b1.db", "NZNTH → EuropeSIT",
                     "EuropeSIT [OnHand = 100]", "Transferred at NZ MWAG ($545.00 AUD)", "Dr 100050 (EuropeSIT) $54,500 / Cr 100040 ($54,500)"),
                    ("2.2.10", "2.2.10.14", "[Logistics] Post UK Inward GRPO (OPDN) @ EuropeMarketPlace → [UK Port Arrival Inbound Clearance]", "OPDN / PDN1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Base receipt cost = $545.00 AUD", "Dr 100040 (EuropeMarketPlace) $54,500 / Cr 100050 ($54,500)"),
                    ("2.2.10", "2.2.10.15", "[Finance] Capitalize UK Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final Stacked Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Final stacked cost = $560.00 AUD", "Dr 100040 (EuropeMarketPlace) $1,500 / Cr 200010 ($1,500)"),
                    ("2.2.10", "2.2.10.16", "[Sales] Book Wholesale Sales Order (ORDR) @ EuropeMarketPlace → [EuropeMarketPlace Channel Allocation]", "ORDR / RDR1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale agreement @ $750.00 AUD", "Sales Order Commitment"),
                    ("2.2.10", "2.2.10.17", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Channel Revenue Recognition]", "OINV / INV1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000, Revenue = $75,000", "Dr 110010 ($75,000) / Dr 500010 ($56,000) / Cr 400010 ($75,000) / Cr 100040 ($56,000)")
                ]
            },
            {
                "l3_banner": "Process 2.2.11: Factory → ICC → NZ Whs → AU Whs → EuropeMarketPlace (Multi-Hub Intercompany Re-Export Direct Invoicing)",
                "steps": [
                    ("2.2.11", "2.2.11.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.2.11", "2.2.11.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.2.11", "2.2.11.3", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Capitalized origin cost = $424.00 AUD", "Dr 100040 ($2,400) / Cr 200010 ($2,400)"),
                    ("2.2.11", "2.2.11.4", "[Purchasing] Create Inventory Transfer Request (OWTQ) @ ICCChina → [NZ Sea Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCChina [IsCommited = +100]", "Reserves stock at $424.00 AUD", "Stock Reservation Queue"),
                    ("2.2.11", "2.2.11.5", "[Logistics] Post In-Transit Stock Transfer (OWTR) based on OWTQ @ ICCChina to ICCSIT → [Goods In-Transit Balance Sheet Capitalization]", "OWTR / WTR1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCSIT [OnHand = 100]", "Sea transit @ $424.00 AUD", "Dr 100050 ($42,400) / Cr 100040 ($42,400)"),
                    ("2.2.11", "2.2.11.6", "[Logistics] Post NZ Port GRPO (OPDN) @ NZNTH → [NZ Port Arrival Inbound Clearance]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base receipt cost = $424.00 AUD", "Dr 100040 ($42,400) / Cr 100050 ($42,400)"),
                    ("2.2.11", "2.2.11.7", "[Finance] Overwrite NZ Destination Landed Cost (OIPF 'A') @ NZNTH → [NZ DC Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "NZ DC moving average = $522.00 AUD", "Dr 100040 ($9,800) / Cr 200010 ($9,800)"),
                    ("2.2.11", "2.2.11.8", "[Purchasing] Create Reverse Trans-Tasman Transfer Request (OWTQ) @ NZNTH → [AU Relay Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "NZNTH → NZSIT",
                     "NZNTH [IsCommited = +100]", "Reserves stock at NZ MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.11", "2.2.11.9", "[Logistics] Post Reverse Trans-Tasman Relay Transfer (OWTR) based on OWTQ @ NZNTH to NZSIT → [Regional Transit Tracking]", "OWTR / WTR1", "new_b1 & old_b1", "NZNTH → NZSIT",
                     "NZSIT [OnHand = 100]", "Transferred at NZ MWAG ($522.00 AUD)", "new_b1: Dr 110020 ($52,200) / Cr 100040 ($52,200)"),
                    ("2.2.11", "2.2.11.10", "[Logistics] Post AU Cross-DB Intercompany GRPO (OPDN) Synchronized with Origin Goods Issue (OIGE) @ AU Warehouse → [AU Port Inbound Clearance]", "OPDN (old_b1) ↔ OIGE (new_b1)", "new_b1 ↔ old_b1", "NZSIT → AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Origin: Dr 110020 ($52,200) / Cr 100050 ($52,200)\nDest: Dr 100010 ($52,200) / Cr 200030 ($52,200)"),
                    ("2.2.11", "2.2.11.11", "[Finance] Overwrite AU Landed Cost (OIPF 'A') @ AU Warehouse → [AU DC Moving Average Lock]", "OIPF (DocType 'A')", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand = 100]", "AU DC moving average = $545.00 AUD", "Dr 100010 (AU Warehouse) $2,300 / Cr 200010 ($2,300)"),
                    ("2.2.11", "2.2.11.12", "[Purchasing] Create UK Export Transfer Request (OWTQ) @ AU Warehouse → [UK Voyage Picking Allocation]", "OWTQ / WTQ1", "old_b1.db", "AU Warehouse → EuropeSIT",
                     "AU Warehouse [IsCommited = +100]", "Reserves stock at AU MWAG ($545.00 AUD)", "Stock Allocation Queue"),
                    ("2.2.11", "2.2.11.13", "[Logistics] Post UK Maritime Transfer (OWTR) based on OWTQ @ AU Warehouse to EuropeSIT → [Long-Haul Transit Tracking]", "OWTR / WTR1", "old_b1.db", "AU Warehouse → EuropeSIT",
                     "EuropeSIT [OnHand = 100]", "Transferred at AU MWAG ($545.00 AUD)", "Dr 100050 (EuropeSIT) $54,500 / Cr 100010 ($54,500)"),
                    ("2.2.11", "2.2.11.14", "[Logistics] Post UK Inward GRPO (OPDN) @ EuropeMarketPlace → [UK Port Arrival Inbound Clearance]", "OPDN / PDN1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Base receipt cost = $545.00 AUD", "Dr 100040 (EuropeMarketPlace) $54,500 / Cr 100050 ($54,500)"),
                    ("2.2.11", "2.2.11.15", "[Finance] Capitalize UK Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final Stacked Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Final stacked cost = $560.00 AUD", "Dr 100040 (EuropeMarketPlace) $1,500 / Cr 200010 ($1,500)"),
                    ("2.2.11", "2.2.11.16", "[Sales] Book Wholesale Sales Order (ORDR) @ EuropeMarketPlace → [EuropeMarketPlace Channel Allocation]", "ORDR / RDR1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale agreement @ $750.00 AUD", "Sales Order Commitment"),
                    ("2.2.11", "2.2.11.17", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Channel Revenue Recognition]", "OINV / INV1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000, Revenue = $75,000", "Dr 110010 ($75,000) / Dr 500010 ($56,000) / Cr 400010 ($75,000) / Cr 100040 ($56,000)")
                ]
            }
        ]
    },
    
    # =========================================================
    # SECTION 2.3: new_b1.db ONLY (INTERNATIONAL MULTI-LEG & D2C)
    # =========================================================
    {
        "section_banner": "SECTION 2.3: new_b1.db ONLY (INTERNATIONAL MULTI-LEG, NZ, UK & D2C NETWORK) — 9 Routes",
        "processes": [
            {
                "l3_banner": "Process 2.3.1: Factory → NZ Warehouse → NZ Consumer (Direct NZ Import & Direct Invoicing)",
                "steps": [
                    ("2.3.1", "2.3.1.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ NZNTH → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "NZNTH",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD @ 0.65 rate", "Off-Balance Sheet Commitment"),
                    ("2.3.1", "2.3.1.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ NZNTH → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base inventory cost = $400.00 AUD", "Dr 100040 (NZNTH) $40,000 / Cr 200060 $40,000"),
                    ("2.3.1", "2.3.1.3", "[Finance] Accrue Destination Estimated Landed Cost (OIPF 'E') @ NZNTH → [Provisional Port Duty & Freight Allocation]", "OIPF (DocType 'E')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Inward provisional NZ duty & freight (+ $122.00 AUD/unit) → Provisional AvgPrice = $522.00 AUD", "Dr 100040 (NZNTH) $12,200 / Cr 200050 $12,200"),
                    ("2.3.1", "2.3.1.4", "[Finance] Overwrite Destination Actual Landed Cost (OIPF 'A') @ NZNTH → [Final Stock Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Overwrites provisional estimate from carrier invoices; locks AvgPrice = $522.00 AUD", "Dr 200050 ($12,200) / Cr 200010 ($12,200)"),
                    ("2.3.1", "2.3.1.5", "[Sales] Book Domestic NZ Customer Sales Order (ORDR) @ NZNTH → [Customer Stock Allocation]", "ORDR / RDR1", "new_b1.db", "NZNTH",
                     "NZNTH [Reserved = +100]", "Domestic sales order booking", "Sales Order Commitment"),
                    ("2.3.1", "2.3.1.6", "[Logistics] Post Direct AR Tax Invoice (OINV) @ NZNTH → [Domestic Customer Dispatch & Revenue Recognition]", "OINV / INV1", "new_b1.db", "NZNTH",
                     "Customer Custody\n[NZNTH OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $52,200, Revenue = $95,000", "Consolidated Entry (OJDT):\nDr 110010 (AR NZ) $95,000\nDr 500010 (COGS NZ) $52,200\nCr 400010 (Revenue) $95,000\nCr 100040 (NZNTH) $52,200")
                ]
            },
            {
                "l3_banner": "Process 2.3.2: Factory → ICC → NZ Warehouse → NZ Consumer (Consolidated NZ Multi-Leg Direct Invoicing)",
                "steps": [
                    ("2.3.2", "2.3.2.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)\n[At Vendor Site]", "DocCur='USD', PriceFC=$260.00, OnOrder=+100", "Off-Balance Sheet Commitment"),
                    ("2.3.2", "2.3.2.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand=100]", "Converted Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.3.2", "2.3.2.3", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand=100]", "Origin handling (+ $24) → OITW.AvgPrice = $424.00 AUD", "Dr 100040 ($2,400) / Cr 200010 ($2,400)"),
                    ("2.3.2", "2.3.2.4", "[Purchasing] Create Inventory Transfer Request (OWTQ) @ ICCChina → [Sea Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCChina [IsCommited = +100]", "Reserves origin stock at $424.00 AUD", "Stock Reservation Queue"),
                    ("2.3.2", "2.3.2.5", "[Logistics] Post Ocean In-Transit Transfer (OWTR) based on OWTQ @ ICCChina to ICCSIT → [Sea Voyage Tracking]", "OWTR / WTR1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCSIT [OnHand=100]", "Transferred at source MWAG ($424.00 AUD)", "Dr 100050 ($42,400) / Cr 100040 ($42,400)"),
                    ("2.3.2", "2.3.2.6", "[Logistics] Post Destination GRPO (OPDN) @ NZNTH → [Port Arrival Inbound Clearance]", "OPDN / PDN1", "new_b1.db", "ICCSIT → NZNTH",
                     "NZNTH [OnHand=100]", "Discharges ICCSIT and receives at NZNTH @ $424.00 AUD", "Dr 100040 NZNTH ($42,400) / Cr 100050 ($42,400)"),
                    ("2.3.2", "2.3.2.7", "[Finance] Overwrite Destination Stacked Landed Cost (OIPF 'A') @ NZNTH → [Regional Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand=100]", "NZ tariff & ocean freight (+ $98) → Final AvgPrice = $522.00 AUD", "Dr 100040 NZNTH ($9,800) / Cr 200010 ($9,800)"),
                    ("2.3.2", "2.3.2.8", "[Purchasing] Create Coastal Transfer Request (OWTQ) @ NZNTH → [South Island Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "NZNTH → NZSTH",
                     "NZNTH [IsCommited = +100]", "Reserves stock at NZ MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.3.2", "2.3.2.9", "[Logistics] Post Coastal Replenishment Transfer (OWTR) based on OWTQ @ NZNTH to NZSTH → [South Island DC Restocking]", "OWTR / WTR1", "new_b1.db", "NZNTH → NZSTH",
                     "NZSTH [OnHand=100]", "Transfers to Christchurch hub + coastal freight → AvgPrice = $545.00 AUD", "Dr 100040 NZSTH ($54,500) / Cr 100040 NZNTH ($52,200) + Clearing ($2,300)"),
                    ("2.3.2", "2.3.2.10", "[Sales] Book Domestic NZ Customer Sales Order (ORDR) @ NZSTH → [Customer Stock Allocation]", "ORDR / RDR1", "new_b1.db", "NZSTH",
                     "NZSTH [Reserved = +100]", "Customer sales order booking", "Sales Order Commitment"),
                    ("2.3.2", "2.3.2.11", "[Logistics] Post Direct AR Tax Invoice (OINV) @ NZSTH → [Customer Dispatch & Revenue Recognition]", "OINV / INV1", "new_b1.db", "NZSTH",
                     "Customer Custody\n[NZSTH OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $54,500 AUD, Revenue = $95,000", "Consolidated Entry (OJDT):\nDr 110010 (AR NZ) $95,000\nDr 500010 (COGS NZ) $54,500\nCr 400010 (Revenue) $95,000\nCr 100040 (NZSTH) $54,500")
                ]
            },
            {
                "l3_banner": "Process 2.3.3: Factory → EuropeMarketPlace (Direct Factory Shipment Direct Wholesale Invoicing)",
                "steps": [
                    ("2.3.3", "2.3.3.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ EuropeMarketPlace → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "EuropeMarketPlace",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD @ 0.65 rate", "Off-Balance Sheet Commitment"),
                    ("2.3.3", "2.3.3.2", "[Logistics] Post Direct Inbound GRPO (OPDN) @ EuropeMarketPlace → [Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Base inventory cost = $400.00 AUD", "Dr 100040 (EuropeMarketPlace) $40,000 / Cr 200060 $40,000"),
                    ("2.3.3", "2.3.3.3", "[Finance] Accrue UK Estimated Landed Cost (OIPF 'E') @ EuropeMarketPlace → [Provisional Felixstowe Port Duty Allocation]", "OIPF (DocType 'E')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Felixstowe duty & cartage (+ $160.00 AUD) → Provisional AvgPrice = $560.00 AUD", "Dr 100040 (EuropeMarketPlace) $16,000 / Cr 200050 $16,000"),
                    ("2.3.3", "2.3.3.4", "[Finance] Overwrite UK Actual Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Overwrites provisional estimate from carrier invoices; AvgPrice = $560.00 AUD", "Dr 200050 ($16,000) / Cr 200010 ($16,000)"),
                    ("2.3.3", "2.3.3.5", "[Sales] Book EuropeMarketPlace EDI Wholesale Order (ORDR) @ EuropeMarketPlace → [Channel Stock Allocation]", "ORDR / RDR1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale order booking @ $750.00 AUD", "Sales Order Commitment"),
                    ("2.3.3", "2.3.3.6", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Revenue Recognition]", "OINV / INV1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000 AUD, Revenue = $75,000", "Dr 110010 (AR) $75,000\nDr 500010 (COGS UK) $56,000\nCr 400010 (Revenue) $75,000\nCr 100040 (EuropeMarketPlace) $56,000")
                ]
            },
            {
                "l3_banner": "Process 2.3.4: Factory → ICC → EuropeMarketPlace (Consolidated Movement Direct Wholesale Invoicing)",
                "steps": [
                    ("2.3.4", "2.3.4.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.3.4", "2.3.4.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.3.4", "2.3.4.3", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Origin capitalized cost = $424.00 AUD", "Dr 100040 ($2,400) / Cr 200010 ($2,400)"),
                    ("2.3.4", "2.3.4.4", "[Purchasing] Create Export Transfer Request (OWTQ) @ ICCChina → [UK Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → EuropeSIT",
                     "ICCChina [IsCommited = +100]", "Reserves origin stock at $424.00 AUD", "Stock Reservation Queue"),
                    ("2.3.4", "2.3.4.5", "[Logistics] Post Ocean Transit Transfer (OWTR) based on OWTQ @ ICCChina to EuropeSIT → [Maritime Voyage Tracking]", "OWTR / WTR1", "new_b1.db", "ICCChina → EuropeSIT",
                     "EuropeSIT [OnHand = 100]", "Transferred at source MWAG ($424.00 AUD)", "Dr 100050 (EuropeSIT) $42,400 / Cr 100040 ($42,400)"),
                    ("2.3.4", "2.3.4.6", "[Logistics] Post Inbound GRPO (OPDN) @ EuropeMarketPlace → [UK Port Arrival Clearance]", "OPDN / PDN1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Base receipt cost = $424.00 AUD", "Dr 100040 (EuropeMarketPlace) $42,400 / Cr 100050 ($42,400)"),
                    ("2.3.4", "2.3.4.7", "[Finance] Overwrite UK Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final Stacked Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "UK ocean freight & customs (+ $136 AUD) → Final AvgPrice = $560.00 AUD", "Dr 100040 (EuropeMarketPlace) $13,600 / Cr 200010 ($13,600)"),
                    ("2.3.4", "2.3.4.8", "[Sales] Book EuropeMarketPlace Wholesale Order (ORDR) @ EuropeMarketPlace → [Finished Goods Allocation]", "ORDR / RDR1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale agreement @ $750.00 AUD", "Sales Order Commitment"),
                    ("2.3.4", "2.3.4.9", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Revenue Recognition]", "OINV / INV1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000 AUD, Revenue = $75,000", "Dr 110010 (AR) $75,000\nDr 500010 (COGS UK) $56,000\nCr 400010 (Revenue) $75,000\nCr 100040 (EuropeMarketPlace) $56,000")
                ]
            },
            {
                "l3_banner": "Process 2.3.5: Factory → NZ Warehouse → EuropeMarketPlace (NZ Hub Re-Export Direct Wholesale Invoicing)",
                "steps": [
                    ("2.3.5", "2.3.5.1", "[Purchasing] Issue Direct Factory PO in USD (OPOR) @ NZNTH → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "NZNTH",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.3.5", "2.3.5.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ NZNTH → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.3.5", "2.3.5.3", "[Finance] Overwrite NZ Landed Cost (OIPF 'A') @ NZNTH → [Direct NZ DC Capitalization]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Direct NZ landed cost = $522.00 AUD", "Dr 100040 ($12,200) / Cr 200010 ($12,200)"),
                    ("2.3.5", "2.3.5.4", "[Purchasing] Create UK Export Transfer Request (OWTQ) @ NZNTH → [UK Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "NZNTH → EuropeSIT",
                     "NZNTH [IsCommited = +100]", "Reserves stock at NZ MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.3.5", "2.3.5.5", "[Logistics] Post Maritime Transfer (OWTR) based on OWTQ @ NZNTH to EuropeSIT → [Re-Export Transit Tracking]", "OWTR / WTR1", "new_b1.db", "NZNTH → EuropeSIT",
                     "EuropeSIT [OnHand = 100]", "Transferred at NZ MWAG ($522.00 AUD)", "Dr 100050 (EuropeSIT) $52,200 / Cr 100040 ($52,200)"),
                    ("2.3.5", "2.3.5.6", "[Logistics] Post Inward GRPO (OPDN) @ EuropeMarketPlace → [UK Port Arrival Inbound Clearance]", "OPDN / PDN1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Dr 100040 (EuropeMarketPlace) $52,200 / Cr 100050 ($52,200)"),
                    ("2.3.5", "2.3.5.7", "[Finance] Capitalize UK Inbound Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final Stacked Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "UK handling & customs (+ $38 AUD) → Final AvgPrice = $560.00 AUD", "Dr 100040 (EuropeMarketPlace) $3,800 / Cr 200010 ($3,800)"),
                    ("2.3.5", "2.3.5.8", "[Sales] Book Wholesale Sales Order (ORDR) @ EuropeMarketPlace → [EuropeMarketPlace Channel Allocation]", "ORDR / RDR1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale agreement @ $750.00 AUD", "Sales Order Commitment"),
                    ("2.3.5", "2.3.5.9", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Channel Revenue Recognition]", "OINV / INV1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000, Revenue = $75,000", "Dr 110010 ($75,000) / Dr 500010 ($56,000) / Cr 400010 ($75,000) / Cr 100040 ($56,000)")
                ]
            },
            {
                "l3_banner": "Process 2.3.6: Factory → ICC → NZ Warehouse → EuropeMarketPlace (Consolidated Transshipment Direct Wholesale Invoicing)",
                "steps": [
                    ("2.3.6", "2.3.6.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.3.6", "2.3.6.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Origin Spot FX Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.3.6", "2.3.6.3", "[Finance] Capitalize Origin Actual Landed Cost (OIPF 'A') @ ICCChina → [Source MWAG Lock]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Capitalized origin cost = $424.00 AUD", "Dr 100040 ($2,400) / Cr 200010 ($2,400)"),
                    ("2.3.6", "2.3.6.4", "[Purchasing] Create Export Transfer Request (OWTQ) @ ICCChina → [NZ Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCChina [IsCommited = +100]", "Reserves origin stock at $424.00 AUD", "Stock Reservation Queue"),
                    ("2.3.6", "2.3.6.5", "[Logistics] Post Ocean Transit Transfer (OWTR) based on OWTQ @ ICCChina to ICCSIT → [Sea Voyage Tracking]", "OWTR / WTR1", "new_b1.db", "ICCChina → ICCSIT",
                     "ICCSIT [OnHand = 100]", "Sea transit @ $424.00 AUD", "Dr 100050 ($42,400) / Cr 100040 ($42,400)"),
                    ("2.3.6", "2.3.6.6", "[Logistics] Post NZ Port Inward GRPO (OPDN) @ NZNTH → [NZ Port Arrival Clearance]", "OPDN / PDN1", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "Base receipt cost = $424.00 AUD", "Dr 100040 ($42,400) / Cr 100050 ($42,400)"),
                    ("2.3.6", "2.3.6.7", "[Finance] Overwrite NZ Destination Landed Cost (OIPF 'A') @ NZNTH → [NZ Regional Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "NZNTH",
                     "NZNTH [OnHand = 100]", "NZ DC moving average = $522.00 AUD", "Dr 100040 ($9,800) / Cr 200010 ($9,800)"),
                    ("2.3.6", "2.3.6.8", "[Purchasing] Create UK Re-Export Transfer Request (OWTQ) @ NZNTH → [UK Voyage Picking Allocation]", "OWTQ / WTQ1", "new_b1.db", "NZNTH → EuropeSIT",
                     "NZNTH [IsCommited = +100]", "Reserves stock at NZ MWAG ($522.00 AUD)", "Stock Allocation Queue"),
                    ("2.3.6", "2.3.6.9", "[Logistics] Post UK Maritime Transfer (OWTR) based on OWTQ @ NZNTH to EuropeSIT → [Long-Haul Transit Tracking]", "OWTR / WTR1", "new_b1.db", "NZNTH → EuropeSIT",
                     "EuropeSIT [OnHand = 100]", "Transferred at NZ MWAG ($522.00 AUD)", "Dr 100050 (EuropeSIT) $52,200 / Cr 100040 ($52,200)"),
                    ("2.3.6", "2.3.6.10", "[Logistics] Post UK Inward GRPO (OPDN) @ EuropeMarketPlace → [UK Port Arrival Clearance]", "OPDN / PDN1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Base receipt cost = $522.00 AUD", "Dr 100040 (EuropeMarketPlace) $52,200 / Cr 100050 ($52,200)"),
                    ("2.3.6", "2.3.6.11", "[Finance] Capitalize UK Landed Cost (OIPF 'A') @ EuropeMarketPlace → [Final Stacked Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [OnHand = 100]", "Final stacked cost = $560.00 AUD", "Dr 100040 (EuropeMarketPlace) $3,800 / Cr 200010 ($3,800)"),
                    ("2.3.6", "2.3.6.12", "[Sales] Book Wholesale Sales Order (ORDR) @ EuropeMarketPlace → [EuropeMarketPlace Channel Allocation]", "ORDR / RDR1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace [Reserved = +100]", "Wholesale agreement @ $750.00 AUD", "Sales Order Commitment"),
                    ("2.3.6", "2.3.6.13", "[Logistics] Post Direct Wholesale AR Invoice (OINV) @ EuropeMarketPlace → [EuropeMarketPlace Channel Revenue Recognition]", "OINV / INV1", "new_b1.db", "EuropeMarketPlace",
                     "EuropeMarketPlace Custody\n[OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $56,000, Revenue = $75,000", "Dr 110010 ($75,000) / Dr 500010 ($56,000) / Cr 400010 ($75,000) / Cr 100040 ($56,000)")
                ]
            },
            {
                "l3_banner": "Process 2.3.7: Factory → ICC → AU Consumer (D2C Air Express Direct Invoicing)",
                "steps": [
                    ("2.3.7", "2.3.7.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.3.7", "2.3.7.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 (ICCChina) $40,000 / Cr 200060 $40,000"),
                    ("2.3.7", "2.3.7.3", "[Finance] Capitalize Air Freight Landed Cost (OIPF 'A') @ ICCChina → [Drop-Ship Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Direct air courier (+ $180 AUD/unit) → AvgPrice = $580.00 AUD", "Dr 100040 (ICCChina) $18,000 / Cr 200010 $18,000"),
                    ("2.3.7", "2.3.7.4", "[Sales] Book D2C Consumer Sales Order (ORDR) @ ICCChina → [AU Consumer Stock Allocation]", "ORDR / RDR1", "new_b1.db", "ICCChina",
                     "ICCChina [Reserved = +100]", "Consumer sales order: Unit Price = $950.00 AUD", "Sales Order Commitment"),
                    ("2.3.7", "2.3.7.5", "[Logistics] Post Direct AR Tax Invoice (OINV) @ ICCChina → [Direct Air Dispatch & Revenue Recognition]", "OINV / INV1", "new_b1.db", "ICCChina",
                     "Customer Custody\n[ICCChina OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $58,000 AUD, Revenue = $95,000", "Dr 110010 ($95,000)\nDr 500010 (COGS D2C) $58,000\nCr 400010 (Revenue) $95,000\nCr 100040 (ICCChina) $58,000")
                ]
            },
            {
                "l3_banner": "Process 2.3.8: Factory → ICC → NZ Consumer (D2C Air Express Direct Invoicing)",
                "steps": [
                    ("2.3.8", "2.3.8.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.3.8", "2.3.8.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 (ICCChina) $40,000 / Cr 200060 $40,000"),
                    ("2.3.8", "2.3.8.3", "[Finance] Capitalize Air Freight Landed Cost (OIPF 'A') @ ICCChina → [Drop-Ship Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Direct air courier (+ $180 AUD/unit) → AvgPrice = $580.00 AUD", "Dr 100040 (ICCChina) $18,000 / Cr 200010 $18,000"),
                    ("2.3.8", "2.3.8.4", "[Sales] Book D2C Consumer Sales Order (ORDR) @ ICCChina → [NZ Consumer Stock Allocation]", "ORDR / RDR1", "new_b1.db", "ICCChina",
                     "ICCChina [Reserved = +100]", "Consumer sales order: Unit Price = $950.00 AUD", "Sales Order Commitment"),
                    ("2.3.8", "2.3.8.5", "[Logistics] Post Direct AR Tax Invoice (OINV) @ ICCChina → [Direct Air Dispatch & Revenue Recognition]", "OINV / INV1", "new_b1.db", "ICCChina",
                     "Customer Custody\n[ICCChina OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $58,000 AUD, Revenue = $95,000", "Dr 110010 ($95,000)\nDr 500010 (COGS D2C) $58,000\nCr 400010 (Revenue) $95,000\nCr 100040 (ICCChina) $58,000")
                ]
            },
            {
                "l3_banner": "Process 2.3.9: Factory → ICC → UK Consumer (D2C Air Express Direct Invoicing)",
                "steps": [
                    ("2.3.9", "2.3.9.1", "[Purchasing] Issue Factory PO in USD (OPOR) @ ICCChina → [Vendor Production Commitment]", "OPOR / POR1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "DocCur='USD', PriceFC=$260.00 USD", "Off-Balance Sheet Commitment"),
                    ("2.3.9", "2.3.9.2", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Base Cost = $400.00 AUD @ 0.65 rate", "Dr 100040 (ICCChina) $40,000 / Cr 200060 $40,000"),
                    ("2.3.9", "2.3.9.3", "[Finance] Capitalize Air Freight Landed Cost (OIPF 'A') @ ICCChina → [Drop-Ship Valuation & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand = 100]", "Direct air courier (+ $195 AUD/unit) → AvgPrice = $595.00 AUD", "Dr 100040 (ICCChina) $19,500 / Cr 200010 $19,500"),
                    ("2.3.9", "2.3.9.4", "[Sales] Book D2C Consumer Sales Order (ORDR) @ ICCChina → [UK Consumer Stock Allocation]", "ORDR / RDR1", "new_b1.db", "ICCChina",
                     "ICCChina [Reserved = +100]", "Consumer sales order: Unit Price = $980.00 AUD", "Sales Order Commitment"),
                    ("2.3.9", "2.3.9.5", "[Logistics] Post Direct AR Tax Invoice (OINV) @ ICCChina → [Direct Air Dispatch & Revenue Recognition]", "OINV / INV1", "new_b1.db", "ICCChina",
                     "Customer Custody\n[ICCChina OnHand = 0]", "Direct from ORDR (bypasses standalone ODLN); COGS = $59,500 AUD, Revenue = $98,000", "Dr 110010 ($98,000)\nDr 500010 (COGS D2C) $59,500\nCr 400010 (Revenue) $98,000\nCr 100040 (ICCChina) $59,500")
                ]
            }
        ]
    },
    
    # =========================================================
    # SECTION 2.4: EXCEPTION PROCESSES (PO REROUTES & VARIANCES)
    # =========================================================
    {
        "section_banner": "SECTION 2.4: EXCEPTION PROCESSES (PO REROUTES & CONTAINER DISCREPANCIES) — 3 Routes",
        "processes": [
            {
                "l3_banner": "Process 2.4.1: PO Changes from ICC to AU Warehouse (Pre-Shipment Destination Change)",
                "steps": [
                    ("2.4.1", "2.4.1.1", "[Purchasing] Cancel Origin Factory PO Line (OPOR) @ ICCChina → [Commitment Release]", "OPOR in new_b1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "Closes open factory PO line (DocStatus='C') in new_b1.db; clears POR1.OnOrder", "Off-Balance Sheet Commitment Release"),
                    ("2.4.1", "2.4.1.2", "[Purchasing] Re-Issue Direct Factory PO in USD (OPOR) @ AU Warehouse → [AU Commitment Establishment]", "OPOR in old_b1", "old_b1.db", "AU Warehouse",
                     "None (OnHand = 0)", "Re-issues PO in USD targeting AU Warehouses in old_b1.db", "Off-Balance Sheet Commitment Established"),
                    ("2.4.1", "2.4.1.3", "[Logistics] Post Inward GRPO (OPDN) @ AU Warehouse → [Direct AU Base Capitalization]", "OPDN in old_b1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand=100]", "Posts direct receipt in AUD at spot rate ($400.00 AUD)", "Dr 100010 ($40,000) / Cr 200010 ($40,000)"),
                    ("2.4.1", "2.4.1.4", "[Finance] Capitalize Destination Landed Cost (OIPF 'A') @ AU Warehouse → [Final AU Stock Valuation & G/L 200050 Reconciled]", "OIPF in old_b1", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand=100]", "Allocates ocean freight & customs into AU moving average ($522.00)", "Dr 100010 ($12,200) / Cr 200010 ($12,200)")
                ]
            },
            {
                "l3_banner": "Process 2.4.2: PO Changes from AU Warehouse to ICC (Consolidation Routing Change)",
                "steps": [
                    ("2.4.2", "2.4.2.1", "[Purchasing] Cancel Direct AU PO Line (OPOR) @ AU Warehouse → [Direct Commitment Release]", "OPOR in old_b1", "old_b1.db", "AU Warehouse",
                     "None (OnHand = 0)", "Cancels direct AU PO lines in old_b1.db", "Off-Balance Sheet Commitment Release"),
                    ("2.4.2", "2.4.2.2", "[Purchasing] Issue Replacement Factory PO in USD (OPOR) @ ICCChina → [Origin Consolidation Commitment]", "OPOR in new_b1", "new_b1.db", "ICCChina",
                     "None (OnHand = 0)", "Issues replacement PO in USD committed to ICCChina hub", "Off-Balance Sheet Commitment Established"),
                    ("2.4.2", "2.4.2.3", "[Logistics] Post Inward Factory GRPO (OPDN) @ ICCChina → [Base Cost Capitalization]", "OPDN / PDN1", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand=100]", "Base receipt cost in AUD at spot rate ($400.00 AUD)", "Dr 100040 ($40,000) / Cr 200060 ($40,000)"),
                    ("2.4.2", "2.4.2.4", "[Finance] Capitalize Origin Landed Cost (OIPF 'A') @ ICCChina → [Origin Hub Capitalization & G/L 200050 Reconciled]", "OIPF (DocType 'A')", "new_b1.db", "ICCChina",
                     "ICCChina [OnHand=100]", "Capitalizes origin cost ($424.00 AUD) and enters multi-leg flow", "Dr 100040 ($2,400) / Cr 200010 ($2,400)")
                ]
            },
            {
                "l3_banner": "Process 2.4.3: Intercompany Transfer Quantity Over/Under-Supply Discrepancy Resolution",
                "steps": [
                    ("2.4.3", "2.4.3.1", "[Logistics] Log Physical Container Discrepancy (OPDN Audit) @ AU Warehouse → [Variance Identification]", "OPDN Audit", "old_b1.db", "AU Warehouse",
                     "Physical Variance Logged", "Discrepancy identified upon container destuffing (e.g. 95 vs 100 units)", "Variance Audit Milestone"),
                    ("2.4.3", "2.4.3.2", "[Logistics] Post Partial Inbound GRPO (OPDN) @ AU Warehouse → [Actual Delivered Stock Receipt]", "OPDN (old_b1)", "old_b1.db", "AU Warehouse",
                     "AU Warehouse [OnHand=95]", "Receives 95 verified units at AU DC ($40,280 AUD)", "Dr 100010 ($40,280) / Cr 200030 ($40,280)"),
                    ("2.4.3", "2.4.3.3", "[Finance] Post Transit Loss Goods Issue Write-Off (OIGE) @ ICCSIT → [In-Transit Loss Clearance]", "OIGE (new_b1)", "new_b1.db", "ICCSIT",
                     "ICCSIT [OnHand=0]", "Writes off 5 missing transit units from ICCSIT asset ledger", "Dr 500090 (Transit Loss Variance) $2,120 / Cr 100050 $2,120"),
                    ("2.4.3", "2.4.3.4", "[Logistics] Post Surplus Inward GRPO & Supplementary Invoice (OPDN/OINV) @ AU Warehouse & ICCChina → [Surplus Settlement]", "OPDN (old_b1) + OINV (new_b1)", "old_b1 & new_b1", "AU Warehouse & ICCChina",
                     "AU Warehouse [OnHand=105]", "Receives 105 units upon commercial approval; supplementary intercompany invoice issued", "Dest: Dr 100010 ($44,520) / Cr 200030 ($44,520)\nOrigin: Dr 110020 ($44,520) / Cr 100050 ($44,520)")
                ]
            }
        ]
    },
    
    # =========================================================
    # SECTION 2.5: RECONCILIATION PROCESSES (FINANCIAL CLOSING)
    # =========================================================
    {
        "section_banner": "SECTION 2.5: RECONCILIATION PROCESSES (FINANCIAL & LANDED COST AUDIT) — 2 Workflows",
        "processes": [
            {
                "l3_banner": "Process 2.5.1: Enterprise Inventory Valuation Reconciliation (Subledger vs G/L)",
                "steps": [
                    ("2.5.1", "2.5.1.1", "[Finance] Extract Warehouse Subledger Balances (OITW/OINM) @ All Hubs → [Subledger Audit Benchmark]", "OITW / OINM", "Both DBs", "All Hubs",
                     "Audit Extraction", "Extract Total Valuation = Sum(OITW.OnHand x OITW.AvgPrice) per warehouse", "Subledger Audit Benchmark"),
                    ("2.5.1", "2.5.1.2", "[Finance] Compare G/L Control Account Balances (OJDT/JDT1) @ Finance Control → [Discrepancy Identification]", "OJDT / JDT1", "Both DBs", "Finance Control",
                     "G/L Audit", "Compare subledger valuation against G/L 100010 (Inventory) and 100050 (In-Transit)", "Identifies manual journal anomalies"),
                    ("2.5.1", "2.5.1.3", "[Logistics] Validate In-Transit Sea Shipments (OWTR/OITW) @ SIT Hubs → [Open Maritime Asset Clearance]", "OWTR / OITW", "Both DBs", "SIT Hubs",
                     "SIT Reconciliation", "Verify all open ICCSIT/NZSIT/EuropeSIT quantities match un-discharged B/L shipments", "Validates open maritime assets"),
                    ("2.5.1", "2.5.1.4", "[Finance] Post Inventory Revaluation Adjustments (MRV/OINM) @ All Hubs → [Balance Sheet Compliance]", "MRV / OINM (TransType 69)", "Both DBs", "All Hubs",
                     "Revaluation Adjust", "Posts adjustment if statutory moving average revaluation is required", "Dr/Cr 100010 (Inventory) / Cr/Dr 500070 (Inventory Reval Variance)")
                ]
            },
            {
                "l3_banner": "Process 2.5.2: Landed Cost Entries Reconciliation (Accrual vs Actual Clearing)",
                "steps": [
                    ("2.5.2", "2.5.2.1", "[Finance] Audit Open Landed Cost Accruals (OIPF 'E') @ All Hubs → [Freight Clearing Identification]", "OIPF (DocType 'E')", "Both DBs", "All Hubs",
                     "Accrual Audit", "Extract all open provisional allocations posted to G/L 200050", "Audit of open freight/duty accruals"),
                    ("2.5.2", "2.5.2.2", "[Finance] Match Actual Carrier & Broker Invoices (OPCH/IPF2) @ Finance Control → [Three-Way Matching Verification]", "OPCH / IPF2", "Both DBs", "Finance Control",
                     "Invoice Matching", "Match actual carrier invoices (ocean freight, customs, wharfage) against estimates", "Three-way invoice verification"),
                    ("2.5.2", "2.5.2.3", "[Finance] Verify Zero-Balance Clearing Closure (OJDT) @ Finance Control → [Variance Transfer & Final Settlement]", "OJDT Reconciliation", "Both DBs", "Finance Control",
                     "Zero Balance Verified", "Verify G/L 200050 nets to exactly $0.00; transfer FX variances to G/L 500080", "Dr 200050 Clearing / Cr 200010 AP (Net $0.00 variance)")
                ]
            }
        ]
    }
]
