from flask import Blueprint,render_template,request,jsonify
from connectors.mysql_connectors import Session
from models.Account import Accounts
from models.Transactions import Transactions
from sqlalchemy import select,func,or_
from flask_login import current_user,login_required

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route('/transactions', methods=['GET'])
def transactions_home():
    return render_template('transaction/transaction_manager.html')

@transaction_routes.route('/transactions', methods=['GET'])
@login_required
def get_transaction():
    # implementing auth 
    user_id = current_user.id
    print(current_user.id)
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
@login_required
def initiate_transaction():
    # authentication here
    user_id = current_user
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

@transaction_routes.route('/transactions/<int:id>', methods=['PUT'])
@login_required
def update_transaction(id):
    try:
        user_id = current_user.id
        # Get the updated transaction details from the request
        data = request.json

        session = Session()
        transaction = session.query(Transactions).filter(Transactions.id == user_id).first()

        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404

        # Update transaction details
        transaction.from_account_id = data.get('from_account_id', transaction.from_account_id)
        transaction.to_account_id = data.get('to_account_id', transaction.to_account_id)
        transaction.amount = data.get('amount', transaction.amount)
        transaction.type = data.get('type', transaction.type)
        transaction.description = data.get('description', transaction.description)

        session.commit()
        session.close()

        return jsonify({'message': 'Transaction updated successfully'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
