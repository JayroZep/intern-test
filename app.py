# coding=utf-8
import uuid

import yaml
from flask import Flask, flash, request, render_template
app = Flask(__name__)
app.secret_key = 'life is pointless'

with open('products.yml') as _f: #the content of products.yml is copied into var PRODUCTS
    PRODUCTS = yaml.load(_f)

with open('denominations.yml') as _f: #the content of denominations.yml is copied into var DENOMINATIONS
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
    context = {}
    if request.method == 'POST':
        record_order(0) #0 just for testing
        print(request.form)
        flash('Order Placed Successfully')
    return render_template('index.jinja', products=PRODUCTS, title='Order Form', **context)

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
    # We have to set all variables that will be displayed in confirmation.jinja : order_id, amount_paid, item_price, change_due
    # But how to access those variables, that are created directly in the .jinja ?
    # How can I use the result of the POST method in index() ? Should I create some temp file and put data from the form into?
    return render_template('confirmation.jinja', order_id=order_id , title='Order Confirmation')


if __name__ == '__main__':
    app.run()
    #former parameters : debug=True, use_reloader=True
