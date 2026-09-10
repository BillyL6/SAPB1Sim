import sqlite3
import sys

def main():
    db_name = sys.argv[1] if len(sys.argv) > 1 else "new_b1.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    print("==========================================================")
    print(f" 🚀 SAP B1 Interactive SQL Console ('{db_name}')")
    print(" Type your SQL query and press Enter.")
    print(" Type 'exit' or 'quit' to close.")
    print("==========================================================\n")

    while True:
        try:
            query = input("SQL> ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            # Execute query
            cursor.execute(query)
            
            if query.lower().startswith(("select", "pragma")):
                rows = cursor.fetchall()
                if not rows:
                    print("  (0 rows returned)\n")
                    continue

                # Get column headers
                col_names = [desc[0] for desc in cursor.description]
                
                # Format table
                # Determine column widths
                col_widths = [len(c) for c in col_names]
                str_rows = []
                for row in rows:
                    str_row = [str(val) if val is not None else "NULL" for val in row]
                    str_rows.append(str_row)
                    for i, val in enumerate(str_row):
                        col_widths[i] = max(col_widths[i], len(val))

                header_line = " | ".join(name.ljust(col_widths[i]) for i, name in enumerate(col_names))
                divider = "-+-".join("-" * col_widths[i] for i in range(len(col_names)))
                
                print(header_line)
                print(divider)
                for str_row in str_rows[:50]:  # Cap display at 50 rows
                    print(" | ".join(val.ljust(col_widths[i]) for i, val in enumerate(str_row)))

                if len(rows) > 50:
                    print(f"... and {len(rows) - 50} more rows (total {len(rows)} rows)")
                else:
                    print(f"({len(rows)} rows)\n")
            else:
                conn.commit()
                print(f" Query executed successfully. Rows affected: {cursor.rowcount}\n")

        except Exception as e:
            print(f"❌ SQL Error: {e}\n")

    conn.close()

if __name__ == "__main__":
    main()
