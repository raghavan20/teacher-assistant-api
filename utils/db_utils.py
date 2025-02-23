from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import inspect
import os

def create_db(app):
    # Read database configuration from environment variables, fallback to defaults
    db_user = os.getenv('DB_USER', 'user')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'teaching_db')

    # Construct the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    # Initialize SQLAlchemy and migration
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


