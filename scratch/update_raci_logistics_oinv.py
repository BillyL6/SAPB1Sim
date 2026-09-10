import re

proc_file = "/Users/billy/SAPB1_Sim/process_data.py"

with open(proc_file, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Policy 9 and Principle text in process_data.py
code = code.replace(
    "• [Purchasing] = OPOR (All Purchase Orders) & OWTQ (All Transfer Requests)\n• [Logistics] = All Material Movements (OIGE Goods Issue, OPDN Goods Receipt, OWTR Transfers)\n• [Finance] = All Cost Accounting, OIPF Landed Costs, Direct OINV Invoicing & G/L Reconciliations.",
    "• [Purchasing] = OPOR (All Purchase Orders) & OWTQ (All Transfer Requests)\n• [Logistics] = All Material Movements (OIGE Goods Issue, OPDN Goods Receipt, OWTR Transfers) & Direct OINV Creation (Order Dispatch Confirmation)\n• [Finance] = All Cost Accounting, OIPF Landed Costs, Revenue/COGS Accounting & G/L Reconciliations."
)

code = code.replace(
    "• [Logistics] is strictly Responsible & Accountable (R/A) for all material movements, physical picking, Goods Issue (OIGE), Goods Receipt POs (OPDN), and Inventory Transfers (OWTR).\n• [Finance] is strictly Responsible & Accountable (R/A) for all Cost Accounting, Landed Cost accruals and actual overwrites (OIPF 'E'/'A'), Direct AR Invoices (OINV), and G/L clearing reconciliations (200050/100050/110020).",
    "• [Logistics] is strictly Responsible & Accountable (R/A) for all material movements, physical picking, Goods Issue (OIGE), Goods Receipt POs (OPDN), Inventory Transfers (OWTR), and creating Direct AR Invoices (OINV) to confirm order dispatch.\n• [Finance] is strictly Responsible & Accountable (R/A) for all Cost Accounting, Landed Cost accruals and actual overwrites (OIPF 'E'/'A'), Revenue/COGS accounting verification, and G/L clearing reconciliations (200050/100050/110020)."
)

code = code.replace(
    "  - [Logistics]: OWTR (WTR1), OIGE (IGE1), OPDN (PDN1)\n  - [Finance]: OIPF (IPF1/IPF2), OINV (INV1), OJDT (JDT1)",
    "  - [Logistics]: OWTR (WTR1), OIGE (IGE1), OPDN (PDN1), OINV (INV1)\n  - [Finance]: OIPF (IPF1/IPF2), OJDT (JDT1), Financial Audits"
)

# 2. Update RACI_DATA entry for Direct AR Invoicing
old_raci_row = """    ("Direct AR Invoicing & Revenue/COGS Accounting", "OINV", "AUD", "Finance", "Accountable (A) / Responsible (R)", "Sales (I), Logistics (C)",
     "• [Finance] Posts Direct AR Tax Invoice (OINV) created directly against Sales Order (ORDR).\\n• Concurrently relieves inventory (100010), recognizes COGS (500010), posts Revenue (400010), tax (200020), and establishes AR (110010) in single unified journal entry."),"""

new_raci_row = """    ("Direct AR Invoicing & Order Dispatch Confirmation", "OINV", "AUD", "Logistics", "Accountable (A) / Responsible (R)", "Finance (A/I - Accounting & Receivables), Sales (I)",
     "• [Logistics] Creates & posts Direct AR Tax Invoice (OINV) directly against Sales Order (ORDR) as part of the physical logistics process confirming order dispatch.\\n• Concurrently executes physical stock deduction (OnHand relief), triggers automatic COGS (500010) and Revenue (400010) recognition, and establishes AR (110010) in unified journal entry."),"""

code = code.replace(old_raci_row, new_raci_row)

# 3. Update all step titles in ALL_SECTIONS where [Finance] was used for OINV
# Pattern: [Finance] Post Direct ... (OINV) -> [Logistics] Post Direct ... (OINV)
# or [Finance] Post ... OINV
code = re.sub(
    r'\[Finance\]\s+Post\s+(Direct[^"]*OINV[^"]*)',
    r'[Logistics] Post \1',
    code
)

# Replace any remaining "[Finance] Post ... (OINV)" if any
code = re.sub(
    r'\[Finance\]\s+Post\s+([^"]*OINV[^"]*)',
    r'[Logistics] Post \1',
    code
)

with open(proc_file, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully updated process_data.py with Logistics OINV responsibility!")
