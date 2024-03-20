# flask import 
import os
from flask import Flask, render_template
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from connectors.mysql_connectors import engine

# controller import 
from controller.User_management import user_routes
from controller.Account_management import account_routes
from controller.Transaction_management import transaction_routes
from controller.Register_user import register_routes
from controller.Login_User import Login_routes
# flask login import 
from flask_login import LoginManager
from models.User import Users



# call function to load env 
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')


# login manager
login_manager = LoginManager()
login_manager.init_app(app)

# user loader manager
@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(Users).get(int(user_id))



app.register_blueprint(user_routes)
app.register_blueprint(account_routes)
app.register_blueprint(transaction_routes)
app.register_blueprint(register_routes)
app.register_blueprint(Login_routes)

@app.route("/")
# def Running_server():
#     return 'server running at port 5000'
def landing_page():
    return render_template('landing/landing_page.html')
