from models_new import *
from sqlalchemy import create_engine, MetaData, Table
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:database@cuibono.io/cuibono"
db = SQLAlchemy(app)

