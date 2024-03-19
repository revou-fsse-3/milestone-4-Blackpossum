from flask import Blueprint,render_template,request,jsonify
from connectors.mysql_connectors import Session
from models.User import Users
from datetime import datetime
from sqlalchemy import select,func,or_

user_routes = Blueprint('user_routes', __name__)

# Get or update user profile
@user_routes.route("/user", methods=['GET'])
def get_user():
    
    try:
        session = Session()
        users = session.query(Users).all()
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            user_list.append(user_data)
        
        return jsonify(user_list), 200
    
    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}),500
