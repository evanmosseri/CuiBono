from models_new import *
from sqlalchemy import create_engine, MetaData, Table
from flask.ext.sqlalchemy import SQLAlchemy
from ast import literal_eval

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:database@cuibono.io/cuibono"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

legs = db.session.query(Legislator).all()


for leg in legs:
	print(type(leg.sources))
	print(leg.server)
	# try:
	# 	leg.sources = json.dumps(list(literal_eval(leg.sources)))
	# except:
	# 	leg.sources = []
	# try:
	# 	leg.offices = json.dumps(list(literal_eval(leg.offices)))
	# except:
	# 	leg.offices = []

# db.session.commit();
