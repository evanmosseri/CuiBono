from models_new import *
from sqlalchemy import create_engine, MetaData, Table
from flask.ext.sqlalchemy import SQLAlchemy
from ast import literal_eval

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:database@cuibono.io/cuibono"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# legs = db.session.query(Legislator).all()


# for leg in legs:
	# print(json.loads(leg.sources)[0])
	# print(leg.server)
	# try:
	# 	leg.sources = json.dumps(list(literal_eval(leg.sources)))
	# except:
	# 	leg.sources = []
	# try:
	# 	leg.offices = json.dumps(list(literal_eval(leg.offices)))
	# except:
	# 	leg.offices = []

# db.session.commit();

bills = db.session.query(Bill).all()
for bill in bills:
	try:
		bill.sources = json.dumps(list(literal_eval(bill.sources)))
	except:
		bill.sources = []
	try:
		bill.subjects = json.dumps(list(literal_eval(bill.subjects)))
	except:
		bill.subjects = []
	try:
		bill.sponsors_meta = json.dumps(list(literal_eval(bill.sponsors_meta)))
	except:
		bill.sponsors_meta = []
	db.session.commit()
	print(bill.id)