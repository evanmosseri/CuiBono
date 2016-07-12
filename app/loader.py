from sqlalchemy import *
#from sqlalchemy.orm import sessionmaker
from models import Bill, Legislator, Contributor, Contribution
import json

#from '' import db

"""
engine = create_engine(' ')
Session = sessionmaker(bind=engine)
session = Session()
engine.echo = True
"""

# Bill Data
def create_bills():
	with open('data/', 'r') as infile:
		data_file = json.load(infile)

	for key in data_file:
		data = data_file[key]
		current_bill = Bill(
			id = key,
			bill_id = data['bill_id'],
			leg_session = data['leg_session'],
			type = data['type'],
			number = data['number'],
			aye_or_nay = data['aye_or_nay'],
			text = data['text']
			)
		db.session.add(current_bill)

	db.session.commit()



# Legislator Data
def create_legislators():
	with open('data/', 'r') as infile:
		data_file = json.load(infile)

	for key in data_file:
		data = data_file[key]
		current_legislator = Legislator(
			legislator_id = key,
			name = data['name'],
			filer_id = data['filer_id'],
			bio = data['bio'],
			party = data['party'],
			district = data['district']
			)
		db.session.add(current_legislator)

	db.session.commit()



# Contributor Data
def create_contributors():
	with open('data/', 'r') as infile:
		data_file = json.load(infile)

	for key in data_file:
		data = data_file[key]
		current_contributor = Contributor(
			contributor_id = key,
			type = data['type'],
			name = data['name'],
			zipcode = data['zipcode']
			)
		db.session.add(current_contributor)

	db.session.commit()


# Contribution Data
def create_contributions():
	with open('data/', 'r') as infile:
		data_file = json.load(infile)

	for key in data_file:
		data = data_file[key]
		current_contribution = Contribution(
			contribution_id = key,
			amount = data['amount'],
			date_contributed = data['date_contributed'],
			contributor_id = data['contributor_id'],
			legislator_id = data['legislator_id']
			)
		db.session.add(current_contribution)

	db.session.commit()


#INIT DB
def create_db():
	db.drop_all()
	db.create_all()
	create_bills()
	create_legislators()
	create_contributors()
	create_contributions()