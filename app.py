import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# This tells Flask your HTML files are in the 'templates' folder
app = Flask(__name__)

# --- PATH CONFIGURATION ---
# This finds the 'data' folder which is one level up from 'src'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, '..', 'data')
DB_PATH = os.path.join(DB_FOLDER, 'billing.db')

# Create the data folder if it doesn't exist
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, date TEXT, subtotal REAL, tax REAL, grand_total REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS invoice_items (id INTEGER PRIMARY KEY, invoice_id INTEGER, name TEXT, price REAL, qty INTEGER, total REAL)''')
    
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        sample_products = [('Apple', 0.99), ('Banana', 0.59), ('Milk', 3.49), ('Bread', 2.49), ('Eggs', 4.19)]
        c.executemany("INSERT INTO products (name, price) VALUES (?, ?)", sample_products)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, price FROM products ORDER BY name")
    products = c.fetchall()
    conn.close()
    # Flask automatically looks in the 'templates' folder for index.html
    return render_template('index.html', products=products)

@app.route('/save_invoice', methods=['POST'])
def save_invoice():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO invoices (date, subtotal, tax, grand_total) VALUES (?, ?, ?, ?)",
              (date_now, data['subtotal'], data['tax'], data['grand_total']))
    invoice_id = c.lastrowid
    for item in data['items']:
        c.execute("INSERT INTO invoice_items (invoice_id, name, price, qty, total) VALUES (?, ?, ?, ?, ?)",
                  (invoice_id, item['name'], item['price'], item['qty'], item['total']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "invoice_id": invoice_id})

if __name__ == '__main__':
    init_db()
    print(f"Server starting... Database is at: {DB_PATH}")
    # '0.0.0.0' allows other devices on Wi-Fi to connect to your laptop
    app.run(host='0.0.0.0', port=5000, debug=True)