from functools import wraps
from hashlib import sha256
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from application import app, bcrypt, serializer, mail
from application.models.general import *
from application.forms.general import *
from application.settings_secrets import *


# Create a decorator function
def abort_not_confirmed(f):
    # When this function is used as a decorator, the @wraps calls the decorator
    # function with the function below the decorator as the parameter "f", and any
    # arguments and keyword arguments are also passed in and can be passed to the
    # original function as well
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_user.is_authenticated and not current_user.confirm:
            return redirect(url_for('confirm_account'))

        return f(*args, **kwargs)

    # If the function is used as a decorator, then return
    # the decorator function which will be called
    return decorator


@app.context_processor
def send_sha_function():
    return {'sha256': sha256, 'serializer': serializer}


# Log the user out
@app.route('/logout')
def logout():
    # If the user is not logged in or have not confirmed their email, don't log them out
    if not current_user.is_authenticated:
        abort(404)

    if not current_user.confirm:
        abort(404)

    logout_user()
    return redirect(url_for('home'))


# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # If the user is already logged in, redirect to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Create form using Flask-WTF
    form = RegistrationForm()

    # If form was submitted successfully, create a user and redirect to confirm account page
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)

        # Resend confirmation email, if there was an error, say so
        try:
            send_confirmation_email()
        except:
            flash('There was an error sending a confirmation email.', 'danger')

        return redirect(url_for('login'))

    return render_template('account/register.html', form=form, page_title='Register')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Create form using Flask-WTF
    form = LoginForm()

    # If the form has been successfully submitted
    if form.validate_on_submit():

        # Check if the user exists and whether the bcrypt hash of the input and the user's hash match
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # Log the user in and redirect to the dashboard if there is not "?next=" parameter in the URL
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home')) if not request.args.get('next') else redirect(
                request.args.get('next'))

        # Flash that the login was unsuccessful (Flash is an in-built
        # Flask tool that sends messages which can be retrieved on the HTML page)
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
    return render_template('account/login.html', form=form, page_title='Login')


# A route to send a password reset email in case the user forgets their password
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    # If the user is logged in, abort with 404 code
    if current_user.is_authenticated:
        abort(404)

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = serializer.dumps(user.email, salt=SECRET_KEY + 'reset')
            mail.send_message(subject='Reset your password.',
                              body=f'Click on the below link to reset your password\n{url_for("forgot_password_token", token=token, _external=True)}',
                              recipients=[user.email])
        flash('An email has been sent to reset your password if the user exists.', 'info')
        return redirect(url_for('forgot_password'))

    return render_template('account/forgot-password.html', form=form, page_title='Forgot password')


# A route to change a user's password based on the token that was sent to their email
@app.route('/forgot-password/<token>', methods=['GET', 'POST'])
def forgot_password_token(token):
    # If the user is logged in, abort with 404 code
    if current_user.is_authenticated:
        abort(404)

    # Get the user's email based on the serializer's value
    try:
        user = User.query.filter_by(
            email=serializer.loads(token, salt=SECRET_KEY + 'reset', max_age=7200)).first()
    # If there was an issue, that means the token was incorrect, then abort with 404
    except:
        abort(404)

    # Initialize the form
    form = ChangePasswordForm()

    # If the form validated, then generate a password hash,
    # change the user's password, then let the user know
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been changed.', 'success')
        return redirect(url_for('login'))

    # Show the HTML page
    return render_template('account/change-password.html', form=form, page_title='Change your password')


# A route to confirm the user's account
@app.route('/confirm-account', methods=['GET', 'POST'])
def confirm_account():
    # If the user is not logged in or the user has already confirmed, then return
    if not current_user.is_authenticated:
        abort(404)

    if current_user.confirm:
        return redirect(url_for('home'))

    # Create the form which allows resending confirmation emails
    form = ConfirmAccountForm()

    # If the form was validated, generate a timed token, then send the message and let the user know
    if form.validate_on_submit():

        # Resend confirmation email, if there was an error, say so
        try:
            send_confirmation_email()
        except:
            flash('There was an error sending a confirmation email.', 'danger')
            return redirect(url_for('confirm_account'))

        flash('The email has been sent to you.', 'success')

        return redirect(url_for('confirm_account'))

    return render_template('account/confirm-account.html', form=form, page_title='Confirm Account')


# Route to check a user's token
@app.route('/token/<token>')
def token(token):
    # If the user has already confirmed, abort with
    # 404, then if the user is logged in, log them out
    if current_user.is_authenticated:
        if current_user.confirm:
            abort(404)
        logout_user()

    # Load the token, then check if the emails match and set that the user has confirmed
    try:
        email = serializer.loads(token, salt=SECRET_KEY, max_age=7200)

        # Get the user from the token
        user = User.query.filter_by(email=email).first_or_404()

        # Log the user in
        login_user(user)

        # If the user has confirmed, abort with 404
        if user.confirm:
            abort(404)

        # Set the user's confirm attribute to True, then commit
        current_user.confirm = True
        db.session.commit()

        # Let the user know they have been confirmed
        flash('Your email has been confirmed.', 'success')
        return redirect(url_for('home'))

    # If there was an error while loading the token, return so
    except:
        return render_template('errors/token_expired.html'), 403


# Delete a user's account
@app.route('/delete-account/')
def delete_account():
    if not current_user.is_authenticated:
        abort(404)

    # Hash the same properties as was passed from the class page
    sha_hash_contents = sha256(
        f'{current_user.id}{current_user.email}{current_user.password}'.encode('utf-8')).hexdigest()

    # if the hashes don't match, don't delete the account
    if sha_hash_contents != request.args.get('hash'):
        return render_template('errors/token_expired.html'), 403

    # Get the user and delete the account
    user = User.query.filter_by(id=current_user.id).first()

    logout_user()

    db.session.delete(user)
    db.session.commit()

    flash('Your account has been deleted.', 'success')

    return redirect(url_for('register'))


def send_confirmation_email():
    token = serializer.dumps(current_user.email, salt=SECRET_KEY)
    mail.send_message(subject='Your Confirmation Email',
                      body=f'Click on the below link to confirm your account\n{url_for("token", token=token, _external=True)}',
                      recipients=[current_user.email])
