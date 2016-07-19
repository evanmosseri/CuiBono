from models_new import *
from sqlalchemy import create_engine, MetaData, Table
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:database@cuibono.io/cuibono"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

sources = db.session.query(Legislator).get("TXL000201").sources.replace("\"",'\'')

print(type(sources))

