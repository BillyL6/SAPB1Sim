import sys
import os

sys.path.insert(0, "/Users/billy/SAPB1_Sim")
import process_data

# Read process_data.py content
proc_path = "/Users/billy/SAPB1_Sim/process_data.py"
with open(proc_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update INDEX_DATA to include 2.5.3, 2.6.1, 2.6.2
old_index_recon = """    ("2.5 [SNG-RECON]", "2.5.1", "Inventory Valuation Reconciliation", "new_b1 + old_b1", "All Hubs", "In-Transit", "Balance Sheet", "Monthly audit: Warehouse subledger (OITW) vs G/L Control (100010/100050)", "OITW, OINM, OJDT, JDT1, Trial Balance"),
    ("2.5 [SNG-RECON]", "2.5.2", "Landed Cost Entries Reconciliation", "new_b1 + old_b1", "All Hubs", "Accrual Clearing", "G/L 200050", "Reconciles Estimated (OIPF 'E') vs Actual (OIPF 'A') broker invoices to $0", "OIPF, IPF1, IPF2, OPCH, OJDT (200050)")
]"""

new_index_recon = """    ("2.5 [SNG-RECONCILIATION]", "2.5.1", "Inventory Valuation Reconciliation", "new_b1 + old_b1", "All Hubs", "In-Transit", "Balance Sheet", "Monthly audit: Warehouse subledger (OITW) vs G/L Control (100010/100050)", "OITW, OINM, OJDT, JDT1, Trial Balance"),
    ("2.5 [SNG-RECONCILIATION]", "2.5.2", "Landed Cost Entries Reconciliation", "new_b1 + old_b1", "All Hubs", "Accrual Clearing", "G/L 200050", "Reconciles Estimated (OIPF 'E') vs Actual (OIPF 'A') broker invoices to $0", "OIPF, IPF1, IPF2, OPCH, OJDT (200050)"),
    ("2.5 [SNG-RECONCILIATION]", "2.5.3", "Group Report Reconciliation", "new_b1 + old_b1", "All Hubs", "Consolidated Ledgers", "Group Financial Statements", "Intercompany elimination, group inventory valuation consolidation, and multi-entity profit reporting", "OJDT, JDT1, OACT, Group Balance Sheet"),
    
    ("2.6 [MD-MAINTENANCE]", "2.6.1", "SAP B1 Inventory Item Master Maintenance", "new_b1 + old_b1", "Master Setup", "Warehouse Bins", "Item Master Records", "Item Code creation, valuation method setup (OITM vs OITW), purchasing/sales UoM, and barcode cataloging", "OITM, OITW, ITM1, OPLN, OWHS, OBIN"),
    ("2.6 [MD-MAINTENANCE]", "2.6.2", "SAP B1 Business Partner Master Maintenance", "new_b1 + old_b1", "Master Setup", "Commercial Ledger", "BP Master Records", "Vendor/Customer setup (OCRD/CRD1), currency assignment (USD/AUD/NZD/GBP), payment terms (OCTG), and tax group mapping", "OCRD, CRD1, OCPR, OCRG, OCTG, OSTC")
]"""

content = content.replace(old_index_recon, new_index_recon)

# 2. Add Section 2.5.3 and Section 2.6 to ALL_SECTIONS
old_sec5_tail = """                    ("2.5.2", "2.5.2.3", "[Finance] Verifies Zero-Balance Clearing Closure (OJDT) @ Finance Control → [Variance Transfer & Final Settlement]", "OJDT Reconciliation", "Both DBs", "Finance Control",
                      "Zero Balance Verified", "Verify G/L 200050 nets to exactly $0.00; transfer FX variances to G/L 500080", "Dr 200050 Clearing / Cr 200010 AP (Net $0.00 variance)")
                ]
            }
        ]
    }
]"""

new_sec5_tail = """                    ("2.5.2", "2.5.2.3", "[Finance] Verifies Zero-Balance Clearing Closure (OJDT) @ Finance Control → [Variance Transfer & Final Settlement]", "OJDT Reconciliation", "Both DBs", "Finance Control",
                      "Zero Balance Verified", "Verify G/L 200050 nets to exactly $0.00; transfer FX variances to G/L 500080", "Dr 200050 Clearing / Cr 200010 AP (Net $0.00 variance)")
                ]
            },
            {
                "l3_banner": "Process 2.5.3: Group Report Reconciliation (Multi-Entity Financial Consolidation & Intercompany Elimination)",
                "steps": [
                    ("2.5.3", "2.5.3.1", "[Finance] Extract Multi-Entity Trial Balance & Ledger Postings (OJDT) @ All Hubs → [Consolidated Entity Extract]", "OJDT / JDT1", "Both DBs", "Finance Control",
                      "All Warehouses & Entities", "Extract trial balances and general ledger journal transactions across new_b1.db and old_b1.db", "Audit extract of operating ledgers (OJDT/JDT1)"),
                    ("2.5.3", "2.5.3.2", "[Finance] Reconcile Intercompany Trade Balances (G/L 110020 vs 200030) @ new_b1 & old_b1 → [Intercompany Clearing Elimination]", "OJDT Elimination", "Both DBs", "Finance Control",
                      "Intercompany Elimination", "Match Intercompany AR (110020) against Intercompany AP (200030); eliminate intercompany markup", "Dr 200030 (IC AP) / Cr 110020 (IC AR) (Elimination Entry)"),
                    ("2.5.3", "2.5.3.3", "[Finance] Generate Group Inventory Valuation & Consolidated P&L Report @ Finance Control → [Statutory Group Consolidation]", "Group Financial Report", "Both DBs", "Executive Control",
                      "Consolidated Group Balance Sheet", "Compile consolidated group inventory asset valuation and net gross profit report", "Group Financial Statements Sign-Off (Balance Sheet & P&L)")
                ]
            }
        ]
    },
    
    # =========================================================
    # SECTION 2.6: MASTER DATA MAINTENANCE (ITEM & BP SETUP)
    # =========================================================
    {
        "section_banner": "SECTION 2.6: MASTER DATA MAINTENANCE (ITEM & BUSINESS PARTNER GOVERNANCE) — 2 Processes",
        "processes": [
            {
                "l3_banner": "Process 2.6.1: SAP B1 Inventory Item Master Maintenance (SKU Definition, Costing Method & Bin Setup)",
                "steps": [
                    ("2.6.1", "2.6.1.1", "[Logistics] Create Inventory Item Master Header (OITM) @ new_b1 & old_b1 → [Master SKU Definition]", "OITM", "Both DBs", "Master Catalog",
                      "Catalog Definition", "Establish unique ItemCode, ItemName, ItemGroup, purchasing/sales units of measure, and default warehouse", "Master Data Setup (No financial journal entries in OJDT)"),
                    ("2.6.1", "2.6.1.2", "[Finance] Configure Item Valuation Method & Price Lists (OITW / ITM1) @ new_b1 & old_b1 → [Costing & Pricing Configuration]", "OITW / ITM1", "Both DBs", "Finance Control",
                      "Valuation Setup", "Configure Moving Average Costing method (OITW.AvgPrice in new_b1 vs OITM.AvgPrice in old_b1) and base price lists", "Inventory Costing Parameter Lock"),
                    ("2.6.1", "2.6.1.3", "[Purchasing] Assign Default Vendor & Purchasing UoM Parameters (OITM / POR1) @ new_b1 & old_b1 → [Procurement Parameter Activation]", "OITM / POR1", "Both DBs", "Purchasing Control",
                      "Vendor Linkage", "Link primary foreign factory vendor (V-FACTORY-CN), purchasing lead times, and customs tariff codes", "Procurement Master Data Lock"),
                    ("2.6.1", "2.6.1.4", "[Logistics] Establish Warehouse Stock Minimums & Bin Allocations (OITW / OBIN) @ All Warehouses → [Warehouse Replenishment Readiness]", "OITW / OBIN", "Both DBs", "All Warehouses",
                      "Stock Thresholds", "Set minimum/maximum reorder stock levels (MinStock/MaxStock) and default physical bin locations", "Operational Logistics Activation")
                ]
            },
            {
                "l3_banner": "Process 2.6.2: SAP B1 Business Partner Master Maintenance (Customer, Vendor & Carrier Onboarding)",
                "steps": [
                    ("2.6.2", "2.6.2.1", "[Sales] Create Customer Business Partner Master Record (OCRD) @ new_b1 & old_b1 → [Customer Account Onboarding]", "OCRD", "Both DBs", "Sales Control",
                      "Customer Onboarding", "Create customer CardCode, registered trading name, contact persons (OCPR), and market territory group (OCRG)", "Customer Master Setup (No financial journal entries in OJDT)"),
                    ("2.6.2", "2.6.2.2", "[Purchasing] Create Supplier & Carrier Business Partner Master Record (OCRD) @ new_b1 & old_b1 → [Vendor & Forwarder Onboarding]", "OCRD", "Both DBs", "Purchasing Control",
                      "Vendor Onboarding", "Create supplier/carrier CardCode, foreign currency assignment (USD FOB / AUD), and logistics contact records", "Vendor Master Setup (No financial journal entries in OJDT)"),
                    ("2.6.2", "2.6.2.3", "[Logistics] Configure Business Partner Ship-To & Bill-To Addresses (CRD1) @ All Entities → [Logistics Routing Setup]", "CRD1", "Both DBs", "Logistics Control",
                      "Address Master", "Configure multiple destination warehouse delivery addresses, port shipping addresses, and export billing locations", "Logistics Address Directory Lock"),
                    ("2.6.2", "2.6.2.4", "[Finance] Assign Currency, Payment Terms & Tax Codes (OCTG / OSTC) @ Finance Control → [Commercial Terms & Credit Lock]", "OCTG / OSTC / OCRD", "Both DBs", "Finance Control",
                      "Commercial Terms", "Assign credit limits, payment terms (Net 30/60/COD), tax codes (GST 10%/Zero-Rated Export), and G/L control accounts", "Financial Master Data Sign-Off")
                ]
            }
        ]
    }
]"""

content = content.replace(old_sec5_tail, new_sec5_tail)

with open(proc_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated process_data.py with Group 2.6 and Process 2.5.3 (31 total processes)!")
