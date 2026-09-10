import sys
from init_sap_b1 import init_database

def init_new_database():
    print("=" * 70)
    print(" 🚀 Initializing 'new_b1.db' (Multi-Warehouse Costing DB)...")
    print("=" * 70)
    init_database(db_name="new_b1.db", stock_by_whs=True)

if __name__ == "__main__":
    init_new_database()
