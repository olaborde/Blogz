from flask import request, redirect, render_template, url_for, session, flash
from main import app, db, bcrypt
from main.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from main.forms import SignupForm, LoginForm

posts = [
    {
        'author': 'Luke Bloomberg',
        'title': 'How to become a Ninja',
        'content': 'Practice nunchucking daily, high every 30 mins intervals',
        'date_posted': 'October 22, 2017'

    },
    {
        'author': 'Donatella Simpson',
        'title': 'Fashion on the runway',
        'content': 'skinny models should with thicker models',
        'date_posted': 'April 17, 2018'

    },
    {
        'author': 'Lance King',
        'title': 'My love for basketball',
        'content': 'Basketball has past past down to me from my great grand-father to my grand-father, and my father and now me',
        'date_posted': 'Decmber 25, 2017'

    }

]


app.secret_key = 'a5207b5ef037e30c70c59d2f339cedb2'


@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    error = None

    form = SignupForm()

    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pass)
        db.session.add(user)
        db.session.commit()


        flash(f'{form.username.data} account have been created!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form, title='Signup', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index')) #ternary condition if else

        else:
            flash('It is not Happening today, check your username or password', 'danger')

    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account')
@login_required
def account():
    
    return render_template('account.html', title='Account')
