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
    tag = Tag.query.all()

    return render_template('users.html', users = users, tag = tag)

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
    tag = Tag.query.all()
    return render_template('post_form.html', user = user, tag = tag)

@app.route('/user/<int:user_id>/new-post', methods=['POST'])
def submit_post(user_id):
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)
    tag = [int(tagint) for tagint in request.form.getlist('tags')]
    post = Post(title = title, content = content, user_id = user.id)
    db.session.add(post)
    db.session.commit()
    for tags in tag:
        tag_num = tags
    
    
        combine = PostTag(post_id = post.id, tag_id = tag_num)
        db.session.add(combine)
    
    
    db.session.commit()
    return redirect('/user/<int:user_id>/<int:post_id>')

@app.route('/user/<int:user_id>/<int:post_id>')
def show_post(user_id,post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    combine = PostTag.query.filter_by(post_id = post.id)
    return render_template('posts.html', user = user, post = post, combine = combine)

@app.route('/user/<int:user_id>/<int:post_id>/edit')
def show_edit_form(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tag = Tag.query.all()

    return render_template('post_edit.html', post = post, user= user,tag = tag)

@app.route('/user/<int:user_id>/<int:post_id>/edit', methods = ['POST'])
def edit_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    # new_post = [post.title, post.content]
    # db.session.add(new_post)
    tag = [int(tagint) for tagint in request.form.getlist('tags')]

    for tags in tag:
        PostTag.tag_id = tags    
        db.session.commit()

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

@app.route('/<int:tag_id>')
def show_tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = PostTag.query.filter_by(tag_id = tag_id)
    # user = User.query.filter_by(posts = posts)
    return render_template('tag_details.html', tag = tag, posts = posts)

@app.route('/<int:tag_id>/edit')
def tag_edit_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag = tag)

@app.route('/<int:tag_id>/edit', methods = ['POST'])
def update_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['title']
    db.session.commit()
    return redirect('/users')

@app.route("/<int:tag_id>/delete", methods = ['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/users')





