# coding=utf-8
import uuid

import yaml
from flask import Flask, flash, request, render_template
app = Flask(__name__)
app.secret_key = 'life is pointless'

with open('products.yml') as _f: #the content of products.yml is copied into vat PRODUCTS
    PRODUCTS = yaml.load(_f)

with open('denominations.yml') as _f: #the content of denominations.yml is copied into vat DENOMINATIONS
    DENOMINATIONS = yaml.load(_f)


ORDER_DB = 'orders.yml' #void at the beginning


def record_order(product_id):
    order_id = str(uuid.uuid4()).split('-', 1)[0]
    orders = {
        order_id: {
            'product_id': product_id,
        }
    }
    with open(ORDER_DB, 'a') as f:
        f.write(yaml.dump(orders, default_flow_style=False))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        flash('Order Placed Successfully') #the flash won't work - 'connection reset - 200'
    return render_template('index.jinja', products=PRODUCTS, title='Order Form')

@app.route('/404')
def error_page():
    return "This page represents a 404 error", 404


@app.route('/confirmation/<order_id>')
def confirmation(order_id):
    with open(ORDER_DB) as f:
        orders = yaml.load(f) or {}
    order = orders.get(order_id)
    if order is None:
        return render_template('404')
    # TODO other stuff has to be calculated here.
    return render_template('confirmation.jinja', order_id=order_id, title='Order Confirmation')


if __name__ == '__main__':
    app.run()
    #former parameters : debug=True, use_reloader=True
