from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import create_engine
import json
from pprint import pprint
import pandas as pd
import numpy as np
import ast

app = Flask(__name__)
engine = create_engine("sqlite:///myapp.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///testdb"
db = SQLAlchemy(app)
shared_dir = "../data-shared"

# class Test(db.Model):
# 	id = db.Column(db.INTEGER,primary_key=True)
# 	name = db.Column(db.String(80))
def get_keys(da,keys):
	return {k:v for k,v in da.items() if ((k in keys) and (k in da))}


sponsors = db.Table('sponsors',
							db.Column("bill_id", db.String, db.ForeignKey("bill.id")),
						    db.Column("legislator_id", db.String, db.ForeignKey("legislator.id")))

# legislator_contributor = db.Table('legislator_contributor',
# 								  db.Column('legislator_id', db.String, db.ForeignKey("legislator.id")),
# 								  db.Column('contributor_id'), db.String, db.ForeignKey("contributor.id"))

class Legislator(db.Model):
	id = db.Column(db.String(15),primary_key=True)
	filer_id = db.Column(db.INTEGER)
	sources = db.Column(JSON)
	offices = db.Column(JSON)
	first_name = db.Column(db.String(128))
	middle_name = db.Column(db.String(128))
	last_name = db.Column(db.String(128))
	district = db.Column(db.INTEGER)
	party = db.Column(db.String(32))
	photo_url = db.Column(db.String(512))
	# contributions = db.relationship('Contribution',backref="legislators")
	def __str__(self):
		return "Legislator: "+str(self.serialize())
	def __repr__(self):
		return "Legislator: "+str(self.serialize())
	def serialize(self):
		return get_keys(self.__dict__,[x for x in self.__dict__.keys() if not(x.startswith("_"))])


class Bill(db.Model):
	id = db.Column(db.String(15),primary_key=True)
	no_count = db.Column(db.INTEGER)
	no_votes = db.Column(JSON)
	yes_count = db.Column(db.INTEGER)
	yes_votes = db.Column(JSON)
	prefix = db.Column(db.String(8))
	number = db.Column(db.INTEGER)
	session = db.Column(db.String(5))
	sources = db.Column(JSON)
	sponsor_meta = db.Column(JSON)
	sponsors = db.relationship("Legislator", secondary=sponsors, backref=db.backref("bills", lazy="dynamic"))
	subjects = db.Column(JSON)
	title = db.Column(db.String(5026))
	def __str__(self):
		return "Bill: "+str(self.serialize())
	def __repr__(self):
		return "Bill: "+str(self.serialize())
	def serialize(self):
		return get_keys(self.__dict__,[x for x in self.__dict__.keys() if not(x.startswith("_"))])

class Contributor(db.Model):
	id = db.Column(db.INTEGER,primary_key=True)
	name = db.Column(db.String(512))
	type = db.Column(db.String(8))
	zip = db.Column(db.String(24))
	contributions = db.relationship('Contribution')
	def legislators(self):
		return list(map(lambda x: x.legislator,db.session.query(Contribution).filter(Contribution.contributor==self)))
	def __str__(self):
		return "Contributor: "+str(self.serialize())
	def __repr__(self):
		return "Contributor: "+str(self.serialize())
	def serialize(self):
		return get_keys(self.__dict__,[x for x in self.__dict__.keys() if not(x.startswith("_"))])

class Contribution(db.Model):
	id = db.Column(db.INTEGER,primary_key=True)
	amount = db.Column(db.FLOAT)
	filer_id = db.Column(db.INTEGER)
	submitted_date = db.Column(db.DateTime)
	contributor_id = db.Column(db.INTEGER,db.ForeignKey("contributor.id"))
	contributor = db.relationship(Contributor)
	legislator_id = db.Column(db.String,db.ForeignKey("legislator.id"))
	legislator = db.relationship(Legislator,backref="contributions")
	def __str__(self):
		return "Contribution: "+str(self.serialize())
	def __repr__(self):
		return "Contribution: "+str(self.serialize())
	def serialize(self):
		return get_keys(self.__dict__,[x for x in self.__dict__.keys() if not(x.startswith("_"))])



def populate():
	# Legislator.query.delete()
	# Bill.query.delete()


	con = Contributor(id=1,name="Paul Weinberg",zip="11234")


	l = Legislator(id="T1",offices=[{1:2}])
	l2 = Legislator(id="T2",offices=[{1:3}])

	c = Contribution(id=2,amount=14.5,contributor=con,legislator=l)

	c2 = Contribution(id=3,amount=140.0,contributor=con,legislator=l2)



	b = Bill(id="2",no_count=3,sponsors=[l,l2])


	db.session.add(l)
	db.session.add(l2)
	db.session.add(b)
	db.session.add(con)
	db.session.add(c)

	db.session.commit()

def tests():
	print("Contributor 1 Contributions:")
	pprint(db.session.query(Contributor).get(1).contributions)
	print()
	pprint("Bill 2 Contributions:")
	pprint(db.session.query(Bill).get("2").sponsors)
	print()
	print("Legislator T1 Contributions:")
	pprint(db.session.query(Legislator).get("T1").contributions)
	print()


def load_dataframes():
	pass

def load_contributors():
	df = pd.read_csv("{}/contributors.csv".format(shared_dir))
	le = len(df)
	for i,row in df.iterrows():
		print("%.2f%%" % ((i/float(le))*100))
		db.session.add(Contributor(**row))
	db.session.commit()

def load_legislators():
	df = pd.read_csv("{}/legislators.csv".format(shared_dir))
	le = float(len(df))
	for i,row in df.iterrows():
		print("%.2f%%" % ((i/le)*100))
		db.session.add(Legislator(**{
			"id":(row["id"]),
			"filer_id":int(row["filer_id"]),
			"sources":(row["sources"]),
			"offices":(row["offices"]),
			"first_name":(row["first_name"]),
			"middle_name":(row["middle_name"]),
			"last_name":(row["last_name"]),
			"district":int(row["district"]) if not(np.isnan(row["district"])) else -1,
			"party":(row["party"]),
			"photo_url":(row["photo_url"])}))
	db.session.commit()

def load_contributions():
	df = pd.read_csv("{}/contributions.csv".format(shared_dir))
	le = float(len(df))
	with db.session.no_autoflush:
		for i,row in df.iterrows():
			print("%.2f%%" % ((i/le)*100))
			dat = row.to_dict()
			id = int(i)
			amount = float(dat["contributionAmount"])
			filer_id = int(dat["filerIdent"])
			submitted_date = str(int(dat["receivedDt"])) if not(row.isnull()["receivedDt"]) else None,
			contributor = db.session.query(Contributor).get(dat["contributor_id"])
			ans = db.session.query(Legislator).filter(Legislator.filer_id==filer_id)
			try:
				legislator = ans[0]
			except:
				legislator = None
			# legislator = None
			attrs = dict(id=id,amount=amount,filer_id=filer_id,submitted_date=submitted_date,contributor=contributor,legislator=legislator)
			# print(list(map(lambda x: [x[0],type(x[1])],attrs.items())))
			db.session.add(Contribution(**attrs))
	db.session.commit()

def load_bills():
	df = pd.read_csv("{}/bill_data.csv".format(shared_dir))
	le = float(len(df))
	with db.session.no_autoflush:
		for i,row in df.iterrows():
			print("%.2f%%" % ((i/le)*100))
			dat = row.to_dict()
			new_sponsors = ast.literal_eval(dat["sponsors"]) if dat["sponsors"] else []
			spons = [x["leg_id"] for x in new_sponsors if x["leg_id"]]
			db.session.add(Bill(**{
				"id":dat["id"],
				"no_count":int(dat["no_count"]) if not(row.isnull()["no_count"]) else -1,
				"no_votes":dat["no_votes"] if not(row.isnull()["no_votes"]) else [],
				"yes_count":int(dat["yes_count"]) if not(row.isnull()["yes_count"]) else -1,
				"yes_votes":dat["yes_votes"] if not(row.isnull()["yes_votes"]) else [],
				"prefix":dat["prefix"],
				"number":int(dat["number"]),
				"session":dat["session"],
				"sources":dat["sources"] if not(row.isnull()["sources"]) else [],
				"sponsor_meta":dat["sponsors"] if not(row.isnull()["sponsors"]) else [],
				"sponsors": [db.session.query(Legislator).get(c) for c in spons if db.session.query(Legislator).get(c)],
				"subjects":dat["subjects"] if not(row.isnull()["subjects"]) else [],
				"title":dat["title"]
			}))
		db.session.commit()

def build_db():
	db.create_all()
	load_legislators()
	load_bills()
	load_contributors()
	#load_contributions()


if __name__ == "__main__":
	pass
	# print(db.session.query(Legislator).filter(Legislator.filer_id==20745)[0])
	# load_contributions()
	build_db()
	# load_bills()
