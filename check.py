import sqlite3

DB_PATH = "core/database/order_management.db"  # 改成你的路徑

def show_tables_and_columns():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        # 查所有 table
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        print("Tables:", tables)

        for table_name, in tables:
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = cur.fetchall()
            print(f"{table_name} columns:", columns)

def show_all_data(table_name):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name};")
        rows = cur.fetchall()
        print(f"Data in {table_name}:")
        for row in rows:
            print(row)

if __name__ == "__main__":
    show_tables_and_columns()
    print("\n--- Order List ---")
    show_all_data("order_list")
    print("\n--- Commodity ---")
    show_all_data("commodity")
