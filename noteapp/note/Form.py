from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,ValidationError,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from noteapp.models import User




class NoteForm(FlaskForm):
    title=StringField("Title",validators=[DataRequired(),Length(min=1,max=200)])
    content=TextAreaField("Content",validators=[DataRequired()])
    submit=SubmitField("Add Note")


class ResetRequestForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    submit=SubmitField("Reset Password")
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email.You must register first.")
        
class ResetPasswordForm(FlaskForm):
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Reset Password")
    



