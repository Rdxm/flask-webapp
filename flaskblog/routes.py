from flask import render_template, url_for, redirect, flash
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required

posts = [
	{
		"title": "I dont know how a long title looks like? so i am just type the same question as long title",
		"content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Error deserunt dicta obcaecati iusto accusamus, magnam, molestias molestiae at. Blanditiis, earum aperiam ex vero adipisci. Voluptatibus!",
		"author": "Rahul Chaudhary",
		"date_posted": "13 Feb 2021"
	},
	{
		"title": "Second Post",
		"content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Error deserunt dicta obcaecati iusto accusamus, magnam, molestias molestiae at. Blanditiis, earum aperiam ex vero adipisci. Voluptatibus!",
		"author": "Rdxmax",
		"date_posted": "13 Feb 2021"
	},
	{
		"title": "Second Post",
		"content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Error deserunt dicta obcaecati iusto accusamus, magnam, molestias molestiae at. Blanditiis, earum aperiam ex vero adipisci. Voluptatibus!",
		"author": "Rdxmax",
		"date_posted": "13 Feb 2021"
	},
	{
		"title": "Second Post",
		"content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Error deserunt dicta obcaecati iusto accusamus, magnam, molestias molestiae at. Blanditiis, earum aperiam ex vero adipisci. Voluptatibus!",
		"author": "Rdxmax",
		"date_posted": "13 Feb 2021"
	}
]

@app.route("/")
@app.route("/home")
def home():
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

@app.route("/account")
@login_required
def account():
	return render_template("account.html")
