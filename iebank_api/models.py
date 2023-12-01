from iebank_api import db
from datetime import datetime
from flask_login import UserMixin
import string, random

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Event %r>' % self.username

    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default = 0.0)
    currency = db.Column(db.String(1), nullable=False, default="€")
    country = db.Column(db.String(57), nullable=False, default = None)
    status = db.Column(db.String(10), nullable=False, default="Active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Event %r>' % self.account_number

    def __init__(self, name, currency,country):
        self.name = name
        self.account_number = ''.join(random.choices(string.digits, k=20))
        self.currency = currency
        self.country = country
        self.balance = 1000.0
        self.status = "Active"