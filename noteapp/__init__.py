from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)
app.config["SECRET_KEY"]="asasjdsk2323"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='user.login'
login_manager.login_message_category="info"


app.config["MAIL_SERVER"]='smtp.googlemail.com'
app.config["MAIL_PORT"]=587
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USERNAME"]=os.environ.get('EMAIL_USER')
app.config["MAIL_PASSWORD"]=os.environ.get('EMAIL_PASS')
mail=Mail(app)

from noteapp.main.routes import main
from noteapp.note.routes import note
from noteapp.user.routes import user
from noteapp.error.handler import errors

app.register_blueprint(main)
app.register_blueprint(note)
app.register_blueprint(user)
app.register_blueprint(errors)









