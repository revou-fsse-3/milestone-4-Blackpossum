from flask import Blueprint,render_template,request,redirect,jsonify
from connectors.mysql_connectors import engine,sessionmaker
from sqlalchemy import select,or_
from models.User import Users
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token

register_routes = Blueprint('register_routes',__name__)

# 
@register_routes.route("/register", methods=['GET'])
def user_register():
    return render_template("user/register.html")

@register_routes.route("/register", methods=['POST'])
def do_registration():
        
    username = request.form['name']
    email = request.form['email']
    password_hash = request.form['password']
    newUser = Users(username=username, email=email)
    newUser.set_password(password_hash)

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()

    try:
        session.add(newUser)
        session.commit()
    except Exception as e:
        session.rollback()
        return {"message":"user registration failure"},500
    
    return {"message":"user register succesfully,continue to login"},201