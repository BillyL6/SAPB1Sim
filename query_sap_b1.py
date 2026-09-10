import sqlite3
import sys

def run_showcase(db_name="new_b1.db"):
    if len(sys.argv) > 1:
        db_name = sys.argv[1]

    print(f"📊 Connecting to database: '{db_name}'...")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    def print_section(title, query):
        print(f"\n=========================================================================================================")
        print(f" 🔍 {title}")
        print(f"=========================================================================================================")
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print("  (0 rows)")
            return
        col_names = [desc[0] for desc in cursor.description]
        col_widths = [len(c) for c in col_names]
        str_rows = []
        for row in rows:
            str_row = [str(val) if val is not None else "NULL" for val in row]
            str_rows.append(str_row)
            for i, val in enumerate(str_row):
                col_widths[i] = max(col_widths[i], len(val))
        
        header = " | ".join(name.ljust(col_widths[i]) for i, name in enumerate(col_names))
        divider = "-+-".join("-" * col_widths[i] for i in range(len(col_names)))
        print(header)
        print(divider)
        for r in str_rows[:8]:
            print(" | ".join(val.ljust(col_widths[i]) for i, val in enumerate(r)))

    # 1. Multi-Warehouse Stock Availability
    print_section(
        "1. Multi-Warehouse Stock Levels (OITW + OWHS + OITM)",
        """
        SELECT 
            T0.ItemCode,
            T1.ItemName,
            T0.WhsCode,
            T2.WhsName,
            T0.OnHand AS Stock,
            T0.IsCommited AS Committed,
            T0.OnOrder AS On_PO,
            (T0.OnHand - T0.IsCommited + T0.OnOrder) AS Available
        FROM OITW T0
        INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
        INNER JOIN OWHS T2 ON T0.WhsCode = T2.WhsCode
        ORDER BY T0.ItemCode, T0.WhsCode
        LIMIT 6;
        """
    )

    # 2. Financial Journal Entry Lines
    print_section(
        "2. Balanced Financial Journal Entries (OJDT + JDT1 + OACT)",
        """
        SELECT 
            T0.TransId AS JE_Num,
            T0.RefDate AS Posting_Date,
            T0.Memo,
            T1.Account AS GL_Account,
            T2.AcctName AS Account_Name,
            T1.Debit,
            T1.Credit
        FROM OJDT T0
        INNER JOIN JDT1 T1 ON T0.TransId = T1.TransId
        INNER JOIN OACT T2 ON T1.Account = T2.AcctCode
        ORDER BY T0.TransId, T1.Line_ID
        LIMIT 6;
        """
    )

    # 3. Banking & Cash Flow - Incoming Payments vs AR Invoices
    print_section(
        "3. Order-to-Cash (O2C) Incoming Payments Settlement (ORCT + RCT2 + OINV)",
        """
        SELECT 
            T0.DocNum AS Payment_Num,
            T0.DocDate AS Payment_Date,
            T0.CardCode,
            T0.CardName AS Customer_Name,
            T1.InvoiceId AS Paid_Invoice_Entry,
            T2.DocNum AS Invoice_DocNum,
            T1.SumApplied AS Amount_Settled,
            T0.DocTotal AS Payment_Total,
            T0.PrjCode AS Project_Code
        FROM ORCT T0
        INNER JOIN RCT2 T1 ON T0.DocEntry = T1.DocEntry
        LEFT JOIN OINV T2 ON T1.InvoiceId = T2.DocEntry
        ORDER BY T0.DocNum
        LIMIT 6;
        """
    )

    # 4. Outgoing Payments to Vendors
    print_section(
        "4. Procure-to-Pay (P2P) Outgoing Disbursements (OVPM + VPM2 + OPCH)",
        """
        SELECT 
            T0.DocNum AS Payment_Num,
            T0.DocDate AS Payment_Date,
            T0.CardCode,
            T0.CardName AS Vendor_Name,
            T1.InvoiceId AS AP_Invoice_Entry,
            T2.DocNum AS AP_Invoice_DocNum,
            T1.SumApplied AS Amount_Disbursed,
            T0.DocTotal AS Total_Payment
        FROM OVPM T0
        INNER JOIN VPM2 T1 ON T0.DocEntry = T1.DocEntry
        LEFT JOIN OPCH T2 ON T1.InvoiceId = T2.DocEntry
        ORDER BY T0.DocNum
        LIMIT 6;
        """
    )

    # 5. Bill of Materials (BOM) & Components
    print_section(
        "5. Bill of Materials (BOM) Multi-Level Structure (OITT + ITT1 + OITM)",
        """
        SELECT 
            T0.Code AS Parent_ItemCode,
            T1.ItemName AS Parent_Name,
            T2.Code AS Child_Component,
            T3.ItemName AS Component_Name,
            T2.Quantity AS Qty_Required,
            T2.Price AS Component_Unit_Cost,
            (T2.Quantity * T2.Price) AS Total_Component_Cost
        FROM OITT T0
        INNER JOIN OITM T1 ON T0.Code = T1.ItemCode
        INNER JOIN ITT1 T2 ON T0.Code = T2.Father
        INNER JOIN OITM T3 ON T2.Code = T3.ItemCode
        ORDER BY T0.Code, T2.ChildNum
        LIMIT 6;
        """
    )

    # 6. Production Orders & Work in Progress
    print_section(
        "6. Manufacturing Work Orders & WIP Tracking (OWOR + WOR1 + OITM)",
        """
        SELECT 
            T0.DocNum AS Work_Order,
            T0.PostDate AS Order_Date,
            T0.ItemCode AS Assembly_Item,
            T1.ItemName AS Assembly_Name,
            T0.PlannedQty AS Target_Qty,
            T0.CmpltQty AS Completed_Qty,
            T2.ItemCode AS Component_Code,
            T2.PlannedQty AS Comp_Planned,
            T2.IssuedQty AS Comp_Issued
        FROM OWOR T0
        INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
        INNER JOIN WOR1 T2 ON T0.DocEntry = T2.DocEntry
        ORDER BY T0.DocNum
        LIMIT 6;
        """
    )

    # 7. Multi-Tier Price Lists & Matrix
    print_section(
        "7. Multi-Tier Price Lists Matrix (OPLN + ITM1 + OITM)",
        """
        SELECT 
            T0.ItemCode,
            T2.ItemName,
            T1.ListName AS Price_List,
            T0.Price,
            T0.Currency,
            T1.Factor AS Markup_Factor
        FROM ITM1 T0
        INNER JOIN OPLN T1 ON T0.PriceList = T1.ListNum
        INNER JOIN OITM T2 ON T0.ItemCode = T2.ItemCode
        ORDER BY T0.ItemCode, T0.PriceList
        LIMIT 10;
        """
    )

    # 8. Batch Traceability & Expiration Audit
    print_section(
        "8. Batch Traceability & Expiry Monitoring (OBTN + OITM + OWHS)",
        """
        SELECT 
            T0.DistNumber AS Batch_Number,
            T0.ItemCode,
            T1.ItemName,
            T0.WhsCode,
            T2.WhsName,
            T0.Quantity AS Batch_Stock,
            T0.InDate AS Received_Date,
            T0.ExpDate AS Expiry_Date
        FROM OBTN T0
        INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
        INNER JOIN OWHS T2 ON T0.WhsCode = T2.WhsCode
        ORDER BY T0.ExpDate ASC
        LIMIT 6;
        """
    )

    # 9. CRM Sales Opportunities & Pipeline
    print_section(
        "9. CRM Sales Opportunity Pipeline & Win Rates (OOPR + OCRD)",
        """
        SELECT 
            T0.OpprId AS Opp_ID,
            T0.Name AS Opportunity_Name,
            T0.CardCode,
            T1.CardName AS Customer_Name,
            T0.MaxSumLoc AS Potential_Revenue,
            T0.ClosePrcnt AS Win_Probability_Pct,
            CASE T0.Status
                WHEN 'W' THEN 'Won'
                WHEN 'O' THEN 'In Progress'
                WHEN 'L' THEN 'Lost'
            END AS Stage_Status,
            T0.OpenDate,
            T0.CloseDate
        FROM OOPR T0
        INNER JOIN OCRD T1 ON T0.CardCode = T1.CardCode
        ORDER BY T0.MaxSumLoc DESC
        LIMIT 6;
        """
    )

    # 10. Project Management & Stage Milestones
    print_section(
        "10. Project Management & Milestone Execution (OPMG + PMG1 + OCRD)",
        """
        SELECT 
            T0.PrjCode AS Project_Code,
            T0.PrjName AS Project_Name,
            T2.CardName AS Client_Name,
            T0.PlanCost AS Budget,
            T0.ActualCost AS Spend_To_Date,
            T1.StageID AS Stage_Num,
            T1.Task AS Milestone_Task,
            T1.PlanCost AS Stage_Cost
        FROM OPMG T0
        INNER JOIN PMG1 T1 ON T0.AbsEntry = T1.AbsEntry
        INNER JOIN OCRD T2 ON T0.CardCode = T2.CardCode
        ORDER BY T0.PrjCode, T1.StageID
        LIMIT 6;
        """
    )

    # 11. Landed Cost Allocations with GRPO & Warehouse Valuation
    print_section(
        "11. Landed Costs & GRPO Multi-Warehouse Valuation (OIPF + IPF1 + OPDN + OITW + OITM)",
        """
        SELECT 
            T0.DocNum AS LC_Doc,
            T0.DocDate,
            T2.DocNum AS GRPO_Doc,
            T1.ItemCode,
            T1.WhsCode AS Whs,
            T1.OrigCost AS Base_Cost,
            T1.AllocSum AS Landed_Fee,
            ROUND(T1.OrigCost + (T1.AllocSum / T1.Quantity), 2) AS Unit_Landed_Cost,
            T4.AvgPrice AS Whs_AvgPrice,
            T5.AvgPrice AS ItemMaster_AvgPrice
        FROM OIPF T0
        INNER JOIN IPF1 T1 ON T0.DocEntry = T1.DocEntry
        INNER JOIN OPDN T2 ON T1.BaseEntry = T2.DocEntry
        INNER JOIN OITW T4 ON T1.ItemCode = T4.ItemCode AND T1.WhsCode = T4.WhsCode
        INNER JOIN OITM T5 ON T1.ItemCode = T5.ItemCode
        WHERE T1.ItemCode LIKE 'ITM-IMP-%'
        ORDER BY T1.ItemCode, T1.WhsCode
        LIMIT 9;
        """
    )

    # 11B. Factory PO (USD) to GRPO Conversion (AUD) Audit
    print_section(
        "11B. Factory PO (USD) to GRPO (AUD) Spot Rate Conversion at ICC (OPOR + POR1 + OPDN + PDN1)",
        """
        SELECT 
            T0.DocNum AS PO_Num,
            T0.DocCur AS PO_Cur,
            T1.ItemCode,
            T1.PriceFC AS FOB_USD,
            T1.TotalFrgn AS Total_USD,
            T2.DocRate AS GRPO_Rate,
            T2.DocNum AS GRPO_Num,
            T3.Price AS Converted_FOB_AUD,
            T3.LineTotal AS Total_AUD,
            T3.WhsCode AS Whs
        FROM OPOR T0
        INNER JOIN POR1 T1 ON T0.DocEntry = T1.DocEntry
        INNER JOIN OPDN T2 ON T0.DocEntry = T2.BaseEntry
        INNER JOIN PDN1 T3 ON T2.DocEntry = T3.DocEntry
        WHERE T0.DocNum >= 5900
        ORDER BY T0.DocNum;
        """
    )

    # 11C. Intercompany Transfer & Stacked Landed Cost Journey (AUD)
    print_section(
        "11C. Multi-Leg Stacked Landed Cost Journey in AUD",
        """
        SELECT 
            T0.ItemCode,
            T1.ItemName,
            T0.WhsCode,
            T2.WhsName,
            T0.AvgPrice AS Stacked_Cost_AUD,
            T0.OnHand AS Stock_Qty,
            T1.AvgPrice AS Enterprise_AvgPrice_AUD
        FROM OITW T0
        INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
        INNER JOIN OWHS T2 ON T0.WhsCode = T2.WhsCode
        WHERE T0.ItemCode LIKE 'ITM-IC-%'
        ORDER BY T0.ItemCode, 
            CASE T0.WhsCode 
                WHEN 'ICCNGB' THEN 1 
                WHEN 'ICCSIT' THEN 2 
                WHEN 'NZNTH'  THEN 3 
                WHEN 'NZSTH'  THEN 4 
                WHEN 'NZSIT'  THEN 5 
                WHEN 'UKWYF'  THEN 6 
                WHEN 'UKSIT'  THEN 7 
                WHEN 'FDMSYD' THEN 1
                WHEN 'BDLMEL' THEN 2
                WHEN 'MFTBNE' THEN 3
                WHEN 'VGLPER' THEN 4
                ELSE 8 
            END
        LIMIT 15;
        """
    )

    # 12. Warehouse Inventory Valuation Log
    print_section(
        "12. Inventory Valuation Audit Log (OINM - Warehouse Journal)",
        """
        SELECT 
            T0.TransSeq,
            T0.DocDate,
            T0.ItemCode,
            CASE T0.TransType 
                WHEN 20 THEN 'GRPO Inward'
                WHEN 15 THEN 'Delivery Out'
                WHEN 67 THEN 'Whs Transfer'
                WHEN 59 THEN 'Receipt from Prod'
                WHEN 60 THEN 'Issue to Prod'
                ELSE 'Other Movement'
            END AS Movement_Type,
            T0.InQty,
            T0.OutQty,
            T0.Price AS Unit_Cost,
            T0.TransValue AS Total_Movement_Val,
            T0.Warehouse
        FROM OINM T0
        ORDER BY T0.TransSeq
        LIMIT 6;
        """
    )

    conn.close()

if __name__ == "__main__":
    run_showcase()
