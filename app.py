from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '4ee9ee6f97edadd4dc2cb968045adafc'

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
			flash('Loggen In Successfully', 'green')
			return redirect(url_for('home'))
		else:
			flash('Log In unsuccessful', 'red')
	return render_template("login.html", form=form)

@app.route("/signup", methods=['GET','POST'])
def signup():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash('Account created successfully!', 'red')
		return redirect(url_for('home'))
	return render_template("signup.html", form=form)

if __name__ == "__main__":
	app.run(debug=True)