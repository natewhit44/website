from flask import Blueprint, redirect, flash, url_for, request, render_template
from flask_login import login_user, current_user, logout_user, login_required
from flask.templating import render_template
from server import db, bcrypt
from server.models import User, Post
from server.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from server.users.utils import save_picture, send_reset_email

# Initialize blueprint
users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Initialize form object
    form = RegistrationForm()

    # Validate form POST
    if form.validate_on_submit():
        # Hash user password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Create new user
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        # User feedback message
        flash('Your account has been created! You are able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Initialize form object
    form = LoginForm()

    # Validate form POST
    if form.validate_on_submit():
        # Check DB to see if user exists
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Login user
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Initialize form object
    form = UpdateAccountForm()

    # Validate form POST
    if form.validate_on_submit():
        # Check for user logo data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        # Grab new user values from form
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Commit changes to DB
        db.session.commit()

        # Feedback message to user
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    # If page is loading (e.g. GET request) then display DB values
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Set user image file
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    # Get user from DB
    user = User.query.filter_by(username=username).first_or_404()

    # Set first page as default
    page = request.args.get('page', 1, type=int)

    # Grab sorted posts from DB
    posts = Post.query\
        .filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)

    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Initialize form object
    form = RequestResetForm()

    # Validate form POST
    if form.validate_on_submit():
        # Get user data
        user = User.query.filter_by(email=form.email.data).first()

        # Send user an email with token
        send_reset_email(user)

        # Feedback message to user
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Validate token
    user = User.verify_reset_token(token)

    # Provide feedback for non-valid token
    if user is None:
        flash('You provided and invalid or expired token...', 'warning')
        return redirect(url_for('resent_request'))

    # Initialize form object
    form = ResetPasswordForm()

    # Validate form POST
    if form.validate_on_submit():
        # Hash user password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Update user password
        user.password = hashed_pw
        db.session.commit()

        # User feedback message
        flash('Your password has been updated! You are able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)