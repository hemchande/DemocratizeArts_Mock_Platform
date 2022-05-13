from flask import Flask, redirect, url_for, render_template, request, url_for, redirect, flash, abort, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, Length, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import datetime


app = Flask(__name__)

# setting configuration settings
app.config['SECRET_KEY'] = "my super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///root:password123@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initialize database
db = SQLAlchemy(app)

#create models

class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(15), nullable = False, unique = True)
    name = db.Column(db.String(200), nullable = False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)


class Instructors(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable = False, unique=True)
    email = db.Column(db.String(50), nullable = False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return "<Name %r>" % self.name

class UserForm(FlaskForm):
    name = StringField("Type your name", validators = [DataRequired()])
    email = StringField("Type your name", validators = [DataRequired()])
    submit = SubmitField("Submit")


class NameForm(FlaskForm):
    name = StringField("Type your name", validators = [DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(
        min=4)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

    def validate_username(self, username):
        username = Students.query.filter_by(username=username.data).first()
        if not username:
            raise ValidationError('Account does not exist.')








login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"







@app.route('/')
def index():
    first_name = "Eisha"
    text = "this <strong>Bold</strong>"
    return render_template("index.html", first_name = first_name, text = text )




@app.route('/student/add',methods = ['GET', 'POST'])
def add_student():
    name = None
    #email = None
    form = UserForm()
    if form.validate_on_submit():
        user = Students.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Students(name = form.name.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("New Student Added")
    current_students = Students.query.order_by(Students.date_added)
    return render_template("add_user.html", current_students = current_students)

@app.route('/instructors/add',methods = ['GET', 'POST'])
def add_student():
    name = None
    #email = None
    form = UserForm()
    if form.validate_on_submit():
        user = Instructors.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Instructors(name = form.name.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("New Instructor Added")
    current_instructors = Students.query.order_by(Students.date_added)
    return render_template("add_user.html", current_instructors = current_instructors)

@app.route('/user/<name>')
def greet(name):
    return render_template("user.html")

#creating custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.route('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NameForm()

    return render_template("name.html", name = name, form = form)



@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500




app.run(debug=True)



