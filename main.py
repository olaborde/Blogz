from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from form import signupForm, loginForm



app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


app.secret_key = 'development-key'



class User(db.Model):

    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(120))
    lastname  = db.Column(db.String(120))
    email     = db.Column(db.String(120), unique=True)
    pwdhash   = db.Column(db.String(60))
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')


    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)
     
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
        


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # publisher = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_posted = db.Column(db.DateTime)
  

    def __init__(self,title, description, user_id, date_posted):
        # self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.date_posted = datetime.now()

blogs = []

@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()

    # if request.method == 'POST':
    #     blog = request.form['blog']
    #     blogs.append(blog)

    return render_template('index.html', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if 'email' not in session:
        return redirect(url_for('login'))


    return render_template('newpost.html')
@app.route('/addpost', methods=['POST', 'GET'])
def addpost(): 
    title = request.form['title']
    description = request.form['description']
    # publisher = request.form['publisher']
    user_id = request.form['publisher']
    blog_entry = Blog(title=title, description=description, user_id=user_id, date_posted=datetime.now())
    db.session.add(blog_entry)
    db.session.commit()

    return redirect(url_for('index'))   

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).one()
    date_posted =blog.date_posted.strftime('%B %d, %Y')
    return render_template('blog.html', blog=blog, date_posted=date_posted)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('index'))

    error = None
  # password = request.form.get['password']
  # vpassword = request.form.get['vpassword']
 
    form = signupForm() 
  
    if request.method == 'POST':
        if form.validate == False:
            return render_template("user-signup.html", form=form)
        else:
            if request.form['password'] != request.form['vpassword']:
                flash('Passwords must match!')
                return redirect(url_for('signup'))
            elif len(request.form['password']) < 3 or len(request.form['password']) > 20:
                flash('password must between 3 or 20 characters!')
                return redirect(url_for('signup'))
            elif ' ' in (request.form['password']).strip() == True:
                flash('No spaces allowed!')
                return redirect(url_for('signup'))
            elif ' ' in (request.form['user_name']).strip() == True:
                flash('No spaces allowed in username!')
                return redirect(url_for('signup'))
            elif len(request.form['user_name']) < 3 or len(request.form['user_name']) > 20:
                flash('username must between 3 or 20 characters!')
                return redirect(url_for('signup')) 
            else: 
                newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()

                session['email'] = newuser.email
                return redirect(url_for('index'))      
    elif request.method == 'GET':   
        return render_template("user-signup.html", form=form, error=error)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('index'))

    form = loginForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('index'))  
            else: 
                return redirect(url_for('login')) 
    elif request.method == 'GET':            
        return render_template('login.html', form=form)
@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

    
