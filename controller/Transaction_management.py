from flask import Blueprint,render_template,request,jsonify
from connectors.mysql_connectors import Session
from models.Account import Accounts
from models.Transactions import Transactions
from sqlalchemy import select,func,or_

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route('/transactions', methods=['GET'])
def get_transactions():
    # belum implement user auth 
    user_id = 1  ##user.id
    session = Session()

    transactions = session.query(Transactions).join(Accounts).filter(Accounts.user_id == user_id)

    # Filter by account ID
    account_id = request.args.get('account_id')
    if account_id:
        transactions = transactions.filter(Transactions.from_account_id == account_id)

    # Filter by date range
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date and end_date:
        transactions = transactions.filter(Transactions.created_at.between(start_date, end_date))

    transaction_list = []
    for transaction in transactions:
        transaction_list.append({
            'id': transaction.id,
            'from_account_id': transaction.from_account_id,
            'to_account_id': transaction.to_account_id,
            'amount': transaction.amount,
            'type': transaction.type,
            'description': transaction.description,
            'created_at': transaction.created_at
        })

    session.close()
    return jsonify(transaction_list)

@transaction_routes.route('/transactions/<int:id>', methods=['GET'])
def get_transaction_details(id):
    # implementing auth 
    user_id = 1  # Example user ID
    session = Session()

    # Retrieve the transaction by its ID
    transaction = session.query(Transactions).join(Accounts).filter(Transactions.id == id, Accounts.user_id == user_id).first()

    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    transaction_details = {
        'id': transaction.id,
        'from_account_id': transaction.from_account_id,
        'to_account_id': transaction.to_account_id,
        'amount': transaction.amount,
        'type': transaction.type,
        'description': transaction.description,
        'created_at': transaction.created_at
    }

    session.close()
    return jsonify(transaction_details)

@transaction_routes.route('/transactions', methods=['POST'])
def initiate_transaction():
    # authentication here
    user_id = 1  
    data = request.json

    # Create a new transaction
    new_transaction = Transactions(
        from_account_id=data.get('from_account_id'),
        to_account_id=data.get('to_account_id'),
        amount=data.get('amount'),
        type=data.get('type'),
        description=data.get('description')
    )

    session = Session()
    session.add(new_transaction)
    session.commit()
    session.close()

    return jsonify({'message': 'Transaction initiated successfully'}), 201