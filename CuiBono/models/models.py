from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Bill(db.Model):
	__tablename__ = "bill"
	id = db.Column(db.Integer,primary_key=True)
	leg_session = db.Column(db.String(10))
	type = db.Column(db.String(32))
	number = db.Column(db.Integer)
	text = db.Column(db.Text(10000000))
	authors = db.relationship("legislator",backref="author")
	sponsors = db.relationship("legislator",backref="sponsor")



class Legislator(db.Model):
	__tablename__ = "legislator"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	filer_id = db.Column(db.Integer)
	bio = db.Column(db.String(100000))
	party = db.Column(db.String(128))
	district = db.Column(db.Integer)
	contributors = db.ForeignKey()
	bills = db.ForeignKey()

class Contributor(db.Model):
	__tablename__ = "contributor"
	id = db.Column(db.Integer,primary_key=True)
	type = db.Column(db.String(16))
	name = db.Column(db.String(256))
	zipcode = db.Column(db.String(32))

class Contribution(db.Model):
	__tablename__ = "contribution"
	id = db.Column(db.Integer,primary_key=True)
	amount = db.Column(db.Integer)
	date_contributed = db.Column(db.Date)
	contributor = db.ForeignKey("contributor",backref="contribution")
	legislator = db.ForeignKey("legislator",backref="contribution")