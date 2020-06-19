from flask_wtf.form import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from server.models import User

class RegistrationForm(FlaskForm):

    # Define form attributes
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    # Submit button
    submit = SubmitField('Sign Up')

    # Username validation
    def validate_username(self, username):
        # Check to see if user exists in DB
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Username already taken, please choose another username.')

    # Email validation
    def validate_email(self, email):
        # Check to see if email exists in DB
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already used, please provide another email.')

class LoginForm(FlaskForm):

    # Define form attributes
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    # Remember field
    remember = BooleanField('Remember Me')

    # Submit button
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):

    # Define form attributes
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    # Submit button
    submit = SubmitField('Update')

    # Username validation
    def validate_username(self, username):
        # Check to see if user is current user to ignore validation
        if username.data != current_user.username:
            # Check to see if user exists in DB
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError('Username already taken, please choose another username.')

    # Email validation
    def validate_email(self, email):
        # Check to see if user is current user to ignore validation
        if email.data != current_user.email:
            # Check to see if email exists in DB
            email = User.query.filter_by(email=email.data).first()

            if email:
                raise ValidationError('Email already used, please provide another email.')

class RequestResetForm(FlaskForm):

    # Define form attributes
    email = StringField('Email', validators=[DataRequired(), Email()])

    # Submit button
    submit = SubmitField('Request Password Reset')

    # Email validation
    def validate_email(self, email):
        # Check to see if email exists in DB
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError('There is account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):

    # Define form attributes
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    # Submit button
    submit = SubmitField('Reset Password')