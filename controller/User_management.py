from flask import Blueprint,render_template,request,jsonify
from connectors.mysql_connectors import Session
from models.User import Users
from datetime import datetime
from sqlalchemy import select,func,or_
from flask_login import current_user,login_required


user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users/me', methods=['GET'])
def user_home():
    return render_template('user/user_profile.html')

@user_routes.route('/users', methods=['POST'])
@login_required
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
@login_required
def get_user_profile():
    try:
        user_id = current_user.id
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
        return render_template('user_profile.html', user=user_profile)
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user_profile():
    try:
        user_id = current_user.id
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
        return jsonify({'message': 'User profile updated successfully'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    finally:
        session.close()

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user_profile():
    try:
        user_id = current_user.id
        session = Session()
        user = session.query(Users).filter(Users.id == user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        session.delete(user)
        session.commit()

        return jsonify({'message': 'User profile deleted successfully'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    finally:
        session.close()



