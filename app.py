from datetime import datetime
from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '4ee9ee6f97edadd4dc2cb968045adafc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	email = db.Column(db.String(30), nullable=False, unique=True)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}')"

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
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'test@admin.com' and form.password.data == 'test':
			flash('Logged In Successfully', 'green')
			return redirect(url_for('home'))
		else:
			flash('Log In unsuccessful', 'red')
	return render_template("login.html", form=form)

@app.route("/signup", methods=['GET','POST'])
def signup():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash('Account created successfully!', 'green')
		return redirect(url_for('home'))
	return render_template("signup.html", form=form)

if __name__ == "__main__":
	app.run(debug=True)