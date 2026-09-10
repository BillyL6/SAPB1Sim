import urllib.request
import json

def test_all():
    print("Testing SAP B1 Simulator Endpoints...")

    tests = [
        ("GET", "http://localhost:5050/", None, "Web UI Homepage"),
        ("GET", "http://localhost:5050/api/kpis", None, "Cockpit KPIs"),
        ("GET", "http://localhost:5050/api/tables", None, "82 Tables Directory"),
        ("GET", "http://localhost:5050/api/document/ORDR/1", None, "Sales Order #1 Form"),
        ("GET", "http://localhost:5050/api/relationship-map/ORDR/1", None, "Relationship Map (ORDR #1)"),
        ("GET", "http://localhost:5050/api/bp/C10001", None, "Customer 360 (C10001)"),
        ("GET", "http://localhost:5050/api/item/ITM-001", None, "Item 360 (ITM-001)"),
        ("POST", "http://localhost:5050/api/sql", json.dumps({"query": "SELECT COUNT(*) AS total_items FROM OITM;"}).encode(), "SQL Studio Query Execution")
    ]

    for method, url, data, desc in tests:
        headers = {"Content-Type": "application/json"} if data else {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as res:
                content = res.read()
                print(f"  ✅ {desc:<30} -> HTTP {res.status} ({len(content)} bytes)")
        except Exception as e:
            print(f"  ❌ {desc:<30} -> Error: {e}")

if __name__ == "__main__":
    test_all()
