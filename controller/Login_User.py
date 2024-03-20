from flask import Blueprint,render_template,request,redirect,jsonify
from connectors.mysql_connectors import engine,sessionmaker
from models.User import Users
from sqlalchemy import select,or_
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token

Login_routes = Blueprint('Login_routes', __name__)

@Login_routes.route("/login", methods=['GET'])
def user_login():
    return render_template("user/login.html")

@Login_routes.route("/login", methods=['POST'])
def do_user_login():
    # establish conncetion session
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    # initialize connection
    session.begin()

    try:
        # find / macthing inputed email on database by query 
        user = session.query(Users).filter(Users.email==request.form['email']).first()

        # conditinal if email doesnt exist 
        if user is None:
            return{"message":"email not match or doesnt exist"}
        
        # find / macthing inputed password on darabase by query
        if not user.check_password(request.form['password']):
            return {"message":"password not macth or doesnt exist"}
        # if login success, this function will save user data to session and created session_id to pass to browser and saved in browser cookie
        login_user(user, remember=False)
        return redirect('/users/me')

    except Exception as e:
        print(e)
        return {"message": "Login failure incorect user data"},401

@Login_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return redirect('/login')
