import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login.utils import current_user
from flask_mail import Message
from server import mail


def save_picture(form_picture):
    # Create random hash based on filename
    random_hex = secrets.token_hex(8)

    # Extract file extension
    _, f_ext = os.path.splitext(form_picture.filename)

    # Combine hash and file extension
    picture_fn = random_hex + f_ext

    # Create path to image file
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Resize image to save space
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Save image
    i.save(picture_path)

    # Delete old image
    if current_user.image_file != 'default.jpg':
        delete_picture()
    return (picture_fn)

def delete_picture():
    # Create path to old image file
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)

    # Delete old image file
    os.remove(picture_path)

def send_reset_email(user):
    # Get token
    token = user.get_reset_token()

    # Prepare email
    msg = Message('Password Reset Request',
                  sender='natewhit44@gmail.com',
                  recipients=[user.email])

    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

The generated token for the password reset process is only valid for 30 minutes.
If you did not make this request then simply ignore this email and no changes will be made.
'''
    # Send email
    mail.send(msg)