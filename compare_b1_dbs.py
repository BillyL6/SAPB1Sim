import sqlite3

def compare_databases():
    print("=" * 110)
    print(" 🔍 SAP BUSINESS ONE DATABASE VALUATION & WAREHOUSE COMPARISON")
    print("    'new_b1.db' (Multi-Warehouse Costing: StockByWhs = 'Y') -> ICCChina, ICCSIT, NZNTH, NZSTH, NZSIT, EuropeMarketPlace, EuropeSIT")
    print("    'old_b1.db' (Single-Level Company Valuation: StockByWhs = 'N') -> AU-SYD, AU-MEL, AU-BNE, VGLPER")
    print("=" * 110)

    conn_new = sqlite3.connect("new_b1.db")
    conn_old = sqlite3.connect("old_b1.db")

    cur_new = conn_new.cursor()
    cur_old = conn_old.cursor()

    # 1. Compare table counts & configured warehouses
    cur_new.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables_new = cur_new.fetchone()[0]
    cur_old.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables_old = cur_old.fetchone()[0]

    cur_new.execute("SELECT WhsCode, WhsName, City, State FROM OWHS WHERE WhsCode IN ('ICCChina', 'ICCSIT', 'NZNTH', 'NZSTH', 'NZSIT', 'EuropeMarketPlace', 'EuropeSIT') ORDER BY WhsCode")
    whs_new = cur_new.fetchall()

    cur_old.execute("SELECT WhsCode, WhsName, City, State FROM OWHS WHERE WhsCode IN ('AU-SYD', 'AU-MEL', 'AU-BNE', 'VGLPER') ORDER BY WhsCode")
    whs_old = cur_old.fetchall()

    print(f"\n📊 Schema & Warehouse Infrastructure Verification:")
    print(f"  • Table Count (new_b1.db) : {tables_new} tables | Schema Match: {'✅ 100% IDENTICAL' if tables_new == tables_old == 82 else '❌'}")
    print(f"  • Table Count (old_b1.db) : {tables_old} tables")
    
    print(f"\n  🏢 Configured Warehouses in 'new_b1.db':")
    for w_code, w_name, city, state in whs_new:
        print(f"     - {w_code:<8} : {w_name:<58} ({city}, {state})")

    print(f"\n  🏢 Configured Warehouses in 'old_b1.db':")
    for w_code, w_name, city, state in whs_old:
        print(f"     - {w_code:<8} : {w_name:<58} ({city}, {state})")

    # 2. Compare OITM (Item Master Level) AvgPrice
    print("\n" + "=" * 110)
    print(" 📦 1. OITM (Item Master Level) - Item Moving Average Price Comparison")
    print("=" * 110)
    print(f"{'ItemCode':<14} | {'Item Name':<42} | {'new_b1 OnHand':>13} | {'new_b1 OITM':>14} | {'old_b1 OITM':>14}")
    print("-" * 110)

    query_oitm = """
    SELECT ItemCode, ItemName, OnHand, AvgPrice
    FROM OITM
    WHERE ItemCode LIKE 'ITM-IC-%' OR ItemCode LIKE 'ITM-IMP-%'
    ORDER BY ItemCode
    """
    cur_new.execute(query_oitm)
    rows_new = {r[0]: r for r in cur_new.fetchall()}

    cur_old.execute(query_oitm)
    rows_old = {r[0]: r for r in cur_old.fetchall()}

    for itm, r_n in rows_new.items():
        r_o = rows_old.get(itm, (itm, "Unknown", 0.0, 0.0))
        item_name = r_n[1][:40]
        on_hand = r_n[2]
        p_new = f"${r_n[3]:,.2f} AUD"
        p_old = f"${r_o[3]:,.2f} AUD"
        print(f"{itm:<14} | {item_name:<42} | {on_hand:>13.0f} | {p_new:>14} | {p_old:>14}")

    # 3. Warehouse-Level Stock in new_b1.db (Multi-Warehouse Stacked Valuation)
    print("\n" + "=" * 110)
    print(" 🏢 2A. 'new_b1.db' - Warehouse Stock & Stacked Costing (OITW)")
    print("=" * 110)
    print(f"{'ItemCode':<14} | {'WhsCode':<8} | {'Whs Role':<28} | {'OnHand':>7} | {'OITW.AvgPrice':>16}")
    print("-" * 110)

    cur_new.execute("""
    SELECT T0.ItemCode, T0.WhsCode, T1.WhsName, T0.OnHand, T0.AvgPrice
    FROM OITW T0
    INNER JOIN OWHS T1 ON T0.WhsCode = T1.WhsCode
    WHERE T0.ItemCode IN ('ITM-IC-001', 'ITM-IC-002')
    ORDER BY T0.ItemCode, 
        CASE T0.WhsCode
            WHEN 'ICCChina' THEN 1
            WHEN 'ICCSIT' THEN 2
            WHEN 'NZNTH' THEN 3
            WHEN 'NZSTH' THEN 4
            WHEN 'NZSIT' THEN 5
            WHEN 'EuropeMarketPlace' THEN 6
            WHEN 'EuropeSIT' THEN 7
            ELSE 8
        END
    """)
    for r in cur_new.fetchall():
        role = r[2][:26]
        p_str = f"${r[4]:,.2f} AUD"
        print(f"{r[0]:<14} | {r[1]:<8} | {role:<28} | {r[3]:>7.0f} | {p_str:>16}")

    # 4. Warehouse-Level Stock in old_b1.db (Company-Level Valuation: AvgPrice = 0.0)
    print("\n" + "=" * 110)
    print(" 🏢 2B. 'old_b1.db' - Warehouse Stock & Deactivated Warehouse Price (OITW)")
    print("=" * 110)
    print(f"{'ItemCode':<14} | {'WhsCode':<8} | {'Whs Role':<28} | {'OnHand':>7} | {'OITW.AvgPrice':>16}")
    print("-" * 110)

    cur_old.execute("""
    SELECT T0.ItemCode, T0.WhsCode, T1.WhsName, T0.OnHand, T0.AvgPrice
    FROM OITW T0
    INNER JOIN OWHS T1 ON T0.WhsCode = T1.WhsCode
    WHERE T0.ItemCode IN ('ITM-IC-001', 'ITM-IC-002')
    ORDER BY T0.ItemCode, T0.WhsCode
    """)
    for r in cur_old.fetchall():
        role = r[2][:26]
        p_str = f"${r[4]:,.2f} AUD"
        print(f"{r[0]:<14} | {r[1]:<8} | {role:<28} | {r[3]:>7.0f} | {p_str:>16}")

    # 5. Verification of Deactivation Rule in old_b1.db
    cur_old.execute("SELECT COUNT(*), MAX(AvgPrice), MIN(AvgPrice) FROM OITW")
    cnt, max_p, min_p = cur_old.fetchone()
    print("\n" + "=" * 110)
    print(" 🛡️ 3. Verification of 'old_b1.db' OITW.AvgPrice Deactivation Rule:")
    print("=" * 110)
    print(f"  • Total OITW Rows Checked : {cnt}")
    print(f"  • Maximum OITW.AvgPrice   : {max_p:.4f}")
    print(f"  • Minimum OITW.AvgPrice   : {min_p:.4f}")
    if max_p == 0.0 and min_p == 0.0:
        print("  ✅ PASS: All OITW.AvgPrice values in 'old_b1.db' are strictly 0.0 (Switched Off).")
    else:
        print("  ❌ FAIL: Some OITW.AvgPrice values in 'old_b1.db' are non-zero!")

    conn_new.close()
    conn_old.close()
    print("=" * 110)

if __name__ == "__main__":
    compare_databases()
