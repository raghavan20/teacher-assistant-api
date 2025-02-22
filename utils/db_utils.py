from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import inspect
from utils.utils import Registry


def create_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/teaching_db'
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    return db


def init_db(app, db):
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        if not tables:
            print("No tables found, creating database tables...")
            db.create_all()
        else:
            print("Database tables already exist.")


