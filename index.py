from flask import Flask
from dotenv import load_dotenv

from controller.User_management import user_routes



# call function to load env 
load_dotenv()

app = Flask(__name__)

app.register_blueprint(user_routes)

@app.route("/")
def Running_server():
    return 'server running at port 5000'

