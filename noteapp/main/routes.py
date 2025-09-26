from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from noteapp.models import User,Note

main=Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    # notes=Note.query.all()
    notes=Note.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html",notes=notes)




