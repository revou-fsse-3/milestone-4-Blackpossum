from flask import Blueprint,render_template,request,jsonify
from connectors.mysql_connectors import Session
from models.Account import Accounts
from sqlalchemy import select,func,or_
from flask_login import current_user,login_required


account_routes = Blueprint('account_routes', __name__)

@account_routes.route('/accounts', methods=['GET'])
@login_required
def get_user_accounts():
    try:
        # Get the authenticated user's ID
        user_id = current_user.id

        # Query the database for the user's accounts
        session = Session()
        accounts = session.query(Accounts).filter(Accounts.user_id == user_id).all()

        # Format the accounts data
        user_accounts = []
        for account in accounts:
            user_accounts.append({
                'id': account.id,
                'account_type': account.account_type,
                'account_number': account.account_number,
                'balance': account.balance,
                'created_at': account.created_at,
                'updated_at': account.updated_at
            })

        session.close()

        # Return the user's account using template 
        return render_template('account/user_account.html',user_accounts=user_accounts)
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching user accounts'}), 500

@account_routes.route('/accounts/<int:id>', methods=['GET'])
@login_required
def get_account_details(id):
    # Assume user authentication is implemented
    user_id = current_user.id  # Example user ID, replace with actual authenticated user ID
    session = Session()
    account = session.query(Accounts).filter(Accounts.id == id, Accounts.user_id == user_id).first()

    if not account:
        return jsonify({'error': 'Account not found'}), 404

    account_details = {
        'id': account.id,
        'account_type': account.account_type,
        'account_number': account.account_number,
        'balance': account.balance,
        'created_at': account.created_at,
        'updated_at': account.updated_at
    }

    session.close()
    return jsonify(account_details)

@account_routes.route('/accounts', methods=['POST'])
def create_account():
    # Assume user authentication is implemented
    user_id = current_user.id  # Example user ID, replace with actual authenticated user ID
    data = request.json

    # Create a new account
    new_account = Accounts(
        user_id=user_id,
        account_type=data.get('account_type'),
        account_number=data.get('account_number'),
        balance=data.get('balance', 0.0)
    )

    session = Session()
    session.add(new_account)
    session.commit()
    session.close()

    return jsonify({'message': 'Account created successfully'}), 201

@account_routes.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    # Assume user authentication is implemented
    user_id = current_user.id  # Example user ID, replace with actual authenticated user ID
    data = request.json

    session = Session()
    account = session.query(Accounts).filter(Accounts.id == id, Accounts.user_id == user_id).first()

    if not account:
        return jsonify({'error': 'Account not found'}), 404

    # Update account details
    account.account_type = data.get('account_type', account.account_type)
    account.account_number = data.get('account_number', account.account_number)
    account.balance = data.get('balance', account.balance)
    account.updated_at = func.now()

    session.commit()
    session.close()

    return jsonify({'message': 'Account updated successfully'})

@account_routes.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    # Assume user authentication is implemented
    user_id = current_user.id  # Example user ID, replace with actual authenticated user ID

    session = Session()
    account = session.query(Accounts).filter(Accounts.id == id, Accounts.user_id == user_id).first()

    if not account:
        return jsonify({'error': 'Account not found'}), 404

    session.delete(account)
    session.commit()
    session.close()

    return jsonify({'message': 'Account deleted successfully'})


