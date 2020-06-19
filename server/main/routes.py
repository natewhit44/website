from flask import Blueprint, render_template, request
from server.models import Post

# Initialize blueprint
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # Set first page as default
    page = request.args.get('page', 1, type=int)

    # Grab sorted posts from DB
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('home.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title='About')