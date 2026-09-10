import sys
from init_sap_b1 import init_database

def init_old_database():
    print("=" * 70)
    print(" 🚀 Initializing 'old_b1.db' (Single-Level Company Valuation DB)...")
    print("=" * 70)
    init_database(db_name="old_b1.db", stock_by_whs=False)

if __name__ == "__main__":
    init_old_database()
