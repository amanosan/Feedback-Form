from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/test'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()


class Feedbackform(db.Model):
    __tableName__ = 'feedbackform'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200), unique=True)
    store_name = db.Column(db.String(100))
    store_rating = db.Column(db.Integer)
    customer_message = db.Column(db.Text())

    def __init__(self, customer_name, store_name, store_rating, customer_message):
        self.customer_name = customer_name
        self.store_name = store_name
        self.store_rating = store_rating
        self.customer_message = customer_message


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/success", methods=['GET', 'POST'])
def submit():
    if request.method == "POST":
        customer_name = request.form['name']
        store_name = request.form['store']
        store_rating = request.form['rating']
        customer_message = request.form['message']
        print(customer_name, customer_message, store_name, store_rating)
        if customer_name == '' or store_name == '':
            return render_template('index.html', message='Please enter required fields')

        # adding data to SQL database
        data = Feedbackform(customer_name, store_name,
                            store_rating, customer_message)
        db.session.add(data)
        db.session.commit()

        return render_template('success.html')


if __name__ == "__main__":
    db.create_all()
    app.run()
