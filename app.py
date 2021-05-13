"""Blogly application."""

from flask import Flask, redirect, render_template,request
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bloglyapp'

connect_db(app)
db.create_all()

@app.route("/")
def show_home():
   
    return render_template('home.html')

@app.route('/users')
def show_users():
     users = User.query.all()
     return render_template('users.html', users = users)

@app.route("/add_new")
def show_form():
    return render_template('new_user.html')

@app.route("/add_new", methods = ['POST'])
def make_new_user():
    first = request.form['first']
    last = request.form['last']
    img = request.form['img']

    new_user = User(first_name = first, last_name = last, image_url = img)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route("/user/<int:user_id>")
def show_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user = user)

@app.route('/user/<int:user_id>/edit')
def edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user = user)

@app.route('/user/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['img']
    db.session.commit()
    return redirect('/users')


@app.route("/user/<int:user_id>/delete", methods = ['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/user/<int:user_id>/new-post')
def show_new_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user = user)

@app.route('/user/<int:user_id>/new-post', methods=['POST'])
def submit_post(user_id):
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)
    post = Post(title = title, content = content, user_id = user.id)
    db.session.add(post)
    db.session.commit()
    return render_template('posts.html', user = user, post = post)

@app.route('/user/<int:user_id>/<int:post_id>')
def show_post(user_id,post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', user = user, post = post)

@app.route('/user/<int:user_id>/<int:post_id>/edit')
def show_edit_form(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post = post, user= user)

@app.route('/user/<int:user_id>/<int:post_id>/edit', methods = ['POST'])
def edit_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    # new_post = [post.title, post.content]
    # db.session.add(new_post)
    db.session.commit()
    return redirect('/user/<int:user_id>/<int:post_id>')
@app.route('/user/<int:user_id>/<int:post_id>', methods = ['POST'])
def delete_post(user_id,post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/user/<int:user_id>')

@app.route('/user/<int:user_id>/new-tag')
def tag_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('create_tag.html', user = user)

@app.route('/user/<int:user_id>/new-tag', methods=['POST'])
def make_tag(user_id):
    user = User.query.get_or_404(user_id)
    name = request.form['name']
    tag = Tag(name = name)
    db.session.add(tag)
    db.session.commit()
    return redirect('/user/<int:user_id>')









