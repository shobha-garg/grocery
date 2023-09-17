import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration:
    DEBUG=False
    SECRET_KEY='MnazCITmL0PgGb1l4VVczxKzQ5ulWgx3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project_db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
