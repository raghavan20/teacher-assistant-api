from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils import Registry

def create_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/teaching_db'
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    return db


