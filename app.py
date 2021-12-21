from flask import Flask, render_template
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route('/')
def start():
    return render_template('index.html')

@app.route('/receipt')
def receipt_action():
    return render_template('receipt.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
