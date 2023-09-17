from flask import Flask
from app.models.admin import db
from app.utils.config import Configuration as Config

app = Flask(__name__)
Config.DEBUG = True

app.config.from_object(Config)

# Initialize the database
db.init_app(app)

app.app_context().push()
db.create_all()

from app.controllers.user import *
from app.controllers.admin import *

if __name__ == '__main__':
    
    app.run(debug=True)
