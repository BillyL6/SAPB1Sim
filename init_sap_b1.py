import sqlite3
import random
from datetime import datetime, timedelta

def init_database(db_name="new_b1.db", stock_by_whs=True):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Optimization for fast bulk creation
    cursor.execute("PRAGMA synchronous = OFF;")
    cursor.execute("PRAGMA journal_mode = MEMORY;")

    print(f" Creating comprehensive 82-table SAP Business One schema for '{db_name}'...")
    if stock_by_whs:
        print(" ⚙️ SYSTEM CONFIGURATION: 'Manage Stock by Warehouse' = 'Y' (Multi-Warehouse Costing)")
        print(" 🏢 ACTIVE WAREHOUSES: ICCChina, ICCSIT, NZNTH, NZSTH, NZSIT, EuropeMarketPlace, EuropeSIT")
    else:
        print(" ⚙️ SYSTEM CONFIGURATION: 'Manage Stock by Warehouse' = 'N' (Company-Level Valuation Only)")
        print(" 🏢 ACTIVE WAREHOUSES: AU Warehouse, AU Warehouse, AU Warehouse, VGLPER")
        print(" ⚙️ OITW.AvgPrice is DISABLED (0.0). All inventory cost is accumulated at OITM.AvgPrice.")

    all_tables = [
        # 1. Audit & Inventory Valuation
        "ADT1", "ADOC", "OINM",
        # 2. Inventory Transfers & Warehouse Management
        "WTR1", "OWTR", "WTQ1", "OWTQ", "INC1", "OINC", "OBIN",
        # 3. Traceability (Batches & Serials)
        "ITL1", "OITL", "OSRN", "OBTN",
        # 4. Landed Costs & Reconciliation
        "ITR1", "OITR", "OJDT", "JDT1", "IPF2", "IPF1", "OIPF", "OALC",
        # 5. Banking & Payments
        "VPM2", "OVPM", "RCT2", "ORCT", "ODSC", "OCTG",
        # 6. Sales & Accounts Receivable (AR)
        "RIN1", "ORIN", "INV1", "OINV", "RDN1", "ORDN", "DLN1", "ODLN", "RDR1", "ORDR", "QUT1", "OQUT",
        # 7. Purchasing & Accounts Payable (AP)
        "RPC1", "ORPC", "PCH1", "OPCH", "PDN1", "OPDN", "POR1", "OPOR", "PQT1", "OPQT", "PRQ1", "OPRQ",
        # 8. Production & Manufacturing (BOM & Work Orders)
        "IGE1", "OIGE", "IGN1", "OIGN", "WOR1", "OWOR", "ITT1", "OITT",
        # 9. Pricing, Tax & Special Conditions
        "OSTC", "SPP1", "OSPP", "ITM1", "OPLN",
        # 10. CRM & Business Partner Sub-Masters
        "OCLG", "OPR1", "OOPR", "OCRG", "CRD1", "OCPR",
        # 11. Cost Accounting, Projects & Budgets
        "BGT1", "OBGT", "PMG1", "OPMG", "OPRC", "ODIM",
        # 12. Master Data & Chart of Accounts
        "OITW", "OITM", "OCRD", "OWHS", "OACT"
    ]

    for tbl in all_tables:
        cursor.execute(f"DROP TABLE IF EXISTS {tbl};")

    # -------------------------------------------------------------
    # 1. Master Data & Chart of Accounts
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OACT (
        AcctCode TEXT PRIMARY KEY,
        AcctName TEXT NOT NULL,
        CurrTotal REAL DEFAULT 0.0,
        LocManTran TEXT DEFAULT 'N',
        Financ TEXT DEFAULT 'Y',
        ActType TEXT DEFAULT 'N',
        Levels INTEGER DEFAULT 3
    );
    """)

    cursor.execute("""
    CREATE TABLE OWHS (
        WhsCode TEXT PRIMARY KEY,
        WhsName TEXT NOT NULL,
        Building TEXT,
        Street TEXT,
        City TEXT DEFAULT 'Sydney',
        State TEXT DEFAULT 'NSW',
        ZipCode TEXT DEFAULT '2000'
    );
    """)

    cursor.execute("""
    CREATE TABLE OCRD (
        CardCode TEXT PRIMARY KEY,
        CardName TEXT NOT NULL,
        CardType TEXT CHECK(CardType IN ('C', 'S')),
        GroupCode INTEGER,
        Phone TEXT,
        Currency TEXT DEFAULT 'AUD',
        Balance REAL DEFAULT 0.0,
        DebPayAcct TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE OITM (
        ItemCode TEXT PRIMARY KEY,
        ItemName TEXT NOT NULL,
        ItmsGrpCod INTEGER,
        OnHand REAL DEFAULT 0.0,
        IsCommited REAL DEFAULT 0.0,
        OnOrder REAL DEFAULT 0.0,
        AvgPrice REAL DEFAULT 0.0,
        DfltWH TEXT DEFAULT '01'
    );
    """)

    cursor.execute("""
    CREATE TABLE OITW (
        ItemCode TEXT NOT NULL,
        WhsCode TEXT NOT NULL,
        OnHand REAL DEFAULT 0.0,
        IsCommited REAL DEFAULT 0.0,
        OnOrder REAL DEFAULT 0.0,
        AvgPrice REAL DEFAULT 0.0,
        MinStock REAL DEFAULT 10.0,
        MaxStock REAL DEFAULT 500.0,
        PRIMARY KEY (ItemCode, WhsCode)
    );
    """)

    # -------------------------------------------------------------
    # 2. Purchasing / AP Tables
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OPRQ (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT NOT NULL,
        ReqName TEXT NOT NULL,
        ReqType INTEGER DEFAULT 1,
        DocStatus TEXT DEFAULT 'C',
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE PRQ1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL DEFAULT 1.0,
        Price REAL DEFAULT 0.0,
        LineTotal REAL DEFAULT 0.0,
        WhsCode TEXT DEFAULT '01',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OPQT (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocStatus TEXT DEFAULT 'C',
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE PQT1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL DEFAULT 1.0,
        Price REAL DEFAULT 0.0,
        LineTotal REAL DEFAULT 0.0,
        WhsCode TEXT DEFAULT '01',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OPOR (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocStatus TEXT CHECK(DocStatus IN ('O', 'C')),
        DocTotal REAL DEFAULT 0.0,
        DocCur TEXT DEFAULT 'AUD',
        DocRate REAL DEFAULT 1.0,
        DocTotalFC REAL DEFAULT 0.0,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE POR1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        PriceFC REAL DEFAULT 0.0,
        TotalFrgn REAL DEFAULT 0.0,
        OpenQty REAL DEFAULT 0.0,
        WhsCode TEXT DEFAULT '01',
        LineStatus TEXT DEFAULT 'C',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OPDN (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocStatus TEXT DEFAULT 'C',
        DocTotal REAL DEFAULT 0.0,
        DocCur TEXT DEFAULT 'AUD',
        DocRate REAL DEFAULT 1.0,
        DocTotalFC REAL DEFAULT 0.0,
        BaseEntry INTEGER,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE PDN1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        PriceFC REAL DEFAULT 0.0,
        TotalFrgn REAL DEFAULT 0.0,
        WhsCode TEXT DEFAULT '01',
        BaseEntry INTEGER,
        BaseLine INTEGER,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OPCH (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocStatus TEXT DEFAULT 'C',
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE PCH1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        WhsCode TEXT DEFAULT '01',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE ORPC (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE RPC1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    # -------------------------------------------------------------
    # 3. Sales / AR Tables
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OQUT (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocStatus TEXT DEFAULT 'C',
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE QUT1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL DEFAULT 1.0,
        Price REAL DEFAULT 0.0,
        LineTotal REAL DEFAULT 0.0,
        WhsCode TEXT DEFAULT '01',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE ORDR (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocStatus TEXT CHECK(DocStatus IN ('O', 'C')),
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE RDR1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        OpenQty REAL DEFAULT 0.0,
        WhsCode TEXT DEFAULT '01',
        LineStatus TEXT DEFAULT 'C',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE ODLN (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocStatus TEXT DEFAULT 'C',
        DocTotal REAL DEFAULT 0.0,
        BaseEntry INTEGER,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE DLN1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        WhsCode TEXT DEFAULT '01',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE ORDN (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocStatus TEXT DEFAULT 'C',
        DocTotal REAL DEFAULT 0.0,
        BaseEntry INTEGER,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE RDN1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL DEFAULT 1.0,
        Price REAL DEFAULT 0.0,
        LineTotal REAL DEFAULT 0.0,
        WhsCode TEXT DEFAULT '01',
        BaseEntry INTEGER,
        BaseLine INTEGER,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OINV (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocStatus TEXT DEFAULT 'C',
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE INV1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        WhsCode TEXT DEFAULT '01',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE ORIN (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE RIN1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    # -------------------------------------------------------------
    # 4. Landed Costs & Customs
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OALC (
        AlcCode TEXT PRIMARY KEY,
        AlcName TEXT NOT NULL,
        AcctCode TEXT,
        AllocMethod TEXT DEFAULT 'V'
    );
    """)

    cursor.execute("""
    CREATE TABLE OIPF (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        CostSum REAL DEFAULT 0.0,
        DocTotal REAL DEFAULT 0.0,
        DocType TEXT DEFAULT 'A',
        BaseEntry INTEGER,
        WhsCode TEXT DEFAULT '01',
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IPF1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        LineTotal REAL NOT NULL,
        OrigCost REAL NOT NULL,
        AllocSum REAL DEFAULT 0.0,
        BaseEntry INTEGER,
        BaseLine INTEGER,
        BaseType INTEGER DEFAULT 20,
        WhsCode TEXT DEFAULT '01',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE IPF2 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        AlcCode TEXT NOT NULL,
        CostSum REAL NOT NULL,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    # -------------------------------------------------------------
    # 5. Financial Journal Entries & Reconciliation
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OJDT (
        TransId INTEGER PRIMARY KEY AUTOINCREMENT,
        BaseRef INTEGER,
        RefDate TEXT NOT NULL,
        DueDate TEXT,
        TaxDate TEXT,
        Memo TEXT,
        TransType INTEGER DEFAULT 30,
        LocTotal REAL DEFAULT 0.0
    );
    """)

    cursor.execute("""
    CREATE TABLE JDT1 (
        TransId INTEGER NOT NULL,
        Line_ID INTEGER NOT NULL,
        Account TEXT NOT NULL,
        ShortName TEXT,
        Debit REAL DEFAULT 0.0,
        Credit REAL DEFAULT 0.0,
        RefDate TEXT,
        DueDate TEXT,
        LineMemo TEXT,
        PRIMARY KEY (TransId, Line_ID)
    );
    """)

    cursor.execute("""
    CREATE TABLE OITR (
        ReconNum INTEGER PRIMARY KEY AUTOINCREMENT,
        ReconDate TEXT NOT NULL,
        Total REAL DEFAULT 0.0,
        ReconType INTEGER DEFAULT 0,
        ReconCurr TEXT DEFAULT 'AUD',
        IsCard TEXT DEFAULT 'C'
    );
    """)

    cursor.execute("""
    CREATE TABLE ITR1 (
        ReconNum INTEGER NOT NULL,
        LineSeq INTEGER NOT NULL,
        ShortName TEXT,
        TransId INTEGER,
        ReconSum REAL DEFAULT 0.0,
        SrcObjTyp TEXT DEFAULT '30',
        PRIMARY KEY (ReconNum, LineSeq)
    );
    """)

    # -------------------------------------------------------------
    # 6. Banking & Payments
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE ORCT (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocType TEXT DEFAULT 'C',
        TrsfrSum REAL DEFAULT 0.0,
        TrsfrRef TEXT,
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT,
        PrjCode TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE RCT2 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        DocTransId INTEGER,
        InvoiceId INTEGER,
        InvType INTEGER DEFAULT 13,
        SumApplied REAL NOT NULL,
        AppliedFC REAL DEFAULT 0.0,
        Discount REAL DEFAULT 0.0,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OVPM (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT,
        CardCode TEXT NOT NULL,
        CardName TEXT NOT NULL,
        DocType TEXT DEFAULT 'S',
        TrsfrSum REAL DEFAULT 0.0,
        TrsfrRef TEXT,
        DocTotal REAL DEFAULT 0.0,
        Comments TEXT,
        PrjCode TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE VPM2 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        DocTransId INTEGER,
        InvoiceId INTEGER,
        InvType INTEGER DEFAULT 18,
        SumApplied REAL NOT NULL,
        AppliedFC REAL DEFAULT 0.0,
        Discount REAL DEFAULT 0.0,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OCTG (
        GroupNum INTEGER PRIMARY KEY,
        PymntGroup TEXT NOT NULL,
        PayDuMonth INTEGER DEFAULT 0,
        ExtraMonth INTEGER DEFAULT 0,
        ExtraDays INTEGER DEFAULT 30,
        DiscPercent REAL DEFAULT 0.0,
        DiscDays INTEGER DEFAULT 0
    );
    """)

    cursor.execute("""
    CREATE TABLE ODSC (
        BankCode TEXT PRIMARY KEY,
        BankName TEXT NOT NULL,
        Account TEXT,
        Branch TEXT,
        CountryCod TEXT DEFAULT 'AU'
    );
    """)

    # -------------------------------------------------------------
    # 7. Production & Manufacturing (BOM & Work Orders)
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OITT (
        Code TEXT PRIMARY KEY,
        TreeType TEXT DEFAULT 'P',
        Qauntity REAL DEFAULT 1.0,
        PriceList INTEGER DEFAULT 1,
        ToWH TEXT DEFAULT '01',
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE ITT1 (
        Father TEXT NOT NULL,
        ChildNum INTEGER NOT NULL,
        Code TEXT NOT NULL,
        Quantity REAL NOT NULL,
        Price REAL DEFAULT 0.0,
        Warehouse TEXT DEFAULT '01',
        Type TEXT DEFAULT 'M',
        PRIMARY KEY (Father, ChildNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OWOR (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        ItemCode TEXT NOT NULL,
        Status TEXT DEFAULT 'R',
        Type TEXT DEFAULT 'S',
        PlannedQty REAL NOT NULL,
        CmpltQty REAL DEFAULT 0.0,
        RjctQty REAL DEFAULT 0.0,
        PostDate TEXT NOT NULL,
        DueDate TEXT NOT NULL,
        Warehouse TEXT DEFAULT '01',
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE WOR1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        ItemType INTEGER DEFAULT 4,
        PlannedQty REAL NOT NULL,
        IssuedQty REAL DEFAULT 0.0,
        wareHouse TEXT DEFAULT '01',
        IssueType TEXT DEFAULT 'M',
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OIGN (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocTotal REAL DEFAULT 0.0,
        Ref2 TEXT,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IGN1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        WhsCode TEXT DEFAULT '01',
        BaseEntry INTEGER,
        BaseType INTEGER DEFAULT 202,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OIGE (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocTotal REAL DEFAULT 0.0,
        Ref2 TEXT,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IGE1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        LineTotal REAL NOT NULL,
        WhsCode TEXT DEFAULT '01',
        BaseEntry INTEGER,
        BaseType INTEGER DEFAULT 202,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    # -------------------------------------------------------------
    # 8. Inventory Transfers & Warehouse Operations
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OWTQ (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        DocDueDate TEXT,
        FromWhsCod TEXT NOT NULL,
        ToWhsCode TEXT NOT NULL,
        DocStatus TEXT DEFAULT 'C',
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE WTQ1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        OpenQty REAL DEFAULT 0.0,
        FromWhsCod TEXT NOT NULL,
        ToWhsCode TEXT NOT NULL,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OWTR (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        DocDate TEXT NOT NULL,
        FromWhsCod TEXT NOT NULL,
        ToWhsCode TEXT NOT NULL,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE WTR1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        Dscription TEXT,
        Quantity REAL NOT NULL,
        Price REAL NOT NULL,
        FromWhsCod TEXT NOT NULL,
        ToWhsCode TEXT NOT NULL,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OBIN (
        AbsEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        BinCode TEXT UNIQUE NOT NULL,
        WhsCode TEXT NOT NULL,
        SysBin TEXT DEFAULT 'N',
        Disabled TEXT DEFAULT 'N',
        Descr TEXT,
        Aisle TEXT,
        Rack TEXT,
        Shelf TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE OINC (
        DocEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocNum INTEGER UNIQUE NOT NULL,
        CountDate TEXT NOT NULL,
        Time TEXT DEFAULT '08:00',
        Status TEXT DEFAULT 'C',
        Remarks TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE INC1 (
        DocEntry INTEGER NOT NULL,
        LineNum INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        ItemDesc TEXT,
        WhsCode TEXT NOT NULL,
        InWhsQty REAL DEFAULT 0.0,
        CountQty REAL DEFAULT 0.0,
        Difference REAL DEFAULT 0.0,
        PRIMARY KEY (DocEntry, LineNum)
    );
    """)

    # -------------------------------------------------------------
    # 9. Traceability & Batches
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OBTN (
        AbsEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        ItemCode TEXT NOT NULL,
        DistNumber TEXT NOT NULL,
        MnfDate TEXT,
        ExpDate TEXT,
        InDate TEXT NOT NULL,
        Quantity REAL DEFAULT 0.0,
        Status INTEGER DEFAULT 0,
        WhsCode TEXT DEFAULT '01'
    );
    """)

    cursor.execute("""
    CREATE TABLE OSRN (
        AbsEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        ItemCode TEXT NOT NULL,
        DistNumber TEXT NOT NULL,
        MnfSerial TEXT,
        LotNumber TEXT,
        InDate TEXT NOT NULL,
        Status INTEGER DEFAULT 0,
        WhsCode TEXT DEFAULT '01',
        CardCode TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE OITL (
        LogEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        DocType INTEGER NOT NULL,
        DocEntry INTEGER NOT NULL,
        DocLine INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        LocCode TEXT NOT NULL,
        DocQty REAL NOT NULL,
        DocDate TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE ITL1 (
        LogEntry INTEGER NOT NULL,
        ItemCode TEXT NOT NULL,
        MdAbsEntry INTEGER NOT NULL,
        Quantity REAL NOT NULL,
        AllocQty REAL NOT NULL,
        DocType INTEGER DEFAULT 20,
        PRIMARY KEY (LogEntry, MdAbsEntry)
    );
    """)

    # -------------------------------------------------------------
    # 10. Pricing, Tax & Special Conditions
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OPLN (
        ListNum INTEGER PRIMARY KEY,
        ListName TEXT NOT NULL,
        BASE_NUM INTEGER DEFAULT 1,
        Factor REAL DEFAULT 1.0,
        PrimCurr TEXT DEFAULT 'AUD',
        Valid TEXT DEFAULT 'Y'
    );
    """)

    cursor.execute("""
    CREATE TABLE ITM1 (
        ItemCode TEXT NOT NULL,
        PriceList INTEGER NOT NULL,
        Price REAL DEFAULT 0.0,
        Currency TEXT DEFAULT 'AUD',
        Factor REAL DEFAULT 1.0,
        PRIMARY KEY (ItemCode, PriceList)
    );
    """)

    cursor.execute("""
    CREATE TABLE OSPP (
        CardCode TEXT NOT NULL,
        ItemCode TEXT NOT NULL,
        Price REAL NOT NULL,
        Currency TEXT DEFAULT 'AUD',
        Discount REAL DEFAULT 0.0,
        ValidFrom TEXT,
        ValidTo TEXT,
        PRIMARY KEY (CardCode, ItemCode)
    );
    """)

    cursor.execute("""
    CREATE TABLE SPP1 (
        CardCode TEXT NOT NULL,
        ItemCode TEXT NOT NULL,
        LineNum INTEGER NOT NULL,
        Amount REAL NOT NULL,
        Price REAL NOT NULL,
        Discount REAL DEFAULT 0.0,
        PRIMARY KEY (CardCode, ItemCode, LineNum)
    );
    """)

    cursor.execute("""
    CREATE TABLE OSTC (
        Code TEXT PRIMARY KEY,
        Name TEXT NOT NULL,
        Rate REAL DEFAULT 10.0,
        Account TEXT,
        SalesTax TEXT DEFAULT 'Y',
        PurchTax TEXT DEFAULT 'Y'
    );
    """)

    # -------------------------------------------------------------
    # 11. CRM & Opportunities
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OCRG (
        GroupCode INTEGER PRIMARY KEY,
        GroupName TEXT NOT NULL,
        GroupType TEXT CHECK(GroupType IN ('C', 'S'))
    );
    """)

    cursor.execute("""
    CREATE TABLE OCPR (
        CntctCode INTEGER PRIMARY KEY AUTOINCREMENT,
        CardCode TEXT NOT NULL,
        Name TEXT NOT NULL,
        Position TEXT,
        Address TEXT,
        Tel1 TEXT,
        Cellolar TEXT,
        E_MailL TEXT,
        Active TEXT DEFAULT 'Y'
    );
    """)

    cursor.execute("""
    CREATE TABLE CRD1 (
        Address TEXT NOT NULL,
        CardCode TEXT NOT NULL,
        Street TEXT,
        Block TEXT,
        ZipCode TEXT,
        City TEXT,
        State TEXT,
        Country TEXT DEFAULT 'AU',
        AdresType TEXT CHECK(AdresType IN ('B', 'S')),
        PRIMARY KEY (CardCode, Address, AdresType)
    );
    """)

    cursor.execute("""
    CREATE TABLE OOPR (
        OpprId INTEGER PRIMARY KEY AUTOINCREMENT,
        CardCode TEXT NOT NULL,
        Name TEXT NOT NULL,
        OpenDate TEXT NOT NULL,
        CloseDate TEXT,
        MaxSumLoc REAL DEFAULT 0.0,
        ClosePrcnt REAL DEFAULT 0.0,
        Status TEXT DEFAULT 'O',
        StepId INTEGER DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE OPR1 (
        OpprId INTEGER NOT NULL,
        Line INTEGER NOT NULL,
        StepId INTEGER NOT NULL,
        ClosePrcnt REAL DEFAULT 0.0,
        MaxSumLoc REAL DEFAULT 0.0,
        OpenDate TEXT NOT NULL,
        CloseDate TEXT,
        PRIMARY KEY (OpprId, Line)
    );
    """)

    cursor.execute("""
    CREATE TABLE OCLG (
        ClgCode INTEGER PRIMARY KEY AUTOINCREMENT,
        Action TEXT DEFAULT 'C',
        CntctType INTEGER DEFAULT 1,
        CardCode TEXT NOT NULL,
        DocType TEXT DEFAULT '17',
        DocEntry INTEGER,
        Recontact TEXT NOT NULL,
        Details TEXT,
        Status TEXT DEFAULT 'C'
    );
    """)

    # -------------------------------------------------------------
    # 12. Cost Accounting & Project Management
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE ODIM (
        DimCode INTEGER PRIMARY KEY,
        DimName TEXT NOT NULL,
        DimActive TEXT DEFAULT 'Y',
        DimDesc TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE OPRC (
        PrcCode TEXT PRIMARY KEY,
        PrcName TEXT NOT NULL,
        DimCode INTEGER NOT NULL,
        ValidFrom TEXT NOT NULL,
        ValidTo TEXT NOT NULL,
        Active TEXT DEFAULT 'Y',
        GrpCode TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE OPMG (
        AbsEntry INTEGER PRIMARY KEY AUTOINCREMENT,
        PrjCode TEXT UNIQUE NOT NULL,
        PrjName TEXT NOT NULL,
        CardCode TEXT,
        StartDate TEXT NOT NULL,
        DueDate TEXT NOT NULL,
        Status TEXT DEFAULT 'S',
        PlanCost REAL DEFAULT 0.0,
        ActualCost REAL DEFAULT 0.0
    );
    """)

    cursor.execute("""
    CREATE TABLE PMG1 (
        AbsEntry INTEGER NOT NULL,
        Line INTEGER NOT NULL,
        StageID INTEGER NOT NULL,
        StartDate TEXT NOT NULL,
        EndDate TEXT NOT NULL,
        Task TEXT,
        PlanCost REAL DEFAULT 0.0,
        Status TEXT DEFAULT 'F',
        PRIMARY KEY (AbsEntry, Line)
    );
    """)

    cursor.execute("""
    CREATE TABLE OBGT (
        AbsId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        InitialBgt REAL DEFAULT 0.0,
        FinancYear INTEGER DEFAULT 2026,
        Comments TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE BGT1 (
        AbsId INTEGER NOT NULL,
        AcctCode TEXT NOT NULL,
        DebLTotal REAL DEFAULT 0.0,
        CredLTotal REAL DEFAULT 0.0,
        FinancYear INTEGER DEFAULT 2026,
        PRIMARY KEY (AbsId, AcctCode)
    );
    """)

    # -------------------------------------------------------------
    # 13. Audit & Inventory Valuation History
    # -------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE OINM (
        TransSeq INTEGER PRIMARY KEY AUTOINCREMENT,
        ItemCode TEXT NOT NULL,
        DocDate TEXT NOT NULL,
        TransType INTEGER NOT NULL,
        CreatedBy INTEGER,
        DocLineNum INTEGER DEFAULT 0,
        InQty REAL DEFAULT 0.0,
        OutQty REAL DEFAULT 0.0,
        Price REAL DEFAULT 0.0,
        TransValue REAL DEFAULT 0.0,
        Warehouse TEXT NOT NULL,
        CalcPrice REAL DEFAULT 0.0,
        Balance REAL DEFAULT 0.0
    );
    """)

    cursor.execute("""
    CREATE TABLE ADOC (
        DocEntry INTEGER NOT NULL,
        ObjType TEXT NOT NULL,
        LogInstanc INTEGER NOT NULL,
        UpdateDate TEXT NOT NULL,
        UserSign INTEGER DEFAULT 1,
        Comments TEXT,
        PRIMARY KEY (DocEntry, ObjType, LogInstanc)
    );
    """)

    cursor.execute("""
    CREATE TABLE ADT1 (
        DocEntry INTEGER NOT NULL,
        ObjType TEXT NOT NULL,
        LogInstanc INTEGER NOT NULL,
        LineId INTEGER NOT NULL,
        FieldName TEXT NOT NULL,
        OldValue TEXT,
        NewValue TEXT,
        PRIMARY KEY (DocEntry, ObjType, LogInstanc, LineId)
    );
    """)

    conn.commit()

    # =============================================================
    # POPULATING REALISTIC BUSINESS DATA
    # =============================================================
    print(f" Generating 100+ realistic sample data rows for all 82 tables in '{db_name}'...")
    base_date = datetime(2026, 1, 1)

    # -------------------------------------------------------------
    # Warehouse Setup Parameters
    # -------------------------------------------------------------
    if stock_by_whs:
        # new_b1.db (Multi-Warehouse Costing):
        # ICCChina, ICCSIT, NZNTH, NZSTH, NZSIT, EuropeMarketPlace, EuropeSIT
        primary_whs = "NZNTH"
        whs_origin = "ICCChina"
        whs_transit = "ICCSIT"
        whs_dest = "NZNTH"
        whs_reg1 = "NZSTH"
        whs_reg2 = "EuropeMarketPlace"
        whs_reg3 = "NZSIT"
        whs_reg4 = "EuropeSIT"

        owhs_data = [
            ("ICCChina", "Intercompany Consolidation Center (Ningbo Port Origin)", "Port Zone 1", "88 Industrial Port Rd", "Ningbo", "ZJ", "315800"),
            ("ICCSIT", "Intercompany Sea In-Transit (Ningbo Ocean Carrier Hub)", "Vessel Pacific Mariner", "Berth 7 Ocean Port", "Singapore", "SG", "018989"),
            ("NZNTH", "New Zealand North Island DC (Auckland Main Hub)", "Auckland Logistics Park", "45 Landing Drive", "Mangere", "Auckland", "2022"),
            ("NZSTH", "New Zealand South Island DC (Christchurch Hub)", "Christchurch Airport Hub", "12 Logistics Dr", "Harewood", "Christchurch", "8042"),
            ("NZSIT", "New Zealand Coastal In-Transit (Sea Hub)", "Cook Strait Maritime Carrier", "Port of Tauranga", "Tauranga", "BOP", "3110"),
            ("EuropeMarketPlace", "UK West Yorkshire Facility (Wakefield Hub)", "Wakefield Europort", "Express Way", "Normanton", "West Yorkshire", "WF6 2TZ"),
            ("EuropeSIT", "UK Maritime In-Transit (Felixstowe Sea Hub)", "North Sea Carrier Vessel", "Port of Felixstowe", "Suffolk", "UK", "IP11 3SY"),
        ]
    else:
        # old_b1.db (Single-Level Company Valuation):
        # AU-SYD, AU-MEL, AU-BNE, VGLPER
        primary_whs = "AU-SYD"
        whs_origin = "AU-SYD"
        whs_transit = "AU-SYD"
        whs_dest = "AU-SYD"
        whs_reg1 = "AU-MEL"
        whs_reg2 = "AU-BNE"
        whs_reg3 = "VGLPER"
        whs_reg4 = "AU-SYD"

        owhs_data = [
            ("AU-SYD", "AU Warehouse Sydney Central DC", "Bldg A", "100 Logistics Way", "Sydney", "NSW", "2000"),
            ("AU-MEL", "AU Warehouse Melbourne Logistics Hub", "Bldg 4", "50 Industrial Ave", "Melbourne", "VIC", "3000"),
            ("AU-BNE", "AU Warehouse Brisbane Distribution Center", "Bldg 2", "12 Airport Dr", "Brisbane", "QLD", "4000"),
            ("VGLPER", "VGL Perth Western Logistics Hub", "Unit 8", "88 Freight Rd", "Perth", "WA", "6000"),
        ]

    # Fill remaining warehouses up to 100
    cities = [("Sydney", "NSW", "2000"), ("Melbourne", "VIC", "3000"), ("Brisbane", "QLD", "4000"), ("Perth", "WA", "6000"), ("Auckland", "AKL", "1010"), ("Leeds", "WYK", "LS1")]
    start_extra = len(owhs_data) + 1
    for i in range(start_extra, 101):
        whs_code = f"W{i:03d}"
        city, state, zip_c = random.choice(cities)
        owhs_data.append((whs_code, f"Regional Depot {whs_code} - {city}", f"Unit {i}", f"{i * 12} Commercial Rd", city, state, zip_c))

    cursor.executemany("INSERT INTO OWHS VALUES (?, ?, ?, ?, ?, ?, ?)", owhs_data)

    # -------------------------------------------------------------
    # SEED 1: OACT (100 Chart of Accounts)
    # -------------------------------------------------------------
    oact_structure = [
        ("100010", "Inventory Raw Materials", "A"), ("100020", "Inventory Finished Goods", "A"),
        ("100030", "Accounts Receivable Trade", "A"), ("100040", "Operating Bank Account AUD", "A"),
        ("100050", "In-Transit Inventory Asset", "A"), ("100060", "Prepaid Import Expenses", "A"),
        ("100070", "GST Input Tax Credits (Receivable)", "A"), ("100080", "Foreign Currency Clearing USD", "A"),
        ("200010", "Accounts Payable Trade", "L"), ("200020", "GST Output Tax Collected (Payable)", "L"),
        ("200030", "Accrued Landed Cost Clearing", "L"), ("200040", "Short-Term Bank Facility", "L"),
        ("200050", "Customs Duty Clearing Account", "L"), ("300010", "Share Capital", "Q"),
        ("300020", "Retained Earnings", "Q"), ("400010", "Sales Revenue - Wholesale", "I"),
        ("400020", "Sales Revenue - Retail", "I"), ("400030", "Freight & Delivery Revenue", "I"),
        ("400040", "Landed Cost Recovery", "I"), ("500010", "Cost of Goods Sold - Normal", "E"),
        ("500020", "COGS - Landed Cost Variance", "E"), ("500030", "Inventory Scrap & Write-off", "E"),
        ("510010", "Ocean Freight Expense Account", "E"), ("510020", "Customs Brokerage Clearing", "E"),
        ("510030", "Import Duty Tariff Expense", "E"), ("510040", "Marine Cargo Insurance Expense", "E"),
        ("510050", "Port Wharfage & Stevedoring", "E"), ("510060", "Quarantine & Fumigation Expense", "E"),
        ("510070", "Air Freight Priority Surcharge", "E"), ("510080", "Origin Terminal Handling Fees", "E"),
        ("510090", "Inland Demurrage Expense", "E"), ("510100", "Local & Interstate Haulage", "E"),
        ("600010", "Warehouse Wages & Staff Cost", "E"), ("600020", "Depreciation Expense", "E"),
        ("600030", "Corporate IT & Software", "E")
    ]
    oact_data = []
    for code, name, act_type in oact_structure:
        bal = round(random.uniform(5000, 250000), 2)
        oact_data.append((code, name, bal, "Y" if act_type in ['A', 'L'] else "N", "Y", act_type, 3))
    for i in range(1, 101 - len(oact_data) + 1):
        code = f"699{i:03d}"
        oact_data.append((code, f"Department Cost Center {i:03d}", round(random.uniform(100, 5000), 2), "N", "Y", "E", 3))
    cursor.executemany("INSERT INTO OACT VALUES (?, ?, ?, ?, ?, ?, ?)", oact_data)

    # -------------------------------------------------------------
    # SEED 3: OCRG (10 BP Groups) & OCRD (120 Business Partners)
    # -------------------------------------------------------------
    ocrg_data = [
        (100, "Enterprise Customers", "C"), (101, "Small & Medium Retailers", "C"),
        (102, "Key Account Distributors", "C"), (103, "Government & Education", "C"),
        (104, "Online Direct Customers", "C"), (200, "Hardware Raw Material Vendors", "S"),
        (201, "Component & Electronics Suppliers", "S"), (202, "Logistics & Freight Forwarders", "S"),
        (203, "IT Services & Subcontractors", "S"), (204, "Packaging Suppliers", "S")
    ]
    cursor.executemany("INSERT INTO OCRG VALUES (?, ?, ?)", ocrg_data)

    first_names = ["Apex", "BlueSky", "Summit", "Nexus", "Pinnacle", "Vanguard", "Horizon", "Crest", "Harbor", "Metro", "Prime", "Quantum", "Solar", "Terra", "Nova", "Beacon", "Atlas", "Eclipse", "Oasis", "Zephyr"]
    mid_names = ["Retail", "Trading", "Logistics", "Enterprises", "Solutions", "Supplies", "Tech", "Holdings", "Distribution", "Wholesale", "Commerce", "Ventures"]
    suffixes = ["Pty Ltd", "Ltd", "Inc", "Group", "Corp"]

    ocrd_data = []
    customers = []
    for i in range(1, 81):
        code = f"C{10000 + i}"
        name = f"{random.choice(first_names)} {random.choice(mid_names)} {random.choice(suffixes)}"
        phone = f"0{random.randint(2,8)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
        bal = round(random.uniform(0.0, 20000.0), 2)
        customers.append((code, name))
        ocrd_data.append((code, name, "C", random.choice([100, 101, 102, 103, 104]), phone, "AUD", bal, "100030"))

    vendors = []
    for i in range(1, 41):
        code = f"V{20000 + i}"
        name = f"Global {random.choice(first_names)} {random.choice(mid_names)} {random.choice(suffixes)}"
        phone = f"0{random.randint(2,8)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
        bal = round(-random.uniform(0.0, 30000.0), 2)
        vendors.append((code, name))
        ocrd_data.append((code, name, "S", random.choice([200, 201, 202, 203, 204]), phone, "AUD", bal, "200010"))
    cursor.executemany("INSERT INTO OCRD VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ocrd_data)

    # -------------------------------------------------------------
    # SEED 4: OCPR & CRD1
    # -------------------------------------------------------------
    c_first = ["David", "Sarah", "Michael", "Emma", "James", "Emily", "Daniel", "Jessica", "Matthew", "Olivia", "Andrew", "Sophia", "Christopher", "Isabella", "Joshua", "Mia"]
    c_last = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin"]
    positions = ["Procurement Manager", "Operations Director", "Finance Controller", "Warehouse Supervisor", "Account Executive", "Purchasing Officer", "Managing Director"]
    ocpr_data = []
    crd1_data = []
    for idx, (c_code, c_name) in enumerate(customers + vendors, 1):
        f = random.choice(c_first)
        l = random.choice(c_last)
        contact_name = f"{f} {l}"
        email = f"{f.lower()}.{l.lower()}@{c_name.split()[0].lower()}corp.com.au"
        phone = f"04{random.randint(10,99)} {random.randint(100,999)} {random.randint(100,999)}"
        ocpr_data.append((c_code, contact_name, random.choice(positions), "Level 5, HQ Tower", phone, phone, email, "Y"))
        crd1_data.append(("Bill-To HQ", c_code, f"{random.randint(10, 200)} Queen Street", "Block A", "2000", "Sydney", "NSW", "AU", "B"))
        crd1_data.append(("Ship-To Whs", c_code, f"{random.randint(5, 80)} Logistics Blvd", "Sector 4", "3000", "Melbourne", "VIC", "AU", "S"))
    cursor.executemany("INSERT INTO OCPR (CardCode, Name, Position, Address, Tel1, Cellolar, E_MailL, Active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ocpr_data)
    cursor.executemany("INSERT INTO CRD1 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", crd1_data)

    # -------------------------------------------------------------
    # SEED 5: OITM (100 Items) & OITW (Inventory Records)
    # -------------------------------------------------------------
    product_templates = [
        ("Laser Barcode Scanner Model {}", 1, 45.0, 120.0, 1.45),
        ("Thermal Receipt Printer {}mm", 1, 80.0, 210.0, 1.40),
        ("Heavy Duty Cash Drawer Size {}", 1, 50.0, 110.0, 1.35),
        ("Touchscreen POS Terminal {}in", 1, 350.0, 850.0, 1.30),
        ("Magnetic Stripe Card Reader v{}", 1, 25.0, 60.0, 1.50),
        ("Handheld Stock PDA Scanner v{}", 1, 280.0, 620.0, 1.35),
        ("Receipt Paper Roll Box ({} Rolls)", 2, 18.0, 45.0, 1.55),
        ("Direct Thermal Barcode Labels ({} Roll)", 2, 12.0, 35.0, 1.60),
        ("Bubble Cushion Wrap Roll {}m", 2, 15.0, 40.0, 1.50),
        ("Heavy Duty Shipping Box {}cm", 2, 2.5, 8.5, 1.70),
    ]

    oitm_data = []
    item_lookup = {}
    oitw_data = []

    for i in range(1, 101):
        item_code = f"ITM-{i:03d}"
        tpl, grp, min_c, max_c, margin = product_templates[(i - 1) % len(product_templates)]
        v = (i // len(product_templates)) + 1
        name = tpl.format(v * 10 if "{}" in tpl else v)
        cost = round(random.uniform(min_c, max_c), 2)
        price = round(cost * margin, 2)
        on_hand_tot = float(random.randint(50, 600))
        comm_tot = float(random.randint(0, int(on_hand_tot * 0.35)))
        order_tot = float(random.randint(0, 120))

        oitm_data.append((item_code, name, grp, on_hand_tot, comm_tot, order_tot, cost, primary_whs))
        item_lookup[item_code] = {"name": name, "cost": cost, "price": price}

        avg_p = cost if stock_by_whs else 0.0
        if stock_by_whs:
            oitw_data.append((item_code, whs_dest, round(on_hand_tot * 0.6, 1), round(comm_tot * 0.6, 1), round(order_tot * 0.6, 1), avg_p, 20.0, 500.0))
            oitw_data.append((item_code, whs_reg1, round(on_hand_tot * 0.25, 1), round(comm_tot * 0.25, 1), round(order_tot * 0.25, 1), avg_p, 10.0, 300.0))
            oitw_data.append((item_code, whs_reg2, round(on_hand_tot * 0.15, 1), round(comm_tot * 0.15, 1), round(order_tot * 0.15, 1), avg_p, 5.0, 150.0))
        else:
            oitw_data.append((item_code, "AU-SYD", round(on_hand_tot * 0.4, 1), round(comm_tot * 0.4, 1), round(order_tot * 0.4, 1), 0.0, 20.0, 500.0))
            oitw_data.append((item_code, "AU-MEL", round(on_hand_tot * 0.3, 1), round(comm_tot * 0.3, 1), round(order_tot * 0.3, 1), 0.0, 10.0, 300.0))
            oitw_data.append((item_code, "AU-BNE", round(on_hand_tot * 0.2, 1), round(comm_tot * 0.2, 1), round(order_tot * 0.2, 1), 0.0, 5.0, 150.0))
            oitw_data.append((item_code, "VGLPER", round(on_hand_tot * 0.1, 1), round(comm_tot * 0.1, 1), round(order_tot * 0.1, 1), 0.0, 5.0, 100.0))

    # Category 3 - Imported Hardware & Automation
    imported_products = [
        ("ITM-IMP-001", "Industrial AI Smart Camera Vision System", 3, 450.0, 1.45),
        ("ITM-IMP-002", "Ultra-Rugged 2D Long-Range Barcode Imager", 3, 320.0, 1.40),
        ("ITM-IMP-003", "Enterprise RFID Automated Portal Reader", 3, 780.0, 1.35),
        ("ITM-IMP-004", "High-Speed Industrial Thermal Print Engine", 3, 520.0, 1.35),
        ("ITM-IMP-005", "Mobile Computing Handheld Terminal 5G", 3, 610.0, 1.30),
        ("ITM-IMP-006", "Automated Guided Vehicle (AGV) LiDAR Sensor", 3, 890.0, 1.40),
        ("ITM-IMP-007", "Omnidirectional Fixed Mount Laser Scanner", 3, 380.0, 1.45),
        ("ITM-IMP-008", "Heavy-Duty Wireless Barcode Scanner Base", 3, 210.0, 1.50),
        ("ITM-IMP-009", "Industrial Touch Panel PC 21.5in IP65", 3, 950.0, 1.30),
        ("ITM-IMP-010", "Digital Freight Dimensioner & Weigh System", 3, 1200.0, 1.35),
    ]

    for item_code, name, grp, base_c, margin in imported_products:
        price = round(base_c * margin, 2)
        on_hand_tot = 200.0
        comm_tot = 25.0
        order_tot = 50.0

        oitm_data.append((item_code, name, grp, on_hand_tot, comm_tot, order_tot, base_c, primary_whs))
        item_lookup[item_code] = {"name": name, "cost": base_c, "price": price}

        avg_imp_p = base_c if stock_by_whs else 0.0
        if stock_by_whs:
            oitw_data.append((item_code, whs_dest, 100.0, 15.0, 25.0, avg_imp_p, 20.0, 500.0))
            oitw_data.append((item_code, whs_reg1, 60.0, 7.0, 15.0, avg_imp_p, 10.0, 300.0))
            oitw_data.append((item_code, whs_reg2, 40.0, 3.0, 10.0, avg_imp_p, 5.0, 150.0))
        else:
            oitw_data.append((item_code, "AU-SYD", 80.0, 10.0, 20.0, 0.0, 20.0, 500.0))
            oitw_data.append((item_code, "AU-MEL", 50.0, 8.0, 15.0, 0.0, 10.0, 300.0))
            oitw_data.append((item_code, "AU-BNE", 40.0, 5.0, 10.0, 0.0, 5.0, 150.0))
            oitw_data.append((item_code, "VGLPER", 30.0, 2.0, 5.0, 0.0, 5.0, 100.0))

    # Category 4 - Robotics & Intercompany Automation
    intercompany_products = [
        ("ITM-IC-001", "Industrial Multi-Axis Robotics Controller", 4, 400.0, 1.45),
        ("ITM-IC-002", "5G Industrial Telematics Edge Gateway", 4, 280.0, 1.40),
        ("ITM-IC-003", "Automated Optical Inspection LiDAR Sensor", 4, 650.0, 1.35),
        ("ITM-IC-004", "High-Torque Servo Drive Control Unit", 4, 520.0, 1.35),
        ("ITM-IC-005", "Heavy-Duty Wireless AGV Navigation Hub", 4, 850.0, 1.30),
    ]

    for item_code, name, grp, base_c, margin in intercompany_products:
        price = round(base_c * margin, 2)
        on_hand_tot = 440.0 if stock_by_whs else 350.0
        comm_tot = 20.0
        order_tot = 40.0

        oitm_data.append((item_code, name, grp, on_hand_tot, comm_tot, order_tot, base_c, primary_whs))
        item_lookup[item_code] = {"name": name, "cost": base_c, "price": price}

        avg_ic_p = base_c if stock_by_whs else 0.0
        if stock_by_whs:
            # new_b1.db (Multi-Warehouse Costing): ICCChina, ICCSIT, NZNTH, NZSTH, NZSIT, EuropeMarketPlace, EuropeSIT
            oitw_data.append((item_code, "ICCChina", 100.0, 10.0, 20.0, avg_ic_p, 20.0, 500.0))
            oitw_data.append((item_code, "ICCSIT", 50.0, 0.0, 0.0, avg_ic_p, 0.0, 500.0))
            oitw_data.append((item_code, "NZNTH", 150.0, 10.0, 20.0, avg_ic_p, 30.0, 500.0))
            oitw_data.append((item_code, "NZSTH", 50.0, 5.0, 10.0, avg_ic_p, 10.0, 300.0))
            oitw_data.append((item_code, "NZSIT", 30.0, 0.0, 0.0, avg_ic_p, 0.0, 200.0))
            oitw_data.append((item_code, "EuropeMarketPlace", 40.0, 5.0, 10.0, avg_ic_p, 10.0, 200.0))
            oitw_data.append((item_code, "EuropeSIT", 20.0, 0.0, 0.0, avg_ic_p, 0.0, 100.0))
        else:
            # old_b1.db (Single-Level Company Valuation): AU-SYD, AU-MEL, AU-BNE, VGLPER
            oitw_data.append((item_code, "AU-SYD", 150.0, 10.0, 20.0, 0.0, 30.0, 500.0))
            oitw_data.append((item_code, "AU-MEL", 100.0, 5.0, 10.0, 0.0, 20.0, 300.0))
            oitw_data.append((item_code, "AU-BNE", 50.0, 3.0, 5.0, 0.0, 10.0, 200.0))
            oitw_data.append((item_code, "VGLPER", 50.0, 2.0, 5.0, 0.0, 5.0, 100.0))

    cursor.executemany("INSERT INTO OITM VALUES (?, ?, ?, ?, ?, ?, ?, ?)", oitm_data)
    cursor.executemany("INSERT INTO OITW VALUES (?, ?, ?, ?, ?, ?, ?, ?)", oitw_data)

    all_items = list(item_lookup.keys())
    imported_item_codes = [x[0] for x in imported_products]
    intercompany_item_codes = [x[0] for x in intercompany_products]

    # -------------------------------------------------------------
    # SEED 6: Pricing Engine (OPLN, ITM1, OSPP, SPP1, OSTC)
    # -------------------------------------------------------------
    opln_data = [
        (1, "Base Purchase Cost Price List", 1, 1.0, "AUD", "Y"),
        (2, "Standard Wholesale Price List", 1, 1.30, "AUD", "Y"),
        (3, "Premium Retail Price List", 1, 1.65, "AUD", "Y"),
        (4, "VIP Key Account Price List", 1, 1.20, "AUD", "Y"),
        (5, "Distributor Clearance Price List", 1, 1.10, "AUD", "Y")
    ]
    cursor.executemany("INSERT INTO OPLN VALUES (?, ?, ?, ?, ?, ?)", opln_data)

    itm1_data = []
    for itm in all_items:
        base_cost = item_lookup[itm]["cost"]
        for list_num, l_name, b_list, factor, curr, valid in opln_data:
            itm1_data.append((itm, list_num, round(base_cost * factor, 2), curr, factor))
    cursor.executemany("INSERT INTO ITM1 VALUES (?, ?, ?, ?, ?)", itm1_data)

    ospp_data = []
    spp1_data = []
    for c_code, c_name in customers[:50]:
        sample_itms = random.sample(all_items, 2)
        for itm in sample_itms:
            spec_price = round(item_lookup[itm]["price"] * 0.85, 2)
            ospp_data.append((c_code, itm, spec_price, "AUD", 15.0, "2026-01-01", "2026-12-31"))
            spp1_data.append((c_code, itm, 0, 10.0, round(spec_price * 0.95, 2), 5.0))
            spp1_data.append((c_code, itm, 1, 50.0, round(spec_price * 0.90, 2), 10.0))
    cursor.executemany("INSERT INTO OSPP VALUES (?, ?, ?, ?, ?, ?, ?)", ospp_data)
    cursor.executemany("INSERT INTO SPP1 VALUES (?, ?, ?, ?, ?, ?)", spp1_data)

    ostc_data = [
        ("GST_10", "Standard 10% Australian GST", 10.0, "200020", "Y", "Y"),
        ("GST_FREE", "GST Free Supplies & Exports", 0.0, "200020", "Y", "Y"),
        ("INP_TAX", "Input Taxed Financial Supplies", 0.0, "200020", "N", "Y"),
        ("DUTY_5", "Import Customs Duty 5%", 5.0, "510040", "N", "Y"),
        ("LUX_TAX", "Luxury Equipment Surcharge 15%", 15.0, "200020", "Y", "N")
    ]
    cursor.executemany("INSERT INTO OSTC VALUES (?, ?, ?, ?, ?, ?)", ostc_data)

    # -------------------------------------------------------------
    # SEED 7: Banking (OCTG, ODSC)
    # -------------------------------------------------------------
    octg_data = [
        (1, "Net 30 Days", 0, 30, 0, 0.0, 0),
        (2, "Net 60 Days", 0, 60, 0, 0.0, 0),
        (3, "Cash On Delivery (COD)", 0, 0, 0, 0.0, 0),
        (4, "2% 10 Net 30", 0, 30, 0, 2.0, 10),
        (5, "End of Month (EOM)", 1, 0, 1, 0.0, 0),
        (6, "Prepayment / Advance", 0, 0, 0, 5.0, 0)
    ]
    cursor.executemany("INSERT INTO OCTG VALUES (?, ?, ?, ?, ?, ?, ?)", octg_data)

    odsc_data = [
        ("CBA", "Commonwealth Bank of Australia", "100-293848", "Sydney Central", "AU"),
        ("ANZ", "Australia and New Zealand Banking Group", "012-948271", "Melbourne Hub", "AU"),
        ("WBC", "Westpac Banking Corporation", "032-118273", "Sydney Financial", "AU"),
        ("NAB", "National Australia Bank", "083-772819", "Brisbane North", "AU"),
        ("MQG", "Macquarie Bank Commercial", "182-990182", "Barangaroo Wharf", "AU")
    ]
    cursor.executemany("INSERT INTO ODSC VALUES (?, ?, ?, ?, ?)", odsc_data)

    # -------------------------------------------------------------
    # SEED 8: Cost Accounting (ODIM, OPRC, OPMG, PMG1, OBGT, BGT1)
    # -------------------------------------------------------------
    odim_data = [
        (1, "Operational Departments", "Y", "Corporate organizational divisions"),
        (2, "Geographical Territories", "Y", "Sales and distribution regional zones"),
        (3, "Product Lines", "Y", "Hardware vs Consumables vs Enterprise Services"),
        (4, "Customer Channels", "Y", "Retail, Wholesale, Online Direct"),
        (5, "Strategic Programs", "Y", "Sustainability & Digital Transformation")
    ]
    cursor.executemany("INSERT INTO ODIM VALUES (?, ?, ?, ?)", odim_data)

    oprc_data = [
        ("CC-HQ-OPS", "Headquarters Operations", 1, "2026-01-01", "2026-12-31", "Y", "HQ"),
        ("CC-MKT-ALL", "National Marketing & PR", 1, "2026-01-01", "2026-12-31", "Y", "MKT"),
        ("CC-RND-TECH", "R&D Hardware Engineering", 1, "2026-01-01", "2026-12-31", "Y", "ENG"),
        ("CC-LOG-PRI", f"{primary_whs} Main Logistics Hub", 2, "2026-01-01", "2026-12-31", "Y", "LOG"),
        ("CC-LOG-REG", f"{whs_reg1} Regional Logistics Hub", 2, "2026-01-01", "2026-12-31", "Y", "LOG"),
        ("CC-SALES-PRI", "Primary Territory Enterprise Sales", 2, "2026-01-01", "2026-12-31", "Y", "SLS"),
        ("CC-SALES-REG", "Regional Territory Enterprise Sales", 2, "2026-01-01", "2026-12-31", "Y", "SLS"),
        ("CC-SUP-TECH", "Client Technical Support", 1, "2026-01-01", "2026-12-31", "Y", "CS")
    ]
    cursor.executemany("INSERT INTO OPRC VALUES (?, ?, ?, ?, ?, ?, ?)", oprc_data)

    for i in range(1, 101):
        prj_code = f"PRJ-{202600 + i}"
        prj_name = f"Enterprise POS Rollout Phase {i}"
        c_code, c_name = random.choice(customers)
        start_d = base_date + timedelta(days=random.randint(0, 30))
        due_d = start_d + timedelta(days=random.randint(60, 180))
        plan_cost = round(random.uniform(15000.0, 95000.0), 2)
        act_cost = round(plan_cost * random.uniform(0.75, 1.10), 2)
        cursor.execute("INSERT INTO OPMG (PrjCode, PrjName, CardCode, StartDate, DueDate, Status, PlanCost, ActualCost) VALUES (?, ?, ?, ?, ?, 'S', ?, ?)",
                       (prj_code, prj_name, c_code, start_d.strftime("%Y-%m-%d"), due_d.strftime("%Y-%m-%d"), plan_cost, act_cost))
        p_entry = cursor.lastrowid
        stages = ["Site Survey & Procurement", "Hardware Installation", "Software Integration", "User Acceptance & Handover"]
        for s_num, stg in enumerate(stages):
            s_start = start_d + timedelta(days=s_num * 20)
            s_end = s_start + timedelta(days=18)
            cursor.execute("INSERT INTO PMG1 VALUES (?, ?, ?, ?, ?, ?, ?, 'F')",
                           (p_entry, s_num, s_num + 1, s_start.strftime("%Y-%m-%d"), s_end.strftime("%Y-%m-%d"), stg, round(act_cost / 4, 2)))

    cursor.execute("INSERT INTO OBGT (Name, InitialBgt, FinancYear, Comments) VALUES ('FY2026 Annual Master Budget', 5000000.0, 2026, 'Approved corporate budget')")
    bgt_id = cursor.lastrowid
    bgt1_data = []
    for acct_code, acct_name, _, _, _, act_type, _ in oact_data:
        if act_type in ['E', 'I']:
            deb_amt = round(random.uniform(20000.0, 150000.0), 2) if act_type == 'E' else 0.0
            cred_amt = round(random.uniform(50000.0, 300000.0), 2) if act_type == 'I' else 0.0
            bgt1_data.append((bgt_id, acct_code, deb_amt, cred_amt, 2026))
    cursor.executemany("INSERT INTO BGT1 VALUES (?, ?, ?, ?, ?)", bgt1_data)

    # -------------------------------------------------------------
    # SEED 9: Pre-Sales & Purchasing (OPRQ, PRQ1, OPQT, PQT1, OQUT, QUT1)
    # -------------------------------------------------------------
    for i in range(1, 101):
        doc_num = 4500 + i
        doc_date = base_date + timedelta(days=random.randint(0, 40))
        due_date = doc_date + timedelta(days=random.randint(5, 20))
        cursor.execute("INSERT INTO OPRQ (DocNum, DocDate, DocDueDate, ReqName, ReqType, DocStatus, DocTotal, Comments) VALUES (?, ?, ?, 'Operations Dept', 1, 'C', 0.0, 'Internal PR for stock replenishment')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d")))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 3))):
            qty = random.randint(10, 40)
            cost = item_lookup[itm]["cost"]
            l_tot = round(qty * cost, 2)
            tot += l_tot
            cursor.execute("INSERT INTO PRQ1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, cost, l_tot, primary_whs))
        cursor.execute("UPDATE OPRQ SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    for i in range(1, 101):
        doc_num = 4700 + i
        doc_date = base_date + timedelta(days=random.randint(0, 45))
        due_date = doc_date + timedelta(days=random.randint(5, 20))
        v_code, v_name = random.choice(vendors)
        cursor.execute("INSERT INTO OPQT (DocNum, DocDate, DocDueDate, CardCode, CardName, DocStatus, DocTotal, Comments) VALUES (?, ?, ?, ?, ?, 'C', 0.0, 'Supplier price quote request')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d"), v_code, v_name))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 3))):
            qty = random.randint(15, 60)
            cost = round(item_lookup[itm]["cost"] * 0.98, 2)
            l_tot = round(qty * cost, 2)
            tot += l_tot
            cursor.execute("INSERT INTO PQT1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, cost, l_tot, primary_whs))
        cursor.execute("UPDATE OPQT SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    for i in range(1, 101):
        doc_num = 800 + i
        doc_date = base_date + timedelta(days=random.randint(0, 50))
        due_date = doc_date + timedelta(days=random.randint(7, 30))
        c_code, c_name = random.choice(customers)
        cursor.execute("INSERT INTO OQUT (DocNum, DocDate, DocDueDate, CardCode, CardName, DocStatus, DocTotal, Comments) VALUES (?, ?, ?, ?, ?, 'C', 0.0, 'Sales Quotation to prospect')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d"), c_code, c_name))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 4))):
            qty = random.randint(2, 15)
            price = item_lookup[itm]["price"]
            l_tot = round(qty * price, 2)
            tot += l_tot
            cursor.execute("INSERT INTO QUT1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, price, l_tot, primary_whs))
        cursor.execute("UPDATE OQUT SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    # -------------------------------------------------------------
    # SEED 10: OPOR & POR1 (100 Purchase Orders)
    # -------------------------------------------------------------
    for i in range(1, 101):
        doc_num = 5000 + i
        doc_date = base_date + timedelta(days=random.randint(0, 50))
        due_date = doc_date + timedelta(days=random.randint(5, 25))
        v_code, v_name = random.choice(vendors)
        doc_status = "C" if random.random() < 0.65 else "O"

        cursor.execute("INSERT INTO OPOR (DocNum, DocDate, DocDueDate, CardCode, CardName, DocStatus, DocTotal, DocCur, DocRate, DocTotalFC, Comments) VALUES (?, ?, ?, ?, ?, ?, 0.0, 'AUD', 1.0, 0.0, ?)",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d"), v_code, v_name, doc_status, "PO Batch replenishment"))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 4))):
            qty = random.randint(15, 80)
            cost = item_lookup[itm]["cost"]
            l_tot = round(qty * cost, 2)
            tot += l_tot
            cursor.execute("INSERT INTO POR1 (DocEntry, LineNum, ItemCode, Dscription, Quantity, Price, LineTotal, PriceFC, TotalFrgn, OpenQty, WhsCode, LineStatus) VALUES (?, ?, ?, ?, ?, ?, ?, 0.0, 0.0, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, cost, l_tot, qty if doc_status == 'O' else 0, primary_whs, doc_status))
        cursor.execute("UPDATE OPOR SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    # -------------------------------------------------------------
    # SEED 11: OPDN & PDN1 (Goods Receipt POs with Multi-Warehouse Deliveries)
    # -------------------------------------------------------------
    target_whs_pool = [whs_dest, whs_reg1, whs_reg2] if stock_by_whs else ["AU-SYD", "AU-MEL", "AU-BNE", "VGLPER"]
    for i in range(1, 101):
        doc_num = 6000 + i
        doc_date = base_date + timedelta(days=random.randint(10, 60))
        v_code, v_name = random.choice(vendors)
        whs_dest_item = target_whs_pool[i % len(target_whs_pool)]
        cursor.execute("INSERT INTO OPDN (DocNum, DocDate, CardCode, CardName, DocStatus, DocTotal, DocCur, DocRate, DocTotalFC, BaseEntry, Comments) VALUES (?, ?, ?, ?, 'C', 0.0, 'AUD', 1.0, 0.0, ?, ?)",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), v_code, v_name, i, f"GRPO Delivery Received - Destination Whs {whs_dest_item}"))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 3))):
            qty = random.randint(10, 50)
            cost = item_lookup[itm]["cost"]
            l_tot = round(qty * cost, 2)
            tot += l_tot
            cursor.execute("INSERT INTO PDN1 (DocEntry, LineNum, ItemCode, Dscription, Quantity, Price, LineTotal, PriceFC, TotalFrgn, WhsCode, BaseEntry, BaseLine) VALUES (?, ?, ?, ?, ?, ?, ?, 0.0, 0.0, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, cost, l_tot, whs_dest_item, i, l_num))
        cursor.execute("UPDATE OPDN SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    # Foreign Import GRPOs for Category 3 items
    foreign_vendor_code, foreign_vendor_name = "V-1005", "Global Precision Automation Corp"
    for idx, imp_code in enumerate(imported_item_codes, 1):
        whs_splits = [(whs_dest, 100.0), (whs_reg1, 60.0), (whs_reg2, 40.0)] if stock_by_whs else [("AU-SYD", 80.0), ("AU-MEL", 50.0), ("AU-BNE", 40.0), ("VGLPER", 30.0)]
        for w_idx, (whs_code_imp, qty) in enumerate(whs_splits, 1):
            doc_num = 6100 + (idx - 1) * len(whs_splits) + w_idx
            doc_date = (base_date + timedelta(days=10 + idx * 3)).strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO OPDN (DocNum, DocDate, CardCode, CardName, DocStatus, DocTotal, DocCur, DocRate, DocTotalFC, BaseEntry, Comments) VALUES (?, ?, ?, ?, 'C', 0.0, 'AUD', 1.0, 0.0, NULL, ?)",
                           (doc_num, doc_date, foreign_vendor_code, foreign_vendor_name, f"Import Shipment GRPO for {imp_code} (Whs {whs_code_imp})"))
            grpo_entry = cursor.lastrowid
            base_c = item_lookup[imp_code]["cost"]
            line_tot = round(qty * base_c, 2)
            cursor.execute("INSERT INTO PDN1 (DocEntry, LineNum, ItemCode, Dscription, Quantity, Price, LineTotal, PriceFC, TotalFrgn, WhsCode, BaseEntry, BaseLine) VALUES (?, 0, ?, ?, ?, ?, ?, 0.0, 0.0, ?, NULL, 0)",
                           (grpo_entry, imp_code, item_lookup[imp_code]["name"], qty, base_c, line_tot, whs_code_imp))
            cursor.execute("UPDATE OPDN SET DocTotal = ? WHERE DocEntry = ?", (line_tot, grpo_entry))

    # -------------------------------------------------------------
    # SEED 12 & 13: OPCH, PCH1, ORPC, RPC1
    # -------------------------------------------------------------
    for i in range(1, 101):
        doc_num = 7000 + i
        doc_date = base_date + timedelta(days=random.randint(15, 60))
        due_date = doc_date + timedelta(days=30)
        v_code, v_name = random.choice(vendors)
        cursor.execute("INSERT INTO OPCH (DocNum, DocDate, DocDueDate, CardCode, CardName, DocStatus, DocTotal, Comments) VALUES (?, ?, ?, ?, ?, 'C', 0.0, 'Standard AP Invoice')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d"), v_code, v_name))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 3))):
            qty = random.randint(10, 50)
            cost = item_lookup[itm]["cost"]
            l_tot = round(qty * cost, 2)
            tot += l_tot
            cursor.execute("INSERT INTO PCH1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, cost, l_tot, primary_whs))
        cursor.execute("UPDATE OPCH SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    for i in range(1, 101):
        doc_num = 7500 + i
        doc_date = base_date + timedelta(days=random.randint(20, 60))
        v_code, v_name = random.choice(vendors)
        cursor.execute("INSERT INTO ORPC (DocNum, DocDate, CardCode, CardName, DocTotal, Comments) VALUES (?, ?, ?, ?, 0.0, 'Supplier return/credit')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), v_code, v_name))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 2))):
            qty = random.randint(1, 5)
            cost = item_lookup[itm]["cost"]
            l_tot = round(qty * cost, 2)
            tot += l_tot
            cursor.execute("INSERT INTO RPC1 VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, cost, l_tot))
        cursor.execute("UPDATE ORPC SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    # -------------------------------------------------------------
    # SEED 14 to 18: Sales Cycle (ORDR, ODLN, ORDN, OINV, ORIN)
    # -------------------------------------------------------------
    for i in range(1, 101):
        doc_num = 1000 + i
        doc_date = base_date + timedelta(days=random.randint(0, 55))
        due_date = doc_date + timedelta(days=random.randint(3, 14))
        c_code, c_name = random.choice(customers)
        doc_status = "C" if random.random() < 0.70 else "O"

        cursor.execute("INSERT INTO ORDR (DocNum, DocDate, DocDueDate, CardCode, CardName, DocStatus, DocTotal, Comments) VALUES (?, ?, ?, ?, ?, ?, 0.0, 'Customer sales order')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d"), c_code, c_name, doc_status))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 4))):
            qty = random.randint(2, 20)
            price = item_lookup[itm]["price"]
            l_tot = round(qty * price, 2)
            tot += l_tot
            cursor.execute("INSERT INTO RDR1 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, price, l_tot, qty if doc_status == 'O' else 0, primary_whs, doc_status))
        cursor.execute("UPDATE ORDR SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    for i in range(1, 101):
        doc_num = 2000 + i
        doc_date = base_date + timedelta(days=random.randint(5, 60))
        c_code, c_name = random.choice(customers)
        cursor.execute("INSERT INTO ODLN (DocNum, DocDate, CardCode, CardName, DocStatus, DocTotal, BaseEntry, Comments) VALUES (?, ?, ?, ?, 'C', 0.0, ?, 'Goods dispatched to client')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), c_code, c_name, i))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 3))):
            qty = random.randint(2, 15)
            price = item_lookup[itm]["price"]
            l_tot = round(qty * price, 2)
            tot += l_tot
            cursor.execute("INSERT INTO DLN1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, price, l_tot, primary_whs))
        cursor.execute("UPDATE ODLN SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    for i in range(1, 101):
        doc_num = 2500 + i
        doc_date = base_date + timedelta(days=random.randint(10, 60))
        c_code, c_name = random.choice(customers)
        cursor.execute("INSERT INTO ORDN (DocNum, DocDate, CardCode, CardName, DocStatus, DocTotal, BaseEntry, Comments) VALUES (?, ?, ?, ?, 'C', 0.0, ?, 'Customer return goods receipt')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), c_code, c_name, i))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 2))):
            qty = random.randint(1, 3)
            price = item_lookup[itm]["price"]
            l_tot = round(qty * price, 2)
            tot += l_tot
            cursor.execute("INSERT INTO RDN1 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, price, l_tot, primary_whs, i, l_num))
        cursor.execute("UPDATE ORDN SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    for i in range(1, 101):
        doc_num = 3000 + i
        doc_date = base_date + timedelta(days=random.randint(10, 60))
        due_date = doc_date + timedelta(days=14)
        c_code, c_name = random.choice(customers)
        cursor.execute("INSERT INTO OINV (DocNum, DocDate, DocDueDate, CardCode, CardName, DocStatus, DocTotal, Comments) VALUES (?, ?, ?, ?, ?, 'C', 0.0, 'AR Customer Tax Invoice')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d"), c_code, c_name))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 4))):
            qty = random.randint(2, 15)
            price = item_lookup[itm]["price"]
            l_tot = round(qty * price, 2)
            tot += l_tot
            cursor.execute("INSERT INTO INV1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, price, l_tot, primary_whs))
        cursor.execute("UPDATE OINV SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    for i in range(1, 101):
        doc_num = 3500 + i
        doc_date = base_date + timedelta(days=random.randint(15, 60))
        c_code, c_name = random.choice(customers)
        cursor.execute("INSERT INTO ORIN (DocNum, DocDate, CardCode, CardName, DocTotal, Comments) VALUES (?, ?, ?, ?, 0.0, 'Customer return adjustment')",
                       (doc_num, doc_date.strftime("%Y-%m-%d"), c_code, c_name))
        entry = cursor.lastrowid
        tot = 0.0
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 2))):
            qty = random.randint(1, 4)
            price = item_lookup[itm]["price"]
            l_tot = round(qty * price, 2)
            tot += l_tot
            cursor.execute("INSERT INTO RIN1 VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (entry, l_num, itm, item_lookup[itm]["name"], qty, price, l_tot))
        cursor.execute("UPDATE ORIN SET DocTotal = ? WHERE DocEntry = ?", (round(tot, 2), entry))

    # -------------------------------------------------------------
    # SEED 19: Banking (ORCT, RCT2, OVPM, VPM2)
    # -------------------------------------------------------------
    for i in range(1, 101):
        pay_date = base_date + timedelta(days=random.randint(15, 65))
        c_code, c_name = random.choice(customers)
        doc_total = round(random.uniform(500.0, 15000.0), 2)
        cursor.execute("INSERT INTO ORCT (DocNum, DocDate, DocDueDate, CardCode, CardName, DocType, TrsfrSum, TrsfrRef, DocTotal, Comments, PrjCode) VALUES (?, ?, ?, ?, ?, 'C', ?, 'EFT-PAY-REC', ?, 'Customer payment settlement', ?)",
                       (90000 + i, pay_date.strftime("%Y-%m-%d"), pay_date.strftime("%Y-%m-%d"), c_code, c_name, doc_total, doc_total, f"PRJ-{202600 + (i % 100) + 1}"))
        rct_entry = cursor.lastrowid
        cursor.execute("INSERT INTO RCT2 VALUES (?, 0, ?, ?, 13, ?, 0.0, 0.0)", (rct_entry, 9000 + i, i, doc_total))

    for i in range(1, 101):
        pay_date = base_date + timedelta(days=random.randint(20, 65))
        v_code, v_name = random.choice(vendors)
        doc_total = round(random.uniform(800.0, 25000.0), 2)
        cursor.execute("INSERT INTO OVPM (DocNum, DocDate, DocDueDate, CardCode, CardName, DocType, TrsfrSum, TrsfrRef, DocTotal, Comments, PrjCode) VALUES (?, ?, ?, ?, ?, 'S', ?, 'EFT-DISBURSE', ?, 'Vendor invoice disbursement', ?)",
                       (80000 + i, pay_date.strftime("%Y-%m-%d"), pay_date.strftime("%Y-%m-%d"), v_code, v_name, doc_total, doc_total, f"PRJ-{202600 + (i % 100) + 1}"))
        vpm_entry = cursor.lastrowid
        cursor.execute("INSERT INTO VPM2 VALUES (?, 0, ?, ?, 18, ?, 0.0, 0.0)", (vpm_entry, 8000 + i, i, doc_total))

    # -------------------------------------------------------------
    # SEED 20: Production & Manufacturing
    # -------------------------------------------------------------
    bom_parents = all_items[:25]
    raw_components = all_items[25:]
    for parent in bom_parents:
        cursor.execute("INSERT INTO OITT VALUES (?, 'P', 1.0, 1, ?, 'Standard Production BOM')", (parent, primary_whs))
        children = random.sample(raw_components, 4)
        for c_idx, child in enumerate(children):
            c_qty = round(random.uniform(1.0, 5.0), 1)
            cursor.execute("INSERT INTO ITT1 VALUES (?, ?, ?, ?, ?, ?, 'B')",
                           (parent, c_idx, child, c_qty, item_lookup[child]["cost"], primary_whs))

    for i in range(1, 101):
        p_num = 65000 + i
        p_date = base_date + timedelta(days=random.randint(5, 50))
        due_d = p_date + timedelta(days=random.randint(5, 15))
        p_item = random.choice(bom_parents)
        p_qty = float(random.randint(10, 50))
        cursor.execute("INSERT INTO OWOR (DocNum, ItemCode, Status, Type, PlannedQty, CmpltQty, RjctQty, PostDate, DueDate, Warehouse, Comments) VALUES (?, ?, 'R', 'S', ?, ?, 0.0, ?, ?, ?, 'Standard assembly work order')",
                       (p_num, p_item, p_qty, p_qty, p_date.strftime("%Y-%m-%d"), due_d.strftime("%Y-%m-%d"), primary_whs))
        wor_entry = cursor.lastrowid
        for l_num, comp in enumerate(random.sample(raw_components, 3)):
            comp_qty = p_qty * random.choice([1.0, 2.0])
            cursor.execute("INSERT INTO WOR1 VALUES (?, ?, ?, 1.0, ?, ?, ?, 'M')",
                           (wor_entry, l_num, comp, comp_qty, comp_qty, primary_whs))

    for i in range(1, 101):
        doc_d = (base_date + timedelta(days=random.randint(10, 60))).strftime("%Y-%m-%d")
        r_item = random.choice(bom_parents)
        r_qty = float(random.randint(10, 50))
        r_price = item_lookup[r_item]["cost"]
        cursor.execute("INSERT INTO OIGN (DocNum, DocDate, DocTotal, Ref2, Comments) VALUES (?, ?, ?, ?, 'Receipt from production')",
                       (55000 + i, doc_d, round(r_qty * r_price, 2), f"WO-{65000 + i}"))
        ign_entry = cursor.lastrowid
        cursor.execute("INSERT INTO IGN1 VALUES (?, 0, ?, ?, ?, ?, ?, ?, ?, 202)",
                       (ign_entry, r_item, item_lookup[r_item]["name"], r_qty, r_price, round(r_qty * r_price, 2), primary_whs, 65000 + i))

        i_item = random.choice(raw_components)
        i_qty = float(random.randint(10, 100))
        i_price = item_lookup[i_item]["cost"]
        cursor.execute("INSERT INTO OIGE (DocNum, DocDate, DocTotal, Ref2, Comments) VALUES (?, ?, ?, ?, 'Issue components to production')",
                       (44000 + i, doc_d, round(i_qty * i_price, 2), f"WO-{65000 + i}"))
        ige_entry = cursor.lastrowid
        cursor.execute("INSERT INTO IGE1 VALUES (?, 0, ?, ?, ?, ?, ?, ?, ?, 202)",
                       (ige_entry, i_item, item_lookup[i_item]["name"], i_qty, i_price, round(i_qty * i_price, 2), primary_whs, 65000 + i))

    # -------------------------------------------------------------
    # SEED 21: Batches, Serials, Bins & Counting
    # -------------------------------------------------------------
    obtn_data = []
    osrn_data = []
    for i in range(1, 101):
        itm = random.choice(all_items)
        b_num = f"BAT-2026-{i:04d}"
        in_d = base_date + timedelta(days=random.randint(1, 30))
        exp_d = in_d + timedelta(days=random.randint(180, 730))
        obtn_data.append((itm, b_num, in_d.strftime("%Y-%m-%d"), exp_d.strftime("%Y-%m-%d"), in_d.strftime("%Y-%m-%d"), float(random.randint(50, 500)), 0, primary_whs))

        s_num = f"SN-8829-{i:05d}"
        c_code, _ = random.choice(customers)
        osrn_data.append((itm, s_num, f"MNF-{random.randint(10000,99999)}", f"LOT-{random.randint(100,999)}", in_d.strftime("%Y-%m-%d"), 0, primary_whs, c_code))

    cursor.executemany("INSERT INTO OBTN (ItemCode, DistNumber, MnfDate, ExpDate, InDate, Quantity, Status, WhsCode) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", obtn_data)
    cursor.executemany("INSERT INTO OSRN (ItemCode, DistNumber, MnfSerial, LotNumber, InDate, Status, WhsCode, CardCode) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", osrn_data)

    for i in range(1, 101):
        log_d = (base_date + timedelta(days=random.randint(5, 60))).strftime("%Y-%m-%d")
        itm = random.choice(all_items)
        qty = float(random.randint(5, 50))
        cursor.execute("INSERT INTO OITL (DocType, DocEntry, DocLine, ItemCode, LocCode, DocQty, DocDate) VALUES (20, ?, 0, ?, ?, ?, ?)",
                       (i, itm, primary_whs, qty, log_d))
        l_entry = cursor.lastrowid
        cursor.execute("INSERT INTO ITL1 VALUES (?, ?, ?, ?, ?, 20)", (l_entry, itm, i, qty, qty))

    obin_data = []
    for aisle in ["A", "B", "C", "D", "E"]:
        for rack in range(1, 6):
            for shelf in range(1, 5):
                bin_code = f"{primary_whs}-{aisle}{rack:02d}-{shelf:02d}"
                obin_data.append((bin_code, primary_whs, "N", "N", f"{primary_whs} Aisle {aisle} Rack {rack} Shelf {shelf}", aisle, str(rack), str(shelf)))
    cursor.executemany("INSERT INTO OBIN (BinCode, WhsCode, SysBin, Disabled, Descr, Aisle, Rack, Shelf) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", obin_data)

    for i in range(1, 101):
        c_date = (base_date + timedelta(days=random.randint(10, 60))).strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO OINC (DocNum, CountDate, Time, Status, Remarks) VALUES (?, ?, '08:30', 'C', 'Periodic stock audit')", (3000 + i, c_date))
        inc_entry = cursor.lastrowid
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 3))):
            whs_qty = float(random.randint(20, 150))
            diff = float(random.choice([0, 0, 0, 1, -1, 2, -2]))
            cnt_qty = whs_qty + diff
            cursor.execute("INSERT INTO INC1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (inc_entry, l_num, itm, item_lookup[itm]["name"], primary_whs, whs_qty, cnt_qty, diff))

    # -------------------------------------------------------------
    # SEED 22: CRM & Opportunities (OOPR, OPR1, OCLG)
    # -------------------------------------------------------------
    for i in range(1, 101):
        c_code, c_name = random.choice(customers)
        o_date = base_date + timedelta(days=random.randint(1, 45))
        c_date = o_date + timedelta(days=random.randint(15, 60))
        max_sum = round(random.uniform(5000.0, 80000.0), 2)
        status = random.choice(["W", "W", "O", "L"])
        step = 4 if status == "W" else (1 if status == "O" else 2)
        close_pct = 100.0 if status == "W" else (30.0 if status == "O" else 0.0)

        cursor.execute("INSERT INTO OOPR (CardCode, Name, OpenDate, CloseDate, MaxSumLoc, ClosePrcnt, Status, StepId) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (c_code, f"POS Upgrade Opportunity - {c_name.split()[0]}", o_date.strftime("%Y-%m-%d"), c_date.strftime("%Y-%m-%d"), max_sum, close_pct, status, step))
        opp_id = cursor.lastrowid
        for s_idx in range(1, step + 1):
            s_date = o_date + timedelta(days=s_idx * 5)
            cursor.execute("INSERT INTO OPR1 VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (opp_id, s_idx - 1, s_idx, s_idx * 25.0, max_sum, s_date.strftime("%Y-%m-%d"), c_date.strftime("%Y-%m-%d")))

    act_types = [("C", "Customer discovery phone call"), ("M", "On-site system requirements meeting"), ("T", "Prepare custom POS hardware proposal"), ("N", "Client requested pricing review")]
    for i in range(1, 101):
        c_code, _ = random.choice(customers)
        act, desc = random.choice(act_types)
        act_date = (base_date + timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO OCLG (Action, CntctType, CardCode, DocType, DocEntry, Recontact, Details, Status) VALUES (?, 1, ?, 17, ?, ?, ?, 'C')",
                       (act, c_code, i, act_date, desc))

    # -------------------------------------------------------------
    # SEED 23A: Landed Costs & Allocation (OALC, OIPF, IPF1, IPF2)
    # -------------------------------------------------------------
    oalc_master = [
        ("LC001", "Ocean Freight International", "510010", "V"),
        ("LC002", "Customs Clearance & Brokerage Fee", "510020", "Q"),
        ("LC003", "Import Duty Tariff", "510030", "V"),
        ("LC004", "Marine Cargo Insurance", "510040", "V"),
        ("LC005", "Port Handling & Wharfage", "510050", "Q"),
        ("LC006", "Fumigation & Quarantine Inspection", "510060", "Q"),
        ("LC007", "Air Cargo Express Surcharge", "510070", "W"),
        ("LC008", "Origin Terminal Handling", "510080", "V"),
        ("LC009", "Inland Terminal Storage & Demurrage", "510090", "Q"),
        ("LC010", "Local Cartage & Interstate Transport", "510100", "W"),
    ]
    cursor.executemany("INSERT INTO OALC VALUES (?, ?, ?, ?)", oalc_master)

    warehouse_cost_tracker = {}
    for (itm, whs, on_h, _, _, c, _, _) in oitw_data:
        warehouse_cost_tracker[(itm, whs)] = {'base_cost': c, 'total_alloc': 0.0, 'qty': on_h}

    cursor.execute("SELECT DocEntry, DocNum, DocDate, CardCode, CardName FROM OPDN ORDER BY DocEntry")
    all_grpos = cursor.fetchall()
    landed_cost_oinm_entries = []

    for grpo_entry, grpo_num, grpo_date, v_code, v_name in all_grpos:
        cursor.execute("SELECT LineNum, ItemCode, Dscription, Quantity, Price, LineTotal, WhsCode FROM PDN1 WHERE DocEntry = ? ORDER BY LineNum", (grpo_entry,))
        pdn_lines = cursor.fetchall()
        if not pdn_lines:
            continue

        doc_num = 8000 + grpo_entry
        cursor.execute("INSERT INTO OIPF (DocNum, DocDate, CardCode, CardName, CostSum, DocTotal, Comments) VALUES (?, ?, ?, ?, 0.0, 0.0, ?)",
                       (doc_num, grpo_date, v_code, v_name, f"Import Landed Cost for GRPO #{grpo_num}"))
        oipf_entry = cursor.lastrowid

        doc_items_tot = 0.0
        doc_fees_tot = 0.0

        for line_idx, (p_line, itm_code, itm_desc, qty, orig_cost, line_tot, whs_code) in enumerate(pdn_lines):
            doc_items_tot += line_tot
            fees_for_line = []
            if whs_code in ["NZNTH", "AU-SYD"]:
                fees_for_line.append(("LC001", round(qty * 25.0, 2)))
                fees_for_line.append(("LC002", round(qty * 10.0, 2)))
                fees_for_line.append(("LC005", round(qty * 8.0, 2)))
            elif whs_code in ["NZSTH", "AU-MEL"]:
                fees_for_line.append(("LC001", round(qty * 25.0, 2)))
                fees_for_line.append(("LC002", round(qty * 10.0, 2)))
                fees_for_line.append(("LC010", round(qty * 45.0, 2)))
                fees_for_line.append(("LC009", round(qty * 15.0, 2)))
            else:
                fees_for_line.append(("LC007", round(qty * 120.0, 2)))
                fees_for_line.append(("LC002", round(qty * 20.0, 2)))
                fees_for_line.append(("LC006", round(qty * 25.0, 2)))
                fees_for_line.append(("LC010", round(qty * 35.0, 2)))

            line_alloc_sum = sum(f[1] for f in fees_for_line)
            doc_fees_tot += line_alloc_sum

            cursor.execute("INSERT INTO IPF1 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 20, ?)",
                           (oipf_entry, line_idx, itm_code, itm_desc, qty, line_tot, orig_cost, line_alloc_sum, grpo_entry, p_line, whs_code))

            for f_idx, (alc_code, fee_amt) in enumerate(fees_for_line):
                cursor.execute("INSERT INTO IPF2 VALUES (?, ?, ?, ?)",
                               (oipf_entry, (line_idx * 10) + f_idx, alc_code, fee_amt))

            if (itm_code, whs_code) in warehouse_cost_tracker:
                warehouse_cost_tracker[(itm_code, whs_code)]['total_alloc'] += line_alloc_sum

            unit_alloc = round(line_alloc_sum / qty, 2)
            new_unit_val = round(orig_cost + unit_alloc, 2)
            landed_cost_oinm_entries.append((itm_code, grpo_date, 69, oipf_entry, line_idx, 0.0, 0.0, new_unit_val, line_alloc_sum, whs_code, new_unit_val, 25000.0 + line_alloc_sum))

        cursor.execute("UPDATE OIPF SET CostSum = ?, DocTotal = ? WHERE DocEntry = ?",
                       (round(doc_fees_tot, 2), round(doc_items_tot + doc_fees_tot, 2), oipf_entry))

    if stock_by_whs:
        for (itm, whs), data in warehouse_cost_tracker.items():
            base_c = data['base_cost']
            alloc = data['total_alloc']
            q = data['qty'] if data['qty'] > 0 else 100.0
            if alloc > 0:
                unit_landed_price = round(base_c + (alloc / q), 2)
            else:
                markup = 43.0 if whs == "NZNTH" else (95.0 if whs == "NZSTH" else 200.0)
                unit_landed_price = round(base_c + markup, 2) if itm.startswith("ITM-IMP") else base_c
            cursor.execute("UPDATE OITW SET AvgPrice = ? WHERE ItemCode = ? AND WhsCode = ?", (unit_landed_price, itm, whs))

        cursor.execute("SELECT DISTINCT ItemCode FROM OITW")
        distinct_items = [r[0] for r in cursor.fetchall()]
        for itm in distinct_items:
            cursor.execute("SELECT OnHand, AvgPrice FROM OITW WHERE ItemCode = ?", (itm,))
            whs_stocks = cursor.fetchall()
            tot_qty = sum(r[0] for r in whs_stocks)
            tot_val = sum(r[0] * r[1] for r in whs_stocks)
            w_avg = round(tot_val / tot_qty, 2) if tot_qty > 0 else item_lookup[itm]["cost"]
            cursor.execute("UPDATE OITM SET AvgPrice = ? WHERE ItemCode = ?", (w_avg, itm))
    else:
        for itm_code in imported_item_codes:
            base_c = item_lookup[itm_code]["cost"]
            alloc_tot = sum(data['total_alloc'] for (i, w), data in warehouse_cost_tracker.items() if i == itm_code)
            tot_on_hand = 200.0
            unit_lc = round(base_c + (alloc_tot / tot_on_hand), 2)
            cursor.execute("UPDATE OITM SET AvgPrice = ? WHERE ItemCode = ?", (unit_lc, itm_code))

    # -------------------------------------------------------------
    # SEED 23B: Dedicated Intercompany Transfer & Stacked Landed Cost Journey
    # In new_b1.db: Factory FOB at ICCChina -> Landed Cost -> Transfer ICCSIT -> Intercompany GRPO NZNTH -> Goods Issue ICCSIT -> Dest Landed Cost Overwrite -> Replenishment NZSTH / EuropeMarketPlace
    # In old_b1.db: Factory FOB at AU Warehouse -> Accumulate Landed Costs globally into OITM.AvgPrice -> Transfer AU Warehouse / AU Warehouse / VGLPER
    # -------------------------------------------------------------
    foreign_vendor_code, foreign_vendor_name = "V-1005", "Global Precision Automation Corp"

    for idx, imp_code in enumerate(intercompany_item_codes, 1):
        fob_price_aud = item_lookup[imp_code]["cost"]
        fob_price_usd = round(fob_price_aud * 0.65, 2)
        grpo_rate = 0.65
        qty = 100.0
        tot_usd = round(qty * fob_price_usd, 2)
        tot_aud = round(qty * fob_price_aud, 2)

        doc_date = (base_date + timedelta(days=5 + idx * 2)).strftime("%Y-%m-%d")
        t_date_sit = (base_date + timedelta(days=12 + idx * 2)).strftime("%Y-%m-%d")
        t_date_dest = (base_date + timedelta(days=25 + idx * 2)).strftime("%Y-%m-%d")

        # Step 1: External Factory PO in USD & GRPO at Origin Hub with AUD/USD conversion
        cursor.execute("INSERT INTO OPOR (DocNum, DocDate, DocDueDate, CardCode, CardName, DocStatus, DocTotal, DocCur, DocRate, DocTotalFC, Comments) VALUES (?, ?, ?, ?, ?, 'C', ?, 'USD', ?, ?, ?)",
                       (5900 + idx, doc_date, doc_date, foreign_vendor_code, foreign_vendor_name, tot_aud, grpo_rate, tot_usd, f"Factory External PO in USD for {imp_code} (FOB Origin: ${fob_price_usd:.2f} USD)"))
        po_entry = cursor.lastrowid
        cursor.execute("INSERT INTO POR1 (DocEntry, LineNum, ItemCode, Dscription, Quantity, Price, LineTotal, PriceFC, TotalFrgn, OpenQty, WhsCode, LineStatus) VALUES (?, 0, ?, ?, ?, ?, ?, ?, ?, 0, ?, 'C')",
                       (po_entry, imp_code, item_lookup[imp_code]["name"], qty, fob_price_aud, tot_aud, fob_price_usd, tot_usd, whs_origin))

        cursor.execute("INSERT INTO OPDN (DocNum, DocDate, CardCode, CardName, DocStatus, DocTotal, DocCur, DocRate, DocTotalFC, BaseEntry, Comments) VALUES (?, ?, ?, ?, 'C', ?, 'USD', ?, ?, ?, ?)",
                       (6900 + idx, doc_date, foreign_vendor_code, foreign_vendor_name, tot_aud, grpo_rate, tot_usd, po_entry, f"Factory GRPO at {whs_origin} (FOB ${fob_price_usd:.2f} USD converted @ rate {grpo_rate} to ${fob_price_aud:.2f} AUD)"))
        grpo_origin_entry = cursor.lastrowid
        cursor.execute("INSERT INTO PDN1 (DocEntry, LineNum, ItemCode, Dscription, Quantity, Price, LineTotal, PriceFC, TotalFrgn, WhsCode, BaseEntry, BaseLine) VALUES (?, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)",
                       (grpo_origin_entry, imp_code, item_lookup[imp_code]["name"], qty, fob_price_aud, tot_aud, fob_price_usd, tot_usd, whs_origin, po_entry))

        landed_cost_oinm_entries.append((imp_code, doc_date, 20, grpo_origin_entry, 0, qty, 0.0, fob_price_aud, tot_aud, whs_origin, fob_price_aud, 50000.0 + tot_aud))

        # Step 2: Estimated Origin Landed Cost at Factory Origin (in AUD)
        origin_fees = [
            ("LC008", round(qty * 8.0, 2)),   # Origin Terminal Handling $8/unit (AUD)
            ("LC002", round(qty * 6.0, 2)),   # Origin Export Customs $6/unit (AUD)
            ("LC010", round(qty * 10.0, 2)),  # Factory Cartage $10/unit (AUD)
        ]
        origin_fee_total = sum(f[1] for f in origin_fees)  # $24.00/unit (AUD)
        origin_unit_alloc = round(origin_fee_total / qty, 2)

        cursor.execute("INSERT INTO OIPF (DocNum, DocDate, CardCode, CardName, CostSum, DocTotal, DocType, BaseEntry, WhsCode, Comments) VALUES (?, ?, ?, ?, ?, ?, 'E', ?, ?, ?)",
                       (8900 + idx, doc_date, foreign_vendor_code, foreign_vendor_name, origin_fee_total, round(tot_aud + origin_fee_total, 2), grpo_origin_entry, whs_origin, f"Estimated Origin Landed Cost at {whs_origin} in AUD for GRPO #{6900 + idx}"))
        oipf_origin_entry = cursor.lastrowid

        cursor.execute("INSERT INTO IPF1 VALUES (?, 0, ?, ?, ?, ?, ?, ?, ?, 0, 20, ?)",
                       (oipf_origin_entry, imp_code, item_lookup[imp_code]["name"], qty, tot_aud, fob_price_aud, origin_fee_total, grpo_origin_entry, whs_origin))

        for f_idx, (alc_code, fee_amt) in enumerate(origin_fees):
            cursor.execute("INSERT INTO IPF2 VALUES (?, ?, ?, ?)", (oipf_origin_entry, f_idx, alc_code, fee_amt))

        cost_origin = round(fob_price_aud + origin_unit_alloc, 2)
        if stock_by_whs:
            cursor.execute("UPDATE OITW SET AvgPrice = ? WHERE ItemCode = ? AND WhsCode = ?", (cost_origin, imp_code, whs_origin))
        else:
            cursor.execute("UPDATE OITM SET AvgPrice = ? WHERE ItemCode = ?", (cost_origin, imp_code))

        landed_cost_oinm_entries.append((imp_code, doc_date, 69, oipf_origin_entry, 0, 0.0, 0.0, cost_origin, origin_fee_total, whs_origin, cost_origin, 52400.0))

        # Step 3: Intercompany Stock Transfer Origin -> Transit Hub (AUD)
        cursor.execute("INSERT INTO OWTQ (DocNum, DocDate, DocDueDate, FromWhsCod, ToWhsCode, DocStatus, Comments) VALUES (?, ?, ?, ?, ?, 'C', ?)",
                       (4900 + idx, t_date_sit, t_date_sit, whs_origin, whs_transit, f"Intercompany Sea Freight Transfer Request ({imp_code})"))
        wtq_entry = cursor.lastrowid
        cursor.execute("INSERT INTO WTQ1 VALUES (?, 0, ?, ?, ?, 0.0, ?, ?)",
                       (wtq_entry, imp_code, item_lookup[imp_code]["name"], qty, whs_origin, whs_transit))

        cursor.execute("INSERT INTO OWTR (DocNum, DocDate, FromWhsCod, ToWhsCode, Comments) VALUES (?, ?, ?, ?, ?)",
                       (4950 + idx, t_date_sit, whs_origin, whs_transit, f"Intercompany Stock Transfer from {whs_origin} to {whs_transit} at Valuation ({cost_origin} AUD)"))
        wtr_entry = cursor.lastrowid
        cursor.execute("INSERT INTO WTR1 VALUES (?, 0, ?, ?, ?, ?, ?, ?)",
                       (wtr_entry, imp_code, item_lookup[imp_code]["name"], qty, cost_origin, whs_origin, whs_transit))

        cost_transit = cost_origin
        if stock_by_whs:
            cursor.execute("UPDATE OITW SET AvgPrice = ? WHERE ItemCode = ? AND WhsCode = ?", (cost_transit, imp_code, whs_transit))
        landed_cost_oinm_entries.append((imp_code, t_date_sit, 67, wtr_entry, 0, qty, 0.0, cost_transit, round(qty * cost_transit, 2), whs_transit, cost_transit, 42400.0))

        # Step 4: Transfer Request Transit Hub -> Destination Hub (AUD)
        cursor.execute("INSERT INTO OWTQ (DocNum, DocDate, DocDueDate, FromWhsCod, ToWhsCode, DocStatus, Comments) VALUES (?, ?, ?, ?, ?, 'C', ?)",
                       (4970 + idx, t_date_dest, t_date_dest, whs_transit, whs_dest, f"Vessel Arrival: Transfer from {whs_transit} to {whs_dest} ({imp_code})"))
        wtq2_entry = cursor.lastrowid
        cursor.execute("INSERT INTO WTQ1 VALUES (?, 0, ?, ?, ?, 0.0, ?, ?)",
                       (wtq2_entry, imp_code, item_lookup[imp_code]["name"], qty, whs_transit, whs_dest))

        # Step 5: Intercompany GRPO at Destination Hub with Transit Inventory Cost (AUD)
        cursor.execute("INSERT INTO OPDN (DocNum, DocDate, CardCode, CardName, DocStatus, DocTotal, DocCur, DocRate, DocTotalFC, BaseEntry, Comments) VALUES (?, ?, ?, ?, 'C', ?, 'AUD', 1.0, 0.0, NULL, ?)",
                       (6950 + idx, t_date_dest, "V-1005", "Intercompany Global Supply Logistics", round(qty * cost_transit, 2), f"Intercompany GRPO at {whs_dest} from {whs_transit} in AUD (Transferred Cost {cost_transit})"))
        grpo_dest_entry = cursor.lastrowid
        cursor.execute("INSERT INTO PDN1 (DocEntry, LineNum, ItemCode, Dscription, Quantity, Price, LineTotal, PriceFC, TotalFrgn, WhsCode, BaseEntry, BaseLine) VALUES (?, 0, ?, ?, ?, ?, ?, 0.0, 0.0, ?, NULL, 0)",
                       (grpo_dest_entry, imp_code, item_lookup[imp_code]["name"], qty, cost_transit, round(qty * cost_transit, 2), whs_dest))

        landed_cost_oinm_entries.append((imp_code, t_date_dest, 20, grpo_dest_entry, 0, qty, 0.0, cost_transit, round(qty * cost_transit, 2), whs_dest, cost_transit, 42400.0))

        # Step 6: Goods Issue out of Transit Hub
        cursor.execute("INSERT INTO OIGE (DocNum, DocDate, DocTotal, Comments) VALUES (?, ?, ?, ?)",
                       (3900 + idx, t_date_dest, round(qty * cost_transit, 2), f"Goods Issue out of Sea Transit {whs_transit} at Cost ({cost_transit} AUD) for Delivery"))
        oige_entry = cursor.lastrowid
        cursor.execute("INSERT INTO IGE1 VALUES (?, 0, ?, ?, ?, ?, ?, ?, NULL, NULL)",
                       (oige_entry, imp_code, item_lookup[imp_code]["name"], qty, cost_transit, round(qty * cost_transit, 2), whs_transit))
        landed_cost_oinm_entries.append((imp_code, t_date_dest, 60, oige_entry, 0, 0.0, qty, cost_transit, round(-qty * cost_transit, 2), whs_transit, cost_transit, 0.0))

        # Step 7: Estimated Destination Landed Cost at Destination Hub
        est_dest_fees = [
            ("LC001", round(qty * 35.0, 2)),  # Ocean Freight $35/unit
            ("LC003", round(qty * 18.0, 2)),  # Import Duty $18/unit
            ("LC005", round(qty * 12.0, 2)),  # Port Wharfage $12/unit
            ("LC010", round(qty * 15.0, 2)),  # Inland Transport $15/unit
        ]
        est_fee_total = sum(f[1] for f in est_dest_fees)  # $80.00/unit
        cost_dest_est = round(cost_transit + (est_fee_total / qty), 2)

        cursor.execute("INSERT INTO OIPF (DocNum, DocDate, CardCode, CardName, CostSum, DocTotal, DocType, BaseEntry, WhsCode, Comments) VALUES (?, ?, ?, ?, ?, ?, 'E', ?, ?, ?)",
                       (8950 + idx, t_date_dest, "V-1005", "Intercompany Global Supply Logistics", est_fee_total, round((qty * cost_transit) + est_fee_total, 2), grpo_dest_entry, whs_dest, f"Estimated Destination Landed Cost ({whs_dest}) for GRPO #{6950 + idx}"))
        oipf_est_entry = cursor.lastrowid
        cursor.execute("INSERT INTO IPF1 VALUES (?, 0, ?, ?, ?, ?, ?, ?, ?, 0, 20, ?)",
                       (oipf_est_entry, imp_code, item_lookup[imp_code]["name"], qty, round(qty * cost_transit, 2), cost_transit, est_fee_total, grpo_dest_entry, whs_dest))
        for f_idx, (alc_code, fee_amt) in enumerate(est_dest_fees):
            cursor.execute("INSERT INTO IPF2 VALUES (?, ?, ?, ?)", (oipf_est_entry, f_idx, alc_code, fee_amt))

        # Step 8: Actual Final Landed Cost at Destination Hub (Overwriting Estimate)
        actual_dest_fees = [
            ("LC001", round(qty * 39.50, 2)),  # Actual Ocean Freight $39.50/unit
            ("LC003", round(qty * 19.20, 2)),  # Actual Import Duty Tariff $19.20/unit
            ("LC005", round(qty * 13.80, 2)),  # Actual Port Handling & Wharfage $13.80/unit
            ("LC006", round(qty * 8.50, 2)),   # Actual Quarantine & Inspection $8.50/unit
            ("LC010", round(qty * 17.00, 2)),  # Actual Container Haulage $17.00/unit
        ]
        actual_fee_total = sum(f[1] for f in actual_dest_fees)  # $98.00/unit
        actual_unit_alloc = round(actual_fee_total / qty, 2)
        cost_dest_final = round(cost_transit + actual_unit_alloc, 2)

        actual_date = (base_date + timedelta(days=28 + idx * 2)).strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO OIPF (DocNum, DocDate, CardCode, CardName, CostSum, DocTotal, DocType, BaseEntry, WhsCode, Comments) VALUES (?, ?, ?, ?, ?, ?, 'A', ?, ?, ?)",
                       (8970 + idx, actual_date, "V-1005", "Intercompany Global Supply Logistics", actual_fee_total, round((qty * cost_transit) + actual_fee_total, 2), grpo_dest_entry, whs_dest, f"Actual Final Landed Cost ({whs_dest}) - Reconciled & Overwriting Estimate for GRPO #{6950 + idx}"))
        oipf_act_entry = cursor.lastrowid
        cursor.execute("INSERT INTO IPF1 VALUES (?, 0, ?, ?, ?, ?, ?, ?, ?, 0, 20, ?)",
                       (oipf_act_entry, imp_code, item_lookup[imp_code]["name"], qty, round(qty * cost_transit, 2), cost_transit, actual_fee_total, grpo_dest_entry, whs_dest))
        for f_idx, (alc_code, fee_amt) in enumerate(actual_dest_fees):
            cursor.execute("INSERT INTO IPF2 VALUES (?, ?, ?, ?)", (oipf_act_entry, f_idx, alc_code, fee_amt))

        if stock_by_whs:
            # Update specific destination and regional warehouses in new_b1.db
            cursor.execute("UPDATE OITW SET AvgPrice = ? WHERE ItemCode = ? AND WhsCode = 'NZNTH'", (cost_dest_final, imp_code))
            cursor.execute("UPDATE OITW SET AvgPrice = ? WHERE ItemCode = ? AND WhsCode = 'NZSTH'", (round(cost_dest_final + 23.0, 2), imp_code))
            cursor.execute("UPDATE OITW SET AvgPrice = ? WHERE ItemCode = ? AND WhsCode = 'NZSIT'", (cost_transit, imp_code))
            cursor.execute("UPDATE OITW SET AvgPrice = ? WHERE ItemCode = ? AND WhsCode = 'EuropeMarketPlace'", (round(cost_dest_final + 38.0, 2), imp_code))
            cursor.execute("UPDATE OITW SET AvgPrice = ? WHERE ItemCode = ? AND WhsCode = 'EuropeSIT'", (cost_transit, imp_code))

            # Recompute weighted moving average in OITM.AvgPrice
            cursor.execute("SELECT OnHand, AvgPrice FROM OITW WHERE ItemCode = ?", (imp_code,))
            whs_rows = cursor.fetchall()
            tot_q = sum(r[0] for r in whs_rows)
            tot_v = sum(r[0] * r[1] for r in whs_rows)
            w_avg = round(tot_v / tot_q, 2) if tot_q > 0 else cost_dest_final
            cursor.execute("UPDATE OITM SET AvgPrice = ? WHERE ItemCode = ?", (w_avg, imp_code))
        else:
            # old_b1.db: All OITW.AvgPrice remain 0.0; OITM.AvgPrice holds accumulated $522.00 AUD
            cursor.execute("UPDATE OITM SET AvgPrice = ? WHERE ItemCode = ?", (cost_dest_final, imp_code))

        landed_cost_oinm_entries.append((imp_code, actual_date, 69, oipf_act_entry, 0, 0.0, 0.0, cost_dest_final, actual_fee_total, whs_dest, cost_dest_final, 78300.0))

    # -------------------------------------------------------------
    # SEED 24 & 25: Financial Journals & Reconciliations
    # -------------------------------------------------------------
    for i in range(1, 101):
        doc_date = (base_date + timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d")
        amount = round(random.uniform(500.0, 25000.0), 2)
        memo = random.choice(["Monthly Depreciation Run", "Accrued Utilities Adjustment", "Payroll Clearing Journal", "Intercompany Allocation", "Stock Adjustment Entry"])
        cursor.execute("INSERT INTO OJDT (BaseRef, RefDate, DueDate, TaxDate, Memo, TransType, LocTotal) VALUES (?, ?, ?, ?, ?, 30, ?)",
                       (9000 + i, doc_date, doc_date, doc_date, memo, amount))
        t_id = cursor.lastrowid
        cursor.execute("INSERT INTO JDT1 VALUES (?, 0, '600010', '600010', ?, 0.0, ?, ?, ?)", (t_id, amount, doc_date, doc_date, memo + " (Debit)"))
        cursor.execute("INSERT INTO JDT1 VALUES (?, 1, '100010', '100010', 0.0, ?, ?, ?, ?)", (t_id, amount, doc_date, doc_date, memo + " (Credit)"))

    for i in range(1, 101):
        recon_date = (base_date + timedelta(days=random.randint(10, 60))).strftime("%Y-%m-%d")
        recon_amt = round(random.uniform(200.0, 8000.0), 2)
        cursor.execute("INSERT INTO OITR (ReconDate, Total, ReconType, ReconCurr, IsCard) VALUES (?, ?, 0, 'AUD', 'C')",
                       (recon_date, recon_amt))
        r_num = cursor.lastrowid
        cursor.execute("INSERT INTO ITR1 VALUES (?, 0, ?, 0, ?, 30)", (r_num, i, recon_amt))
        cursor.execute("INSERT INTO ITR1 VALUES (?, 1, ?, 1, ?, 30)", (r_num, i, -recon_amt))

    # -------------------------------------------------------------
    # SEED 26: OWTQ & OWTR (Inventory Transfers)
    # -------------------------------------------------------------
    for i in range(1, 101):
        doc_num = 4000 + i
        doc_date = (base_date + timedelta(days=random.randint(1, 55))).strftime("%Y-%m-%d")
        due_date = (base_date + timedelta(days=random.randint(5, 60))).strftime("%Y-%m-%d")
        from_w = whs_dest if stock_by_whs else "AU-SYD"
        to_w = whs_reg1 if stock_by_whs else "AU-MEL"
        cursor.execute("INSERT INTO OWTQ (DocNum, DocDate, DocDueDate, FromWhsCod, ToWhsCode, DocStatus, Comments) VALUES (?, ?, ?, ?, ?, 'C', 'Stock replenishment request')",
                       (doc_num, doc_date, due_date, from_w, to_w))
        q_entry = cursor.lastrowid
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 3))):
            qty = random.randint(5, 25)
            cursor.execute("INSERT INTO WTQ1 VALUES (?, ?, ?, ?, ?, 0.0, ?, ?)",
                           (q_entry, l_num, itm, item_lookup[itm]["name"], qty, from_w, to_w))

        cursor.execute("INSERT INTO OWTR (DocNum, DocDate, FromWhsCod, ToWhsCode, Comments) VALUES (?, ?, ?, ?, 'Completed inventory transfer')",
                       (doc_num + 500, doc_date, from_w, to_w))
        t_entry = cursor.lastrowid
        for l_num, itm in enumerate(random.sample(all_items, random.randint(1, 3))):
            qty = random.randint(5, 25)
            cost = item_lookup[itm]["cost"]
            cursor.execute("INSERT INTO WTR1 VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (t_entry, l_num, itm, item_lookup[itm]["name"], qty, cost, from_w, to_w))

    # -------------------------------------------------------------
    # SEED 27: OINM (Inventory Audit Trail)
    # -------------------------------------------------------------
    oinm_data = []
    oinm_data.extend(landed_cost_oinm_entries[:60])
    for i in range(1, 151):
        itm = random.choice(all_items)
        doc_date = (base_date + timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d")
        trans_type = random.choice([20, 15, 67, 59, 60])
        cost = item_lookup[itm]["cost"]
        if trans_type in [20, 59]:
            in_qty, out_qty = float(random.randint(20, 80)), 0.0
            val = round(in_qty * cost, 2)
        else:
            in_qty, out_qty = 0.0, float(random.randint(5, 30))
            val = round(-out_qty * cost, 2)
        oinm_data.append((itm, doc_date, trans_type, i, 0, in_qty, out_qty, cost, val, primary_whs, cost, 15000.0 + val))
    cursor.executemany("INSERT INTO OINM (ItemCode, DocDate, TransType, CreatedBy, DocLineNum, InQty, OutQty, Price, TransValue, Warehouse, CalcPrice, Balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", oinm_data)

    # -------------------------------------------------------------
    # SEED 28: ADOC & ADT1 (Audit Trail)
    # -------------------------------------------------------------
    fields_list = [("AvgPrice", "85.00", "89.50"), ("OnHand", "150", "200"), ("CardName", "Apex Trading", "Apex Trading Pty Ltd"), ("DocStatus", "O", "C"), ("Comments", "Draft", "Approved")]
    for i in range(1, 101):
        obj_code = random.choice(["4", "2", "17", "22", "24", "46", "67"])
        update_date = (base_date + timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO ADOC VALUES (?, ?, 1, ?, 1, 'Auto audit capture')", (i, obj_code, update_date))
        f_name, old_v, new_v = random.choice(fields_list)
        cursor.execute("INSERT INTO ADT1 VALUES (?, ?, 1, 0, ?, ?, ?)", (i, obj_code, f_name, old_v, new_v))

    conn.commit()

    print("\n=================================================================")
    print(f" ✅ Complete SAP Business One Database ('{db_name}') Generated!")
    print(f" 📊 Total Tables: {len(all_tables)}")
    print("=================================================================")
    for idx, tbl in enumerate(sorted(all_tables), 1):
        cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
        count = cursor.fetchone()[0]
        print(f"  {idx:>2}. Table {tbl:<6} : {count:>4} rows")
    print("=================================================================")

    conn.close()

if __name__ == "__main__":
    init_database()
