import sqlite3
from datetime import datetime
import random
import string

class Database:
    def __init__(self, db_path="core/database/order_management.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_product_names_by_category(self, category):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT product FROM commodity WHERE category=?", (category,))
        products = cur.fetchall()
        conn.close()
        return products

    def get_product_price(self, product):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT price FROM commodity WHERE product=?", (product,))
        result = cur.fetchone()
        conn.close()
        return result[0] if result else 0

    def add_order(self, order_data):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO order_list (
                order_id, date, customer_name, product, 
                amount, total, status, note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_data['order_id'],
            order_data['product_date'],  # 對應資料表 date
            order_data['customer_name'],
            order_data['product_name'],  # 對應資料表 product
            order_data['product_amount'], # 對應資料表 amount
            order_data['product_total'],  # 對應資料表 total
            order_data['product_status'], # 對應資料表 status
            order_data['product_note']    # 對應資料表 note
        ))
        conn.commit()
        conn.close()

    def delete_order(self, order_id):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM order_list WHERE order_id=?", (order_id,))
        conn.commit()
        conn.close()

    def get_all_orders(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.order_id, o.date, o.customer_name, o.product,
                   c.price, o.amount, o.total, o.status, o.note
            FROM order_list o
            LEFT JOIN commodity c ON o.product = c.product
        """)
        orders = cur.fetchall()
        conn.close()
        return orders

    def generate_order_id(self):
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        rand = ''.join(random.choices(string.digits, k=3))
        return now + rand
