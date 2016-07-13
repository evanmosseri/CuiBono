from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base

#MANY TO MANY relationships
bill_legislator = Table('bill_legislator',
								Column('bill_id', Integer, ForeignKey('Bill.id')),
								Column('legislator_id', Integer, ForeignKey('Legislator.id')))

legislator_contributor = db.Table('legislator_contributor', 
    							Column('legislator_id', Integer, ForeignKey('Legislator.id')),
    							Column('contributor_id', Integer, ForeignKey('Contributor.id')))


# Bill has many-to-many relationship with Legislator seperated into authors and sponsors

class Bill(Base):
	__tablename__ = "bill"
	id = Column(Integer, primary_key=True)
	leg_session = Column(String(10))
	type = Column(String(32))
	number = Column(Integer)
	aye_or_nay = Column(String(64))
	text = Column(db.Text(10000000))

	#authors = relationship("legislator", backref="author")
	#sponsors = relationship("legislator", backref="sponsor")

	#many-many
	legislators = relationship("Legislator", secondary=bill_legislator, back_populates="bills")


	def __init__(self, id, leg_session, type, number, aye_or_nay, text):
		self.id = id
		self.leg_session = leg_session
		self.type = type
		self.number = number
		self.aye_or_nay = aye_or_nay
		self.text = text


	def serialize(self):
		return {
			"id": self.id,
			"leg_session": self.leg_session,
			"type": self.type,
			"number": self.number,
			"aye_or_nay": self.aye_or_nay,
			"text": self.text
		}




# Legislator has many-to-many relationship with Bill and Contributor
# Legislator has one-to-many relationship with Contribution

class Legislator(Base):
	__tablename__ = "legislator"
	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	filer_id = Column(Integer)
	bio = Column(String(100000))
	party = Column(String(128))
	district = Column(Integer)

	#many-many
	bills = relationship("Bill", secondary=bill_legislator, back_populates="legislators")
	contributors = relationship("Contributor", secondary=legislator_contributor, back_populates="legislators")

	#1-many
	contributions = relationship('Contribution', backref='legislators', lazy='dynamic')


	def __init__(self, id, name, filer_id, bio, party, district):
		self.id = id
		self.name = name
		self.filer_id = filer_id
		self.bio = bio
		self.party = party
		self.district = district

	def serialize(self):
		return {
			"id": self.id,
			"name": self.name,
			"filer_id": self.filer_id,
			"bio": self.bio,
			"party": self.party,
			"district": self.district
		}



# Contributor has many-to-many relationship with Legislator
# Contributor has one-to-many relationship with Contribution

class Contributor(Base):
	__tablename__ = "contributor"
	id = Column(Integer, primary_key=True)
	type = Column(String(16))
	name = Column(String(256))
	zipcode = Column(String(32))

	#many-many
	legislators = relationship("Legislator", secondary=legislator_contributor, back_populates="contributors")

	#1-many
	contributions = relationship('Contribution', backref='contributor', lazy='dynamic')


	def __init__(self, id, type, name, zipcode):
		self.id = id
		self.type = type
		self.name = name
		self.zipcode = zipcode

	def serialize(self):
		return {
			"id": self.id,
			"type": self.type,
			"name": self.name,
			"zipcode": self.zipcode
		}


# Contribution has many-to-one relationship with Contributor and Legislator

class Contribution(Base):
	__tablename__ = "contribution"
	id = Column(Integer, primary_key=True)
	amount = Column(Integer)
	date_contributed = Column(Date)

	#many-1
	contributor_id = Column(Integer, ForeignKey('Contributor.id'))
	legislator_id = Column(Integer, ForeignKey('Legislator.id'))

	def __init__(self, id, amount, date_contributed):
		self.id = id
		self.amount = amount
		self.date_contributed = date_contributed

	def serialize(self):
		return {
			"id": self.id,
			"amount": self.amount,
			"date_contributed": self.date_contributed,
			"contributor_id": self.contributor_id,
			"legislator_id": self.legislator_id
		}
