from flask import Blueprint,render_template,request,jsonify
from connectors.mysql_connectors import Session
from models.User import Users
from datetime import datetime
from sqlalchemy import select,func,or_

user_routes = Blueprint('user_routes', __name__)

# Get or update user profile

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password_hash = data.get('password_hash')

    # Create a new user
    new_user = Users(username=username, email=email, password_hash=password_hash)

    session = Session()
    session.add(new_user)
    session.commit()
    session.close()

    return jsonify({'message': 'User created successfully'}), 201

@user_routes.route('/users/me', methods=['GET'])
def get_user_profile():
    # Assume user authentication is implemented
    user_id = 1  # Example user ID, replace with actual authenticated user ID
    session = Session()
    user = session.query(Users).filter(Users.id == user_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_profile = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }

    session.close()
    return jsonify(user_profile)

@user_routes.route('/users/me', methods=['PUT'])
def update_user_profile():
    # Assume user authentication is implemented
    user_id = 1  # Example user ID, replace with actual authenticated user ID
    data = request.json

    session = Session()
    user = session.query(Users).filter(Users.id == user_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update user profile
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.updated_at = func.now()

    session.commit()
    session.close()

    return jsonify({'message': 'User profile updated successfully'})


