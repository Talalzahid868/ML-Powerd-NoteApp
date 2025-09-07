from noteapp.Form import RegistrationForm,LoginForm,NoteForm
from flask import render_template,url_for,flash,redirect,request
from noteapp import app,bcrypt,db
from noteapp.models import User,Note
from flask_login import login_user,current_user,logout_user,login_required
from noteapp.ml_utils import auto_tag,extract_keywords,generate_summary


@app.route("/")
@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('login Unsuccessful.Please check email and password','danger')
    return render_template('login.html',title='login',form=form)       

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login')) 

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("account.html",title='Account',notes=notes)

@app.route("/home")
@login_required
def home():
    # notes=Note.query.all()
    notes=Note.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html",notes=notes)

@app.route("/add",methods=['GET','POST'])
@login_required
def add_note():
    form=NoteForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        category=auto_tag(content)
        keywords=extract_keywords(content)
        summary=generate_summary(content)
        note=Note(title=title,content=content,category=category,keywords=','.join(keywords),summary=summary,user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        flash('Note added successfully',"success")
        return redirect(url_for('view_note',note_id=note.id))
    return render_template("add_note.html",title="Add Note",form=form)

@app.route("/note/<int:note_id>")
@login_required
def view_note(note_id):
    note=Note.query.get_or_404(note_id)
    if note.author!=current_user:
        flash("You don't have permission to view this note.","danger")
        return redirect(url_for('home'))
    return render_template("view_note.html",note=note)


@app.route("/note/<int:note_id>/delete",methods=['POST'])
@login_required
def delete_note(note_id):
    note=Note.query.get_or_404(note_id)
    if note.author!=current_user:
        flash("You don't have permission to delete this note.","danger")
        return redirect(url_for('home'))
    db.session.delete(note)
    db.session.commit()
    flash("Note has been deleted!","success")
    return redirect(url_for('home'))


