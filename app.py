import requests as requests
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_restful import Api
import codecs
import webbrowser

import simplejson as json

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = '123456iejcrh84f8j84hv'
# app.config['JSON_AS_ASCII'] = False



@app.route('/', methods=('GET', 'POST'))
def payment_register():

    if request.method == 'POST':

        sum = request.form['sum']
        item = request.form['item']

        try:
            if not sum:
                flash('Sum is required!')
            float(sum)

            if not item:
                flash('Item name is required!')

        except ValueError:
            flash('sum data is not valid!')


        GET_payment_dict = {
            "PAY_ACTION": "GET_PAYMENT_INFO",
            "PAY_ID": "071021132755"
        }

        POST_payment_dict = {
            "PAY_ACTION": "REG_PAYMENT",
            "PAY_ITOG":sum,
            "PAY_NAME":item
        }

        reg = "https://pay.pay-ok.org/demo/?REQ={0}".format(json.dumps(POST_payment_dict,ensure_ascii=False ))

        response1 = requests.post(reg)

        res = response1.json()

        if webbrowser.open(res["PAY_URL"]):return render_template('index.html')

    else:
        return render_template('index.html')


@app.route('/payment', methods=('GET', 'POST'))
def payment_information():

    if request.method == 'POST':

        id = request.form['id']
        try:
            if not id:
                flash('id is required!')
            float(id)
        except ValueError:
            flash('id data is not valid!')

        POST_payment_inf_dict = {
            "PAY_ACTION": "GET_PAYMENT_INFO",
            "PAY_ID": id
        }

        reg = "https://pay.pay-ok.org/demo/?REQ={0}".format(json.dumps(POST_payment_inf_dict, ensure_ascii=False))

        response1 = requests.get(reg)

        res = response1.json()

        return res

    else:
        return render_template('payment.html')



@app.route('/receipt',  methods=('GET', 'POST'))
def receipt_action():

    if request.method == 'POST':

        id = request.form['id']
        sum = request.form['sum']
        name = request.form['name']
        date = request.form['date']
        email = request.form['email']

        try:
            if not id:
                flash('id is required!')
            if not sum:
                flash('sum is required!')
            if not name:
                flash('name is required!')
            if not date:
                flash('date is required!')
            if not email:
                flash('email is required!')

            float(id)
            float(sum)

        except ValueError:
            flash('some data is not valid!')

        POST_receipt_reg_dict = {
            "PAY_ID": id,
            "PAY_ACTION": "REG",
            "PAY_DATE": date,
            "PAY_EMAIL": email,
            "PAY_LS": "724144",
            "PAY_ITOG": sum,
            "PAY_NAME": name
        }

        reg = "https://pay.pay-ok.org/demo/?REQ={0}".format(json.dumps(POST_receipt_reg_dict, ensure_ascii=False))

        response1 = requests.get(reg)

        res = response1.json()

        return res

    else:
        return render_template('receipt.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
