from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from application.models.general import User


# The registration form
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={'placeholder': 'Name'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Sign up')

    # If a user already exists with that email, then throw an error
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


# The login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# A form to send a password reset email to the specified email address
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send password reset email')


# A form to change the password of a user
class ChangePasswordForm(FlaskForm):
    password = PasswordField('New password', validators=[DataRequired()])
    submit = SubmitField('Change password')


# A form to send the confirmation email
class ConfirmAccountForm(FlaskForm):
    submit = SubmitField('Resend confirmation email')
