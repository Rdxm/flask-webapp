import os
from flask import render_template, url_for, redirect, flash, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Post
from flaskblog import app, bcrypt, db, mail
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from PIL import Image
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page =  request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash('Logged In Successfully', 'green')
			return redirect(url_for('home'))
		else:
			flash('Log In unsuccessful', 'red')
	return render_template("login.html", form=form)

@app.route("/signup", methods=['GET','POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=pwd)
		db.session.add(user)
		db.session.commit()
		flash('Account created successfully!', 'green')
		return redirect(url_for('login'))
	return render_template("signup.html", form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	prev_picture = os.path.join(app.root_path, 'static/img', current_user.image_file)
	if os.path.exists(prev_picture):
		os.remove(prev_picture)
	picture_path = os.path.join(app.root_path, 'static/img', picture_fn)

	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file	
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Account Updated successfully", 'green')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='img/'+current_user.image_file)
	return render_template("account.html", image_file=image_file, form=form)


@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Post has been created !', 'green')
		return redirect(url_for('home'))
	return render_template("new_post.html", form=form, legend="Create New Post")

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', post=post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash("Post Updated Successfully !", 'green')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template("new_post.html", form=form, legend="Update Post")

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Post deleted Successfully !", 'green')
	return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    page =  request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("user_post.html", posts=posts, user=user)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset request', sender='noreply@demo.com', recipients=[user.email])
	msg.body = f'''To reset your password , visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request please ignore this email.
'''
	mail.send(msg)

@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("An email has been sent with instructions to reset password", 'blue')
		return redirect(url_for('login'))
	return render_template("reset_request.html", form=form)

@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash("Invalid/Expired Token", 'red')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = pwd
		db.session.commit()
		flash('Pasword Updated successfully!', 'green')
		return redirect(url_for('login'))
	return render_template('reset_token.html', form=form)


