from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_mail import Mail

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__)


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_id'],
    MAIL_PASSWORD=params['gmail_password']


)
mail = Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    msg = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    phone = db.Column(db.String(12), nullable=False)


@app.route('/')
def index():
    return render_template('index.html', params=params)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        phone = request.form.get("phone")
        msg = request.form.get("msg")
        email = request.form.get("email")
        entry = Contact(name=name, phone=phone, msg=msg, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New Message From ' + name,
                          sender=email,
                          recipients=[params['gmail_id']],
                          body=msg + "\n" + phone
                          )
    return render_template('contact.html', params=params)


@app.route('/post')
def post():
    return render_template('post.html', params=params)


app.run(debug=True)
