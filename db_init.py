from sqlalchemy import inspect


def init_db(app, db):
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        if not tables:
            print("No tables found, creating database tables...")
            db.create_all()
        else:
            print("Database tables already exist.")