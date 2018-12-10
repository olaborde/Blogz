from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from werkzeug import generate_password_hash, check_password_hash



app = Flask(__name__, static_url_path='/static')
# app = Flask(__name__)
app.config['DEBUG'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://oz509:FlaskBlog509@blogz305.cdcva0qeex0t.us-east-2.rds.amazonaws.com:3306/blogz305'
app.config['SQLALCHEMY_ECHO'] = True
app.config['QLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['WHOOSH_BASE'] = 'whoosh'
# database instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from main import routes
