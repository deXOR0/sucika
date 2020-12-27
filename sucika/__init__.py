from flask import Flask  # Basic flask dependecies
from flask_sqlalchemy import SQLAlchemy  # Database connection and ORM
from flask_bcrypt import Bcrypt  # Hashing and CSRF token
from flask_login import LoginManager  # Login Manager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import configure_uploads, DATA, UploadSet
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '1cc02622ded9f82327f6dc502f611ed3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sucika.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_CSV_DEST'] = f'{__name__}/static/uploads'

cwd = os.getcwd()
upload_directory = os.path.join(cwd, app.config['UPLOADED_CSV_DEST'])

csv = UploadSet('csv', DATA)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

configure_uploads(app, csv)
manager.add_command('db', MigrateCommand)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# Uncomment the two lines below to implement default login page
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from sucika import routes  # import routes to be used with the web page