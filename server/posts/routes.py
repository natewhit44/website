from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from server import db
from server.models import Post
from server.posts.forms import PostForm

# Initialize blueprint
posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    # Initialize form object
    form = PostForm()

    # Validate form POST
    if form.validate_on_submit():
        # Store post data
        post = Post(title=form.title.data, content=form.content.data, author=current_user)

        # Add post to DB
        db.session.add(post)
        db.session.commit()

        # Feedback message to user
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    # Try to query a post from DB
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # Try to query a post from DB
    post = Post.query.get_or_404(post_id)

    # Check to ensure author is current user
    if post.author != current_user:
        abort(403)

    # Initialize post form
    form = PostForm()

    # Validate form POST
    if form.validate_on_submit():
        # Update DB fields w/ new values
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        # Feedback message to user
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    elif request.method == 'GET':
        # Populate form w/ current form data
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', post=post, form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    # Try to query a post from DB
    post = Post.query.get_or_404(post_id)

    # Check to ensure author is current user
    if post.author != current_user:
        abort(403)

    # Delete post and return to home
    db.session.delete(post)
    db.session.commit()

    # Feedback message to user
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))