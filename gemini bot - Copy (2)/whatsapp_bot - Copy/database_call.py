import os
import sqlite3
import urllib.request
import urllib.parse
import json
import datetime
# from security import load_dotenv

# Load env variables
# load_dotenv()

BASE_URL = "https://gokultexprint.frappe.cloud"
API_TOKEN ="761f1e97da41eff"
API_SECRET ="9a8783b55964900"
DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Sales Invoices
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_invoices (
        name TEXT PRIMARY KEY,
        customer TEXT,
        posting_date TEXT,
        grand_total REAL,
        outstanding_amount REAL,
        status TEXT,
        owner TEXT,
        territory TEXT,
        customer_group TEXT,
        custom_hns_sub_transaction_mode TEXT
    )
    """)
print(init_db)