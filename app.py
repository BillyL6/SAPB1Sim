import os
import json
import sqlite3
import time
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_PATH = "new_b1.db"
PORT = 5050

# Map document types to their Line tables and key fields
DOC_MAP = {
    "OQUT": {"lines": "QUT1", "key": "DocEntry", "name": "Sales Quotation", "line_desc": "Dscription"},
    "ORDR": {"lines": "RDR1", "key": "DocEntry", "name": "Sales Order", "line_desc": "Dscription"},
    "ODLN": {"lines": "DLN1", "key": "DocEntry", "name": "Delivery Note", "line_desc": "Dscription"},
    "ORDN": {"lines": "RDN1", "key": "DocEntry", "name": "Sales Return", "line_desc": "Dscription"},
    "OINV": {"lines": "INV1", "key": "DocEntry", "name": "AR Invoice", "line_desc": "Dscription"},
    "ORIN": {"lines": "RIN1", "key": "DocEntry", "name": "AR Credit Memo", "line_desc": "Dscription"},
    
    "OPRQ": {"lines": "PRQ1", "key": "DocEntry", "name": "Purchase Request", "line_desc": "Dscription"},
    "OPQT": {"lines": "PQT1", "key": "DocEntry", "name": "Purchase Quotation", "line_desc": "Dscription"},
    "OPOR": {"lines": "POR1", "key": "DocEntry", "name": "Purchase Order", "line_desc": "Dscription"},
    "OPDN": {"lines": "PDN1", "key": "DocEntry", "name": "Goods Receipt PO", "line_desc": "Dscription"},
    "OPCH": {"lines": "PCH1", "key": "DocEntry", "name": "AP Invoice", "line_desc": "Dscription"},
    "ORPC": {"lines": "RPC1", "key": "DocEntry", "name": "AP Credit Memo", "line_desc": "Dscription"},
    
    "ORCT": {"lines": "RCT2", "key": "DocEntry", "name": "Incoming Payment", "line_desc": "InvoiceId"},
    "OVPM": {"lines": "VPM2", "key": "DocEntry", "name": "Outgoing Payment", "line_desc": "InvoiceId"},
    
    "OITT": {"lines": "ITT1", "key": "Father", "name": "Bill of Materials", "header_key": "Code"},
    "OWOR": {"lines": "WOR1", "key": "DocEntry", "name": "Production Order"},
    "OIGN": {"lines": "IGN1", "key": "DocEntry", "name": "Goods Receipt", "line_desc": "Dscription"},
    "OIGE": {"lines": "IGE1", "key": "DocEntry", "name": "Goods Issue", "line_desc": "Dscription"},
    
    "OWTQ": {"lines": "WTQ1", "key": "DocEntry", "name": "Transfer Request", "line_desc": "Dscription"},
    "OWTR": {"lines": "WTR1", "key": "DocEntry", "name": "Inventory Transfer", "line_desc": "Dscription"},
    "OINC": {"lines": "INC1", "key": "DocEntry", "name": "Inventory Count", "line_desc": "ItemDesc"},
    "OJDT": {"lines": "JDT1", "key": "TransId", "name": "Journal Entry", "line_desc": "LineMemo"},
    "OIPF": {"lines": "IPF1", "lines2": "IPF2", "key": "DocEntry", "name": "Landed Costs", "line_desc": "Dscription"}
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class SAPB1Handler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def send_error_json(self, message, status=400):
        self.send_json({"error": message}, status)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # 1. API: KPIs
        if path == "/api/kpis":
            self.handle_get_kpis()
            return

        # 2. API: Tables List
        elif path == "/api/tables":
            self.handle_get_tables()
            return

        # 3. API: Paginated Table Data
        elif path.startswith("/api/table/"):
            table_name = path[len("/api/table/"):]
            self.handle_get_table_data(table_name, query)
            return

        # 4. API: Document Viewer (Header + Lines)
        elif path.startswith("/api/document/"):
            parts = path.split("/")[3:]
            if len(parts) >= 2:
                doc_type = parts[0].upper()
                doc_id = parts[1]
                self.handle_get_document(doc_type, doc_id)
                return
            self.send_error_json("Invalid document endpoint. Use /api/document/:type/:id")
            return

        # 5. API: Business Partner 360
        elif path.startswith("/api/bp/"):
            card_code = path[len("/api/bp/"):]
            self.handle_get_bp_360(card_code)
            return

        # 6. API: Item 360
        elif path.startswith("/api/item/"):
            item_code = path[len("/api/item/"):]
            self.handle_get_item_360(item_code)
            return

        # 7. API: Relationship Map
        elif path.startswith("/api/relationship-map/"):
            parts = path.split("/")[3:]
            if len(parts) >= 2:
                doc_type = parts[0].upper()
                doc_id = parts[1]
                self.handle_get_relationship_map(doc_type, doc_id)
                return
            self.send_error_json("Invalid relationship map endpoint")
            return

        # Static File Serving
        self.serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/sql":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                sql = data.get("query", "").strip()
                self.handle_execute_sql(sql)
            except Exception as e:
                self.send_error_json(str(e))
            return

        self.send_error_json("Not found", 404)

    # -------------------------------------------------------------
    # API Handlers
    # -------------------------------------------------------------
    def handle_get_kpis(self):
        conn = get_db()
        cursor = conn.cursor()

        # AR Total
        cursor.execute("SELECT COALESCE(SUM(DocTotal), 0) FROM OINV")
        tot_rev = cursor.fetchone()[0]

        # AR Balances
        cursor.execute("SELECT COALESCE(SUM(Balance), 0) FROM OCRD WHERE CardType='C'")
        ar_bal = cursor.fetchone()[0]

        # AP Balances
        cursor.execute("SELECT COALESCE(SUM(ABS(Balance)), 0) FROM OCRD WHERE CardType='S'")
        ap_bal = cursor.fetchone()[0]

        # Total Stock Value
        cursor.execute("SELECT COALESCE(SUM(OnHand * AvgPrice), 0) FROM OITW")
        stock_val = cursor.fetchone()[0]

        # Open Sales Orders
        cursor.execute("SELECT COUNT(*), COALESCE(SUM(DocTotal), 0) FROM ORDR WHERE DocStatus='O'")
        open_so_cnt, open_so_tot = cursor.fetchone()

        # Open Purchase Orders
        cursor.execute("SELECT COUNT(*), COALESCE(SUM(DocTotal), 0) FROM OPOR WHERE DocStatus='O'")
        open_po_cnt, open_po_tot = cursor.fetchone()

        # Production WIP
        cursor.execute("SELECT COUNT(*) FROM OWOR WHERE Status='R'")
        active_prod = cursor.fetchone()[0]

        # Opportunities
        cursor.execute("SELECT COUNT(*), COALESCE(SUM(MaxSumLoc), 0), SUM(CASE WHEN Status='W' THEN 1 ELSE 0 END) FROM OOPR")
        opp_cnt, opp_tot, opp_won = cursor.fetchone()

        # Recent SOs
        cursor.execute("SELECT DocEntry, DocNum, DocDate, CardCode, CardName, DocTotal, DocStatus FROM ORDR ORDER BY DocDate DESC, DocNum DESC LIMIT 6")
        recent_so = [dict(r) for r in cursor.fetchall()]

        # Top Customers by Balance
        cursor.execute("SELECT CardCode, CardName, Balance, Phone FROM OCRD WHERE CardType='C' ORDER BY Balance DESC LIMIT 5")
        top_customers = [dict(r) for r in cursor.fetchall()]

        # Stock Alerts (Items near or below MinStock)
        cursor.execute("""
            SELECT T0.ItemCode, T1.ItemName, T0.WhsCode, T0.OnHand, T0.MinStock 
            FROM OITW T0 
            INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
            WHERE T0.OnHand <= T0.MinStock * 1.5 
            ORDER BY T0.OnHand ASC LIMIT 5
        """)
        stock_alerts = [dict(r) for r in cursor.fetchall()]

        conn.close()

        self.send_json({
            "kpis": {
                "total_revenue": round(tot_rev, 2),
                "ar_receivables": round(ar_bal, 2),
                "ap_payables": round(ap_bal, 2),
                "stock_valuation": round(stock_val, 2),
                "open_so_count": open_so_cnt,
                "open_so_total": round(open_so_tot, 2),
                "open_po_count": open_po_cnt,
                "open_po_total": round(open_po_tot, 2),
                "active_production": active_prod,
                "opp_count": opp_cnt,
                "opp_total": round(opp_tot, 2),
                "opp_win_rate": round((opp_won / opp_cnt * 100) if opp_cnt else 0, 1)
            },
            "recent_orders": recent_so,
            "top_customers": top_customers,
            "stock_alerts": stock_alerts
        })

    def handle_get_tables(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
        tables = [r[0] for r in cursor.fetchall()]

        res = []
        for t in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = cursor.fetchone()[0]
            category = "General"
            if t.startswith(("OINV", "INV1", "ORDR", "RDR1", "ODLN", "DLN1", "OQUT", "QUT1", "ORIN", "RIN1", "ORDN", "RDN1")):
                category = "Sales & AR"
            elif t.startswith(("OPOR", "POR1", "OPDN", "PDN1", "OPCH", "PCH1", "OPRQ", "PRQ1", "OPQT", "PQT1", "ORPC", "RPC1")):
                category = "Purchasing & AP"
            elif t.startswith(("ORCT", "RCT", "OVPM", "VPM", "OCTG", "ODSC")):
                category = "Banking & Payments"
            elif t.startswith(("OITT", "ITT1", "OWOR", "WOR1", "OIGN", "IGN1", "OIGE", "IGE1")):
                category = "Production & BOM"
            elif t.startswith(("OITM", "OITW", "OWHS", "OBTN", "OSRN", "OITL", "ITL1", "OBIN", "OINC", "INC1", "OWTR", "WTR1", "OWTQ", "WTQ1", "OINM")):
                category = "Inventory & Warehouses"
            elif t.startswith(("OACT", "OJDT", "JDT1", "OITR", "ITR1", "OBGT", "BGT1", "ODIM", "OPRC")):
                category = "Financials & Costing"
            elif t.startswith(("OCRD", "OCPR", "CRD1", "OCRG", "OOPR", "OPR1", "OCLG")):
                category = "Business Partners & CRM"
            elif t.startswith(("OPLN", "ITM1", "OSPP", "SPP1", "OSTC")):
                category = "Pricing & Taxes"
            elif t.startswith(("OALC", "OIPF", "IPF")):
                category = "Landed Costs"
            elif t.startswith(("ADOC", "ADT1")):
                category = "Audit Logs"

            res.append({"name": t, "count": cnt, "category": category})

        conn.close()
        self.send_json({"tables": res, "total_tables": len(res)})

    def handle_get_table_data(self, table_name, query):
        conn = get_db()
        cursor = conn.cursor()

        # Validate table name
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            conn.close()
            self.send_error_json(f"Table '{table_name}' does not exist.", 404)
            return

        page = int(query.get("page", [1])[0])
        limit = min(int(query.get("limit", [25])[0]), 100)
        offset = (page - 1) * limit
        search = query.get("search", [""])[0].strip()

        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [r["name"] for r in cursor.fetchall()]

        where_clause = ""
        params = []
        if search:
            search_conds = [f"{col} LIKE ?" for col in columns]
            where_clause = f"WHERE {' OR '.join(search_conds)}"
            params = [f"%{search}%"] * len(columns)

        # Count total
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} {where_clause}", params)
        total_records = cursor.fetchone()[0]

        # Fetch records
        cursor.execute(f"SELECT * FROM {table_name} {where_clause} LIMIT ? OFFSET ?", params + [limit, offset])
        rows = [dict(r) for r in cursor.fetchall()]

        conn.close()
        self.send_json({
            "table": table_name,
            "columns": columns,
            "rows": rows,
            "total": total_records,
            "page": page,
            "limit": limit,
            "total_pages": (total_records + limit - 1) // limit if limit else 1
        })

    def handle_get_document(self, doc_type, doc_id):
        conn = get_db()
        cursor = conn.cursor()

        if doc_type not in DOC_MAP:
            # Fallback to single table lookup
            try:
                cursor.execute(f"SELECT * FROM {doc_type} WHERE DocEntry=? OR DocNum=?", (doc_id, doc_id))
                row = cursor.fetchone()
                if row:
                    conn.close()
                    self.send_json({"type": doc_type, "header": dict(row), "lines": []})
                    return
            except Exception:
                pass
            conn.close()
            self.send_error_json(f"Document type '{doc_type}' not supported for form view", 400)
            return

        config = DOC_MAP[doc_type]
        header_key = config.get("header_key", "DocEntry")
        lines_table = config.get("lines")
        lines_key = config.get("key", "DocEntry")

        # Fetch header
        query = f"SELECT * FROM {doc_type} WHERE {header_key}=? OR DocNum=?" if header_key != "Code" else f"SELECT * FROM {doc_type} WHERE {header_key}=?"
        params = (doc_id, doc_id) if header_key != "Code" else (doc_id,)
        cursor.execute(query, params)
        header_row = cursor.fetchone()

        if not header_row:
            conn.close()
            self.send_error_json(f"Document {doc_type} #{doc_id} not found", 404)
            return

        header = dict(header_row)
        actual_id = header.get(header_key, doc_id)

        # Fetch lines
        cursor.execute(f"SELECT * FROM {lines_table} WHERE {lines_key}=?", (actual_id,))
        lines = [dict(r) for r in cursor.fetchall()]

        lines2 = []
        if "lines2" in config:
            cursor.execute(f"SELECT * FROM {config['lines2']} WHERE {lines_key}=?", (actual_id,))
            lines2 = [dict(r) for r in cursor.fetchall()]

        conn.close()
        self.send_json({
            "doc_type": doc_type,
            "doc_name": config.get("name", doc_type),
            "header": header,
            "lines": lines,
            "lines2": lines2
        })

    def handle_get_bp_360(self, card_code):
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM OCRD WHERE CardCode=?", (card_code,))
        bp = cursor.fetchone()
        if not bp:
            conn.close()
            self.send_error_json(f"Business Partner '{card_code}' not found", 404)
            return

        bp_dict = dict(bp)

        # Addresses
        cursor.execute("SELECT * FROM CRD1 WHERE CardCode=?", (card_code,))
        addresses = [dict(r) for r in cursor.fetchall()]

        # Contacts
        cursor.execute("SELECT * FROM OCPR WHERE CardCode=?", (card_code,))
        contacts = [dict(r) for r in cursor.fetchall()]

        # Recent Orders / Documents
        if bp_dict.get("CardType") == "C":
            cursor.execute("SELECT DocEntry, DocNum, DocDate, DocTotal, DocStatus FROM ORDR WHERE CardCode=? ORDER BY DocDate DESC LIMIT 5", (card_code,))
            orders = [dict(r) for r in cursor.fetchall()]
            cursor.execute("SELECT DocEntry, DocNum, DocDate, DocTotal, DocStatus FROM OINV WHERE CardCode=? ORDER BY DocDate DESC LIMIT 5", (card_code,))
            invoices = [dict(r) for r in cursor.fetchall()]
            cursor.execute("SELECT DocEntry, DocNum, DocDate, DocTotal FROM ORCT WHERE CardCode=? ORDER BY DocDate DESC LIMIT 5", (card_code,))
            payments = [dict(r) for r in cursor.fetchall()]
        else:
            cursor.execute("SELECT DocEntry, DocNum, DocDate, DocTotal, DocStatus FROM OPOR WHERE CardCode=? ORDER BY DocDate DESC LIMIT 5", (card_code,))
            orders = [dict(r) for r in cursor.fetchall()]
            cursor.execute("SELECT DocEntry, DocNum, DocDate, DocTotal, DocStatus FROM OPCH WHERE CardCode=? ORDER BY DocDate DESC LIMIT 5", (card_code,))
            invoices = [dict(r) for r in cursor.fetchall()]
            cursor.execute("SELECT DocEntry, DocNum, DocDate, DocTotal FROM OVPM WHERE CardCode=? ORDER BY DocDate DESC LIMIT 5", (card_code,))
            payments = [dict(r) for r in cursor.fetchall()]

        # Opportunities
        cursor.execute("SELECT OpprId, Name, OpenDate, MaxSumLoc, ClosePrcnt, Status FROM OOPR WHERE CardCode=? ORDER BY OpenDate DESC LIMIT 5", (card_code,))
        opps = [dict(r) for r in cursor.fetchall()]

        conn.close()
        self.send_json({
            "bp": bp_dict,
            "addresses": addresses,
            "contacts": contacts,
            "orders": orders,
            "invoices": invoices,
            "payments": payments,
            "opportunities": opps
        })

    def handle_get_item_360(self, item_code):
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM OITM WHERE ItemCode=?", (item_code,))
        item = cursor.fetchone()
        if not item:
            conn.close()
            self.send_error_json(f"Item '{item_code}' not found", 404)
            return

        item_dict = dict(item)

        # Warehouses stock
        cursor.execute("""
            SELECT T0.*, T1.WhsName, T1.City 
            FROM OITW T0 
            INNER JOIN OWHS T1 ON T0.WhsCode = T1.WhsCode 
            WHERE T0.ItemCode=?
        """, (item_code,))
        whs_stock = [dict(r) for r in cursor.fetchall()]

        # Prices
        cursor.execute("""
            SELECT T0.PriceList, T1.ListName, T0.Price, T0.Currency, T1.Factor 
            FROM ITM1 T0 
            INNER JOIN OPLN T1 ON T0.PriceList = T1.ListNum 
            WHERE T0.ItemCode=?
        """, (item_code,))
        prices = [dict(r) for r in cursor.fetchall()]

        # Batches
        cursor.execute("SELECT * FROM OBTN WHERE ItemCode=? ORDER BY ExpDate ASC", (item_code,))
        batches = [dict(r) for r in cursor.fetchall()]

        # BOM Components if parent
        cursor.execute("""
            SELECT T0.Father, T0.ChildNum, T0.Code, T1.ItemName, T0.Quantity, T0.Price 
            FROM ITT1 T0 
            INNER JOIN OITM T1 ON T0.Code = T1.ItemCode 
            WHERE T0.Father=?
        """, (item_code,))
        bom_components = [dict(r) for r in cursor.fetchall()]

        conn.close()
        self.send_json({
            "item": item_dict,
            "warehouses": whs_stock,
            "prices": prices,
            "batches": batches,
            "bom": bom_components
        })

    def handle_get_relationship_map(self, doc_type, doc_id):
        conn = get_db()
        cursor = conn.cursor()

        nodes = []
        links = []

        # Find current doc
        try:
            cursor.execute(f"SELECT DocEntry, DocNum, DocDate, DocTotal, CardName FROM {doc_type} WHERE DocEntry=? OR DocNum=?", (doc_id, doc_id))
            curr = cursor.fetchone()
        except Exception:
            curr = None

        if not curr:
            conn.close()
            self.send_error_json("Document not found", 404)
            return

        entry = curr["DocEntry"]
        doc_num = curr["DocNum"]
        card_name = curr["CardName"] if "CardName" in curr.keys() else ""
        tot = curr["DocTotal"] if "DocTotal" in curr.keys() else 0.0

        # Build realistic O2C or P2P chain based on doc_type and entry id
        if doc_type in ["OQUT", "ORDR", "ODLN", "OINV", "ORCT", "ORDN", "ORIN"]:
            nodes.append({"id": "OQUT", "type": "OQUT", "name": f"Sales Quote #{800 + (entry % 100) + 1}", "amount": tot * 1.05, "status": "Closed", "current": doc_type == "OQUT"})
            nodes.append({"id": "ORDR", "type": "ORDR", "name": f"Sales Order #{1000 + (entry % 100) + 1}", "amount": tot, "status": "Closed", "current": doc_type == "ORDR"})
            nodes.append({"id": "ODLN", "type": "ODLN", "name": f"Delivery #{2000 + (entry % 100) + 1}", "amount": tot, "status": "Closed", "current": doc_type == "ODLN"})
            nodes.append({"id": "OINV", "type": "OINV", "name": f"AR Invoice #{3000 + (entry % 100) + 1}", "amount": tot, "status": "Closed", "current": doc_type == "OINV"})
            nodes.append({"id": "ORCT", "type": "ORCT", "name": f"Incoming Pay #{90000 + (entry % 100) + 1}", "amount": tot, "status": "Settled", "current": doc_type == "ORCT"})

            links = [
                {"from": "OQUT", "to": "ORDR"},
                {"from": "ORDR", "to": "ODLN"},
                {"from": "ODLN", "to": "OINV"},
                {"from": "OINV", "to": "ORCT"}
            ]
        elif doc_type in ["OPRQ", "OPQT", "OPOR", "OPDN", "OPCH", "OVPM", "OIPF"]:
            nodes.append({"id": "OPRQ", "type": "OPRQ", "name": f"Purchase Req #{4500 + (entry % 100) + 1}", "amount": tot, "status": "Closed", "current": doc_type == "OPRQ"})
            nodes.append({"id": "OPQT", "type": "OPQT", "name": f"Purchase Quote #{4700 + (entry % 100) + 1}", "amount": tot, "status": "Closed", "current": doc_type == "OPQT"})
            nodes.append({"id": "OPOR", "type": "OPOR", "name": f"Purchase Order #{5000 + (entry % 100) + 1}", "amount": tot, "status": "Closed", "current": doc_type == "OPOR"})
            nodes.append({"id": "OPDN", "type": "OPDN", "name": f"Goods Receipt PO #{6000 + (entry % 100) + 1}", "amount": tot, "status": "Closed", "current": doc_type == "OPDN"})
            nodes.append({"id": "OPCH", "type": "OPCH", "name": f"AP Invoice #{7000 + (entry % 100) + 1}", "amount": tot, "status": "Closed", "current": doc_type == "OPCH"})
            nodes.append({"id": "OVPM", "type": "OVPM", "name": f"Outgoing Pay #{80000 + (entry % 100) + 1}", "amount": tot, "status": "Settled", "current": doc_type == "OVPM"})

            links = [
                {"from": "OPRQ", "to": "OPQT"},
                {"from": "OPQT", "to": "OPOR"},
                {"from": "OPOR", "to": "OPDN"},
                {"from": "OPDN", "to": "OPCH"},
                {"from": "OPCH", "to": "OVPM"}
            ]
        else:
            nodes.append({"id": doc_type, "type": doc_type, "name": f"{doc_type} #{doc_num}", "amount": tot, "status": "Standard", "current": True})

        conn.close()
        self.send_json({
            "nodes": nodes,
            "links": links,
            "card_name": card_name
        })

    def handle_execute_sql(self, sql):
        if not sql:
            self.send_error_json("SQL query cannot be empty")
            return

        conn = get_db()
        cursor = conn.cursor()
        t0 = time.time()
        try:
            cursor.execute(sql)
            if sql.strip().upper().startswith(("SELECT", "PRAGMA", "EXPLAIN")):
                rows_raw = cursor.fetchmany(250)
                duration_ms = round((time.time() - t0) * 1000, 2)
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = [dict(r) for r in rows_raw]
                conn.close()
                self.send_json({
                    "columns": columns,
                    "rows": rows,
                    "count": len(rows),
                    "duration_ms": duration_ms
                })
            else:
                conn.commit()
                duration_ms = round((time.time() - t0) * 1000, 2)
                affected = cursor.rowcount
                conn.close()
                self.send_json({
                    "columns": [],
                    "rows": [],
                    "count": 0,
                    "affected_rows": affected,
                    "duration_ms": duration_ms,
                    "message": f"Query executed successfully. Rows affected: {affected}"
                })
        except Exception as e:
            conn.close()
            self.send_error_json(f"SQL Error: {str(e)}", 400)

    # -------------------------------------------------------------
    # Static Files
    # -------------------------------------------------------------
    def serve_static(self, path):
        if path in ["/", ""]:
            path = "/index.html"

        file_path = os.path.join("static", path.lstrip("/"))
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            file_path = os.path.join("static", "index.html")

        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "text/plain"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error_json(f"File read error: {e}", 500)

def run():
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, SAPB1Handler)
    print(f"============================================================")
    print(f" 🚀 SAP Business One UI Simulator is LIVE on port {PORT}")
    print(f" 🌐 Access Web UI: http://localhost:{PORT}")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n Server stopped.")
        httpd.server_close()

if __name__ == "__main__":
    run()
