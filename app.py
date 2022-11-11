import subprocess
from multiprocessing import Process
from speechrecognition import micon
from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm,LoginForm
import os
from main import get_images
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin,logout_user,login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LogRecord.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager(app)
stylefolder = os.path.join('static','styless')
app.config['UPLOAD_FOLDER']=stylefolder


@login_manager.user_loader
def load_user(user_id):
    return Candidate.query.get(int(user_id))

class Logged(db.Model):
    S_no = db.Column(db.Integer(), primary_key=True)
    Log_time = db.Column(db.String(length=20), nullable=False)
    description = db.Column(db.String(length=20), nullable=False)

    def __repr__(self):
        return f'{self.S_no}'

class answers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    answer = db.Column(db.String(length=100), nullable=False)


class Candidate(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


@app.route('/')
def home():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'],'pic1.png')
    logo = os.path.join(app.config['UPLOAD_FOLDER'],'logo.svg')
    logo2 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo2.svg')
    return render_template('proj1.html',pic1 = pic1,logo= logo,logo2=logo2)


@app.route('/logg')
def logg():
    items = Logged.query.all()
    print(type(items))
    return render_template('logg.html', items=items)


@app.route('/register',methods = ['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Candidate(username=form.username.data,
                                   email_address=form.email_address.data,
                                   password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successully! You are now logged in as {user_to_create.username}',category='success')
        return redirect(url_for('dashboard_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Candidate.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash('Successfully Logged in!',category='success')
            return redirect(url_for('dashboard_page'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!!!",category='info')
    return redirect(url_for("home"))

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/eventlog')
def logger():
    return render_template('logg.html')

@app.route('/testenv')
def disclamer_page():
    return render_template('testenv.html')

@app.route("/exam", methods=["GET", "POST"])
def give_exam():
    get_images()
    transcript = ""

    if request.method == "POST":
        print("FORM DATA RECEIVED")
        x,y= micon(1,5)
        add_answer = answers(answer= x)
        db.session.add(add_answer)
        db.session.commit()
    else:
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    #p1 = Process(target=
    app.run(debug=False)
