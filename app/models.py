from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

#MANY TO MANY relationships

bill_legislator = db.Table('bill_legislator',
								db.Column('bill_id', db.Integer, db.ForeignKey('bill.id')),
								db.Column('legislator_id', db.Integer, db.ForeignKey('legislator.legislator_id')))

legislator_contributor = db.Table('legislator_contributor', 
    							db.Column('legislator_id', db.Integer, db.ForeignKey('legislator.legislator_id')),
    							db.Column('contributor_id', db.Integer, db.ForeignKey('contributor.contributor_id')))


# Bill has many-to-many relationship with Legislator seperated into authors and sponsors

class Bill(db.Model):
	__tablename__ = "bill"
	id = db.Column(db.Integer, primary_key=True)
	bill_id = db.Column(db.String, unique=True)
	leg_session = db.Column(db.String(10))
	type = db.Column(db.String(32))
	number = db.Column(db.Integer)
	aye_or_nay = db.Column(db.String(64))
	text = db.Column(db.Text(10000000))

	#authors = db.relationship("legislator", backref="author")
	#sponsors = db.relationship("legislator", backref="sponsor")

	#many-many
	legislators = db.relationship("Legislator", secondary=bill_legislator, back_populates="bills")


	def __init__(self, bill_id, leg_session, type, number, aye_or_nay, text):
		self.bill_id = bill_id
		self.leg_session = leg_session
		self.type = type
		self.number = number
		self.aye_or_nay = aye_or_nay
		self.text = text


	def serialize(self):
		return {
			"bill_id": self.id,
			"leg_session": self.leg_session,
			"type": self.type,
			"number": self.number,
			"aye_or_nay": self.aye_or_nay,
			"text": self.text
		}




# Legislator has many-to-many relationship with Bill and Contributor
# Legislator has one-to-many relationship with Contribution

class Legislator(db.Model):
	__tablename__ = "legislator"
	legislator_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	filer_id = db.Column(db.Integer)
	bio = db.Column(db.String(100000))
	party = db.Column(db.String(128))
	district = db.Column(db.Integer)

	#many-many
	bills = db.relationship("Bill", secondary=bill_legislator, back_populates="legislators")
	contributors = db.relationship("Contributor", secondary=legislator_contributor, back_populates="legislators")

	#1-many
	contributions = db.relationship('Contribution', backref='legislators', lazy='dynamic')


	def __init__(self, legislator_id, name, filer_id, bio, party, district):
		self.legislator_id = legislator_id
		self.name = name
		self.filer_id = filer_id
		self.bio = bio
		self.party = party
		self.district = district

	def serialize(self):
		return {
			"legislator_id": self.legislator_id,
			"name": self.name,
			"filer_id": self.filer_id,
			"bio": self.bio,
			"party": self.party,
			"district": self.district
		}



# Contributor has many-to-many relationship with Legislator
# Contributor has one-to-many relationship with Contribution

class Contributor(db.Model):
	__tablename__ = "contributor"
	contributor_id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(16))
	name = db.Column(db.String(256))
	zipcode = db.Column(db.String(32))

	#many-many
	legislators = db.relationship("Legislator", secondary=legislator_contributor, back_populates="contributors")

	#1-many
	contributions = db.relationship('Contribution', backref='contributor', lazy='dynamic')


	def __init__(self, contributor_id, type, name, zipcode):
		self.contributor_id = contributor_id
		self.type = type
		self.name = name
		self.zipcode = zipcode

	def serialize(self):
		return {
			"contributor_id": self.contributor_id,
			"type": self.type,
			"name": self.name,
			"zipcode": self.zipcode
		}


# Contribution has many-to-one relationship with Contributor and Legislator

class Contribution(db.Model):
	__tablename__ = "contribution"
	contribution_id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Integer)
	date_contributed = db.Column(db.Date)

	#many-1
	contributor_id = db.Column(db.Integer, db.ForeignKey('contributor.id'))
	legislator_id = db.Column(db.Integer, db.ForeignKey('legislator.id'))

	def __init__(self, contribution_id, amount, date_contributed):
		self.contribution_id = contribution_id
		self.amount = amount
		self.date_contributed = date_contributed

	def serialize(self):
		return {
			"contribution_id": self.contribution_id,
			"amount": self.amount,
			"date_contributed": self.date_contributed,
			"contributor_id": self.contributor_id,
			"legislator_id": self.legislator_id
		}