from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import current_user,login_required
from noteapp.models import User,Note
from noteapp import app,bcrypt,db,mail
from noteapp.note.Form import NoteForm,ResetPasswordForm,ResetRequestForm
from noteapp.ml_utils import auto_tag,extract_keywords,generate_summary
from flask_mail import Message
import os

note=Blueprint('note',__name__)

@note.route("/add",methods=['GET','POST'])
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
        return redirect(url_for('note.view_note',note_id=note.id))
    return render_template("add_note.html",title="Add Note",form=form)

@note.route("/note/<int:note_id>")
@login_required
def view_note(note_id):
    note=Note.query.get_or_404(note_id)
    if note.author!=current_user:
        flash("You don't have permission to view this note.","danger")
        return redirect(url_for('main.home'))
    return render_template("view_note.html",note=note)


@note.route("/note/<int:note_id>/delete",methods=['POST'])
@login_required
def delete_note(note_id):
    note=Note.query.get_or_404(note_id)
    if note.author!=current_user:
        flash("You don't have permission to delete this note.","danger")
        return redirect(url_for('main.home'))
    db.session.delete(note)
    db.session.commit()
    flash("Note has been deleted!","success")
    return redirect(url_for('main.home'))

def sent_resent_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request',sender=os.environ.get('EMAIL_USER'),recipients=[user.email])
    msg.body=f'''To reset your password, visit the following link:
    {url_for('note.reset_token',token=token,_external=True)}
    if you did not make this request simply ingore it.
        '''
    mail.send(msg)

@note.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=ResetRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            sent_resent_email(user)
            flash('An email has been sent with instructions to reset your password.','info')
            return redirect(url_for('user.login'))
        else:
            flash('Email not found',"danger")
    return render_template('reset_request.html',title='Reset Password',form=form)  

@note.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user=User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid token ","warning")
        return redirect(url_for('note.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You can now log in.','success')
        return redirect(url_for('user.login'))
    return render_template('reset_token.html',title='Reset Password',form=form,token=token)




