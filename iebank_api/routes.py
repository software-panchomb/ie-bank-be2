from flask import Flask, request, jsonify
from flask_login import login_user, logout_user, login_required
from iebank_api import db, app, login_manager
from iebank_api.models import Account, User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
    response = {}
    json = request.json
    email = json['email']
    password = json['password']
    user = User.query.filter_by(email=email).first()
    if user:
        if user.password == password:
            response['message'] = 'Login successful'
            login_user(user)
        else:
            response['message'] = 'Incorrect password'
    else:
        response['message'] = 'User not found'
    
    return jsonify(response)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    response = {}
    response['message'] = 'Logout successful'
    return jsonify(response)

@app.route('/register', methods=['POST'])
def register():
    response = {}
    json = request.json

    username = json['username']
    email = json['email']
    password = json['password']

    user = User(username, email, password)

    db.session.add(user)
    db.session.commit()

    response['message'] = 'User created'
    return jsonify(response)

@app.route('/transfer', methods=['POST'])
def transfer():
    response = {}
    json = request.json
    print(json)
    sender_account_number = json['sender_account_number']
    receiver_account_number = json['receiver_account_number']
    amount = json['amount']

    sender_account = Account.query.filter_by(account_number=sender_account_number).first()
    receiver_account = Account.query.filter_by(account_number=receiver_account_number).first()

    if sender_account and receiver_account:
        if sender_account.balance >= amount:
            sender_account.balance -= amount
            receiver_account.balance += amount
            db.session.commit()
            response['message'] = 'Transfer successful'
        else:
            response['message'] = 'Insufficient funds'
    else:
        response['message'] = 'One or more accounts not found'
    
    return jsonify(response)

# TEST ROUTE (NOT FOR PRODUCTION)
@app.route('/add_money', methods=['POST'])
def add_money():
    response = {}
    json = request.json
    account_number = json['account_number']
    amount = json['amount']

    account = Account.query.filter_by(account_number=account_number).first()
    print(Account.query.all())
    if account:
        account.balance += amount
        db.session.commit()
        response['message'] = 'Money added'
    else:
        response['message'] = 'Account not found'
    
    return jsonify(response)

@app.route('/skull', methods=['GET'])
def skull():
    return 'Hi! This is the BACKEND SKULL! 💀'

@app.route('/accounts', methods=['POST'])
def create_account():
    name = request.json['name']
    currency = request.json['currency']
    country = request.json['country']
    account = Account(name, currency,country)
    db.session.add(account)
    db.session.commit()
    return format_account(account)

@app.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    accounts = Account.query.all()
    return {'accounts': [format_account(account) for account in accounts]}

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return {'users': [format_user(user) for user in users]}

@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    account.name = request.json['name']
    db.session.commit()
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    return format_account(account)

def format_account(account):
    return {
        'id': account.id,
        'name': account.name,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'country':account.country,
        'status': account.status,
        'created_at': account.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

def format_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'admin': user.admin
    }