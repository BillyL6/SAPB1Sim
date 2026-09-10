import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from process_data import PRINCIPLES_DATA, POLICIES_DATA, RACI_DATA, INDEX_DATA, ALL_SECTIONS

def create_workbook():
    wb = openpyxl.Workbook()
    wb.remove(wb.active) # Remove default sheet
    
    # -------------------------------------------------------------
    # STYLES & COLOR PALETTE
    # -------------------------------------------------------------
    navy_header = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    section_banner_fill = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
    l3_banner_fill = PatternFill(start_color="34495E", end_color="34495E", fill_type="solid")
    light_zebra = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    highlight_fill = PatternFill(start_color="EBF5FB", end_color="EBF5FB", fill_type="solid")
    
    title_font = Font(name="Calibri", size=15, bold=True, color="1B365D")
    subtitle_font = Font(name="Calibri", size=11, italic=True, color="566573")
    white_font_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    section_title_font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    l3_title_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=10, bold=True, color="2C3E50")
    regular_font = Font(name="Calibri", size=10, color="2C3E50")
    code_font = Font(name="Consolas", size=9.5, bold=True, color="1A5276")
    
    thin_side = Side(border_style="thin", color="D5D8DC")
    border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    # =============================================================
    # TAB 1: Process Design Principles & Policies
    # =============================================================
    ws1 = wb.create_sheet(title="Principles & Policies")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1["A1"] = "SAP Business One Enterprise Supply Chain: Process Design Principles & Governance"
    ws1["A1"].font = title_font
    ws1["A2"] = "Master Governance Framework, Multi-Currency Rules, Direct AR Invoicing, and Intercompany Accounting Policies for E2E-P2F"
    ws1["A2"].font = subtitle_font
    
    headers1 = ["Policy Code", "Policy Name", "Scope & Applicability", "Mandatory Policy Statement & Operational Rules", "SAP B1 System Implementation & G/L Impact"]
    for col_idx, h in enumerate(headers1, 1):
        cell = ws1.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws1.row_dimensions[4].height = 28
    
    for row_idx, data in enumerate(POLICIES_DATA, 5):
        for col_idx, val in enumerate(data, 1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=val)
            cell.font = bold_font if col_idx <= 2 else regular_font
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = border
            if row_idx % 2 == 0:
                cell.fill = light_zebra
        ws1.row_dimensions[row_idx].height = 80
        
    ws1.column_dimensions["A"].width = 16
    ws1.column_dimensions["B"].width = 30
    ws1.column_dimensions["C"].width = 24
    ws1.column_dimensions["D"].width = 50
    ws1.column_dimensions["E"].width = 45

    # =============================================================
    # TAB 2: Enterprise RACI Governance Matrix
    # =============================================================
    ws_raci = wb.create_sheet(title="RACI Governance Matrix")
    ws_raci.views.sheetView[0].showGridLines = True
    
    ws_raci["A1"] = "SAP Business One Enterprise RACI Governance Matrix"
    ws_raci["A1"].font = title_font
    ws_raci["A2"] = "Role Accountability & Document Ownership: Purchasing, Logistics, Finance, Sales & Corporate Treasury"
    ws_raci["A2"].font = subtitle_font
    
    headers_raci = ["Supply Chain Functional Activity", "ERP Document", "Currency", "Accountable & Responsible Role", "RACI Status", "Consulted (C) & Informed (I)", "Operational Responsibility Scope & Transactional Boundary"]
    for col_idx, h in enumerate(headers_raci, 1):
        cell = ws_raci.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_raci.row_dimensions[4].height = 28
    
    for row_idx, data in enumerate(RACI_DATA, 5):
        for col_idx, val in enumerate(data, 1):
            cell = ws_raci.cell(row=row_idx, column=col_idx, value=val)
            if col_idx in [2, 3]:
                cell.font = code_font if col_idx == 2 else bold_font
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx in [1, 4, 5]:
                cell.font = bold_font
                cell.alignment = Alignment(vertical="top", wrap_text=True)
            else:
                cell.font = regular_font
                cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = border
            if row_idx % 2 == 0:
                cell.fill = light_zebra
        ws_raci.row_dimensions[row_idx].height = 55
        
    ws_raci.column_dimensions["A"].width = 30
    ws_raci.column_dimensions["B"].width = 18
    ws_raci.column_dimensions["C"].width = 12
    ws_raci.column_dimensions["D"].width = 24
    ws_raci.column_dimensions["E"].width = 26
    ws_raci.column_dimensions["F"].width = 28
    ws_raci.column_dimensions["G"].width = 50

    # =============================================================
    # TAB 3: Process Hierarchy Register (Index)
    # =============================================================
    ws2 = wb.create_sheet(title="Hierarchy Register (Index)")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2["A1"] = "SAP Business One Process Hierarchy Register (Index)"
    ws2["A1"].font = title_font
    ws2["A2"] = "Master Directory of 5 Node Groups and 28 Level 3 Supply Network Routes & Control Workflows (Direct Invoicing)"
    ws2["A2"].font = subtitle_font
    
    headers2 = ["Level 2 Group", "Level 3 Code", "Process Pathway & Title", "Operating DBs", "Origin Node", "Transit Node", "Destination Node", "Primary Valuation & Costing Mechanism", "Key SAP B1 Documents"]
    for col_idx, h in enumerate(headers2, 1):
        cell = ws2.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws2.row_dimensions[4].height = 28
    
    for row_idx, data in enumerate(INDEX_DATA, 5):
        for col_idx, val in enumerate(data, 1):
            cell = ws2.cell(row=row_idx, column=col_idx, value=val)
            if col_idx in [1, 2]:
                cell.font = bold_font
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx in [4, 5, 6, 7]:
                cell.font = regular_font
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            elif col_idx == 9:
                cell.font = code_font
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            else:
                cell.font = regular_font
                cell.alignment = Alignment(vertical="center", wrap_text=True)
            cell.border = border
            if row_idx % 2 == 0:
                cell.fill = light_zebra
        ws2.row_dimensions[row_idx].height = 32
        
    ws2.column_dimensions["A"].width = 24
    ws2.column_dimensions["B"].width = 14
    ws2.column_dimensions["C"].width = 52
    ws2.column_dimensions["D"].width = 18
    ws2.column_dimensions["E"].width = 14
    ws2.column_dimensions["F"].width = 22
    ws2.column_dimensions["G"].width = 18
    ws2.column_dimensions["H"].width = 54
    ws2.column_dimensions["I"].width = 38

    # =============================================================
    # TAB 3: Master Step Design Matrix (Level 4 Operational Procedures)
    # =============================================================
    ws3 = wb.create_sheet(title="Master Process Step Matrix")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3["A1"] = "SAP Business One Master Process Step Design Matrix (Level 4 Detail)"
    ws3["A1"].font = title_font
    ws3["A2"] = "Complete Operational Steps, SAP B1 Database Tables, Warehouses, Accounting Entries, and Moving Average Valuation Impacts"
    ws3["A2"].font = subtitle_font
    
    headers3 = [
        "Level 3 Code",
        "Step Code (L4)",
        "Step Name / Description",
        "SAP B1 Document & Database",
        "Source DB",
        "Warehouse / Hub",
        "OnHand Snapshot (OITW)",
        "Inventory Valuation Calculation & Cost Flow",
        "Chart of Accounts (CoA) G/L Entry (OJDT / JDT1)"
    ]
    for col_idx, h in enumerate(headers3, 1):
        cell = ws3.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws3.row_dimensions[4].height = 30
    
    current_row = 5
    
    for sec in ALL_SECTIONS:
        # Write Section Banner
        ws3.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=9)
        sec_cell = ws3.cell(row=current_row, column=1, value=sec["section_banner"])
        sec_cell.font = section_title_font
        sec_cell.fill = section_banner_fill
        sec_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws3.row_dimensions[current_row].height = 28
        current_row += 1
        
        for proc in sec["processes"]:
            # Write Level 3 Process Banner
            ws3.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=9)
            l3_cell = ws3.cell(row=current_row, column=1, value=proc["l3_banner"])
            l3_cell.font = l3_title_font
            l3_cell.fill = l3_banner_fill
            l3_cell.alignment = Alignment(horizontal="left", vertical="center", indent=2)
            ws3.row_dimensions[current_row].height = 24
            current_row += 1
            
            # Write Step Rows
            for step_data in proc["steps"]:
                for col_idx, val in enumerate(step_data, 1):
                    cell = ws3.cell(row=current_row, column=col_idx, value=val)
                    if col_idx in [1, 2]:
                        cell.font = code_font
                        cell.alignment = Alignment(horizontal="center", vertical="top")
                    elif col_idx in [4, 5, 6]:
                        cell.font = bold_font
                        cell.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
                    else:
                        cell.font = regular_font
                        cell.alignment = Alignment(vertical="top", wrap_text=True)
                    cell.border = border
                    if current_row % 2 == 0:
                        cell.fill = light_zebra
                ws3.row_dimensions[current_row].height = 65
                current_row += 1
                
            # Subtle spacer row between processes
            current_row += 1
            
        # Spacer row between sections
        current_row += 1
        
    ws3.column_dimensions["A"].width = 14
    ws3.column_dimensions["B"].width = 14
    ws3.column_dimensions["C"].width = 34
    ws3.column_dimensions["D"].width = 24
    ws3.column_dimensions["E"].width = 16
    ws3.column_dimensions["F"].width = 24
    ws3.column_dimensions["G"].width = 28
    ws3.column_dimensions["H"].width = 48
    ws3.column_dimensions["I"].width = 52

    # Freeze panes on all sheets (at row 5)
    ws1.freeze_panes = "A5"
    ws2.freeze_panes = "A5"
    ws3.freeze_panes = "A5"

    output_path = "/Users/billy/SAPB1_Sim/SAP_B1_Process_Design_Matrix.xlsx"
    wb.save(output_path)
    print(f"Successfully generated full 28-process matrix with Universal Direct AR Invoicing at {output_path}")

if __name__ == "__main__":
    create_workbook()
