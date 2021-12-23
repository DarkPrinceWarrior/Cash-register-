import random

import requests as requests
from flask import Flask, render_template, request, flash, jsonify
from flask_restful import Api
import webbrowser
import simplejson as json
import time
from sqlalchemy.orm import sessionmaker
from DAO.cash_database import db_session as db_session, PaymentModel, ReceiptModel

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

        POST_payment_dict = {
            "PAY_ACTION": "REG_PAYMENT",
            "PAY_ITOG": sum,
            "PAY_NAME": item
        }

        reg = "https://pay.pay-ok.org/demo/?REQ={0}".format(json.dumps(POST_payment_dict, ensure_ascii=False))

        response1 = requests.post(reg)
        res1 = response1.json()

        GET_payment_dict = {
            "PAY_ACTION": "GET_PAYMENT_INFO",
            "PAY_ID": res1["PAY_ID"]
        }

        get_pay_inf = "https://pay.pay-ok.org/demo/?REQ={0}".format(json.dumps(GET_payment_dict, ensure_ascii=False))

        if webbrowser.open(res1["PAY_URL"]):
            time.sleep(30)
            pay_id = res1["PAY_ID"]
            bank_response = requests.get(f"https://pay.pay-ok.org/demo/index.php?id={pay_id}")
            text = bank_response.text
            if "<p>Операция оплаты отменена клиентом</p>" in text:
                return render_template('cancel_payment.html')
            else:
                response2 = requests.get(get_pay_inf)
                res2 = response2.json()

                payment_inf = PaymentModel(payment_id=res2["STATUS"]["params"]["payment_id"],
                                           item_sum=res2["STATUS"]["params"]["paidAmount"],
                                           item_name=res2["STATUS"]["options"]["PAY_NAME"],
                                           order_id=res2["STATUS"]["params"]["order_id"],
                                           paid_date=res2["STATUS"]["params"]["paidDate"],
                                           created_date=res2["STATUS"]["params"]["createdDate"],
                                           status=res2["STATUS"]["params"]["status"],
                                           session_id=res2["STATUS"]["params"]["session_id"],
                                           text_status=res2["STATUS"]["params"]["textstatus"]
                                           )
                db_session.add(payment_inf)
                db_session.commit()
                db_session.close()

                return render_template('index.html')

    else:
        return render_template('index.html')


@app.route('/payment', methods=('GET', 'POST'))
def payment_information():

    if request.method == 'POST':

        payment_id = request.form['payment_id']
        try:
            if not payment_id:
                flash('payment_id is required!')
            float(payment_id)
        except ValueError:
            flash('payment_id data is not valid!')

        GET_payment_inf_dict = {
            "PAY_ACTION": "GET_PAYMENT_INFO",
            "PAY_ID": payment_id
        }

        reg = "https://pay.pay-ok.org/demo/?REQ={0}".format(json.dumps(GET_payment_inf_dict, ensure_ascii=False))

        response1 = requests.get(reg)
        res = response1.json()

        name = res["STATUS"]["options"]["PAY_NAME"]
        sum = res["STATUS"]["params"]["paidAmount"]
        date = res["STATUS"]["params"]["paidDate"]

        return render_template('payment_info.html',name=name ,sum=sum,date=date)

    else:

        payments = db_session.query(PaymentModel).all()
        db_session.close()

        return render_template('payment.html', payments=payments)


@app.route('/receipt', methods=('GET', 'POST'))
def receipt_action():
    payments = db_session.query(PaymentModel).all()
    db_session.close()

    if request.method == 'POST':

        date = ""
        pay_id = ""
        pay_ls = ""
        sum = request.form['sum']
        name = request.form['name']
        email = request.form['email']

        for i in payments:
            if i.item_name == name:
                date = i.paid_date
                pay_id = i.payment_id
                pay_ls = i.order_id
                break

        random_integer = random.randint(1, 100000)
        pay_ls = int(pay_ls)
        pay_ls += random_integer

        POST_receipt_reg_dict = {
            "PAY_ID": pay_id,
            "PAY_ACTION": "REG",
            "PAY_DATE": date,
            "PAY_EMAIL": email,
            "PAY_LS": pay_ls,
            "PAY_ITOG": sum,
            "PAY_NAME": name
        }

        GET_receipt_inf = {
            "PAY_ID": pay_id,
            "PAY_ACTION": "GET_INFO"}

        reg = "https://pay.pay-ok.org/demo/?REQ={0}".format(json.dumps(POST_receipt_reg_dict, ensure_ascii=False))
        requests.post(reg)

        reg = "https://pay.pay-ok.org/demo/?REQ={0}".format(json.dumps(GET_receipt_inf, ensure_ascii=False))
        res = requests.get(reg)
        res1 = res.json()


        receipt = ReceiptModel(payment_id=res1["STATUS"]["params"]["payment_id"],
                               item_sum=sum,
                               item_name=name,
                               receipt_date=res1["STATUS"]["params"]["date"],
                               lsc=res1["STATUS"]["params"]["lsc"],)
        db_session.add(receipt)
        db_session.commit()
        db_session.close()

        return render_template('index.html')

    else:

        return render_template('receipt.html', payments=payments)


@app.route('/receipt/details', methods=('GET', 'POST'))
def receipt_details():

    receipts = db_session.query(ReceiptModel).all()
    db_session.close()

    if request.method == 'POST':

        payment_id = request.form['payment_id']

        GET_receipt_inf_dict = {
            "PAY_ID": payment_id,
            "PAY_ACTION": "GET_INFO"
        }

        reg = "https://pay.pay-ok.org/demo/?REQ={0}".format(json.dumps(GET_receipt_inf_dict, ensure_ascii=False))

        response1 = requests.get(reg)
        res = response1.json()

        name = ""
        sum = 0.0

        for i in receipts:
            if i.payment_id == payment_id:
                name = i.item_name
                sum =i.item_sum
                break

        date = res["STATUS"]["params"]["date"]
        lsc = res["STATUS"]["params"]["lsc"]

        return render_template('receipt_inf.html', name=name, sum=sum, date=date, lsc=lsc)

    else:

        return render_template('choose_receipt.html', receipts=receipts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
