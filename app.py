# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database
from datetime import datetime

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def index():
    orders = db.get_all_orders()
    today = datetime.now().strftime("%Y-%m-%d")
    warning = request.args.get('warning')
    return render_template('form.html', orders=orders, today=today, warning=warning)

@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():
    if request.method == 'GET':
        category = request.args.get('category')
        product_name = request.args.get('product')
        if category:
            products = db.get_product_names_by_category(category)
            return jsonify({"product": [p[0] for p in products]})
        elif product_name:
            price = db.get_product_price(product_name)
            return jsonify({"price": price})
        return jsonify({"error": "Invalid request"})

    elif request.method == 'POST':
        form = request.form
        product_name = form.get('product-name')
        price = db.get_product_price(product_name)
        order_data = {
            'order_id': db.generate_order_id(),
            'product_date': form.get('product-date'),  # 對應資料表 date
            'customer_name': form.get('customer-name'),
            'product_name': product_name,             # 對應資料表 product
            'product_amount': int(form.get('product-amount')), 
            'product_total': price * int(form.get('product-amount')),
            'product_status': form.get('product-status'),  # 對應資料表 status
            'product_note': form.get('product-note')       # 對應資料表 note
        }
        db.add_order(order_data)
        return redirect(url_for('index', warning="Order placed successfully"))

    elif request.method == 'DELETE':
        order_id = request.args.get('order_id')
        db.delete_order(order_id)
        return jsonify({"message": "Order deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5500)
