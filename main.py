from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from form import signupForm



app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


app.secret_key = 'development-key'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime)
  

    def __init__(self,title, description, publisher, date_posted):
        # self.id = id
        self.title = title
        self.description = description
        self.publisher = publisher
        self.date_posted = datetime.now()


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(120))
    lastname  = db.Column(db.String(120))
    email     = db.Column(db.String(120), unique=True)
    pwdhash   = db.Column(db.String(60))


    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)
     
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
        





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

    return render_template('newpost.html')
@app.route('/addpost', methods=['POST', 'GET'])
def addpost(): 
    title = request.form['title']
    description = request.form['description']
    publisher = request.form['publisher']
    blog_entry = Blog(title=title, description=description, publisher=publisher, date_posted=datetime.now())
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
  error = None
  # password = request.form.get['password']
  # vpassword = request.form.get['vpassword']
 
  form = signupForm() 
  
  if request.method == 'POST':
      if form.validate == False:
        return render_template("user-signup.html", form=form)
      else:
            if request.form['password'] != request.form['vpassword']:
                  # error = 'Password must match'
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
              return 'Welcome, ' + request.form['user_name']    
  elif request.method == 'GET':   
    return render_template("user-signup.html", form=form, error=error)




if __name__ == '__main__':
    app.run()

    
