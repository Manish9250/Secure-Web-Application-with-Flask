# __init__ file initialises the program, needed to complete a package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.app_context().push() # Direct access to other modules
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gun_market.db" # connecting to database
app.config["SECRET_KEY"] = "123456"
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view= "login"
login_manager.login_message_category="info"

from backend import routes # Routes also initialized    


