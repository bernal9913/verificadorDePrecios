from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

products = []

def add_product(product_id, product_name, product_price):
    product = {
        'id': product_id,
        'name': product_name,
        'price': product_price
    }
    products.append(product)

def load_products_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            product_id = row['id']
            product_name = row['name']
            product_price = float(row['price'])
            add_product(product_id, product_name, product_price)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    product_code = request.form['product_code']
    product = next((p for p in products if p['id'] == product_code), None)
    if product:
        product_id = product['id']
        product_name = product['name']
        product_price = product['price']
    else:
        product_id = 'Producto no encontrado'
        product_name = ''
        product_price = ''
    response = {
        'product_id': product_id,
        'product_name': product_name,
        'product_price': product_price
    }
    return jsonify(response)

if __name__ == '__main__':
    load_products_from_csv('products.csv')  # Ruta al archivo CSV con los productos
    app.run()
