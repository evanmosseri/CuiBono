from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from models import Bill, Legislator, Contributor, Contribution
import json

engine = create_engine(' ')
Session = sessionmaker(bind=engine)
session = Session()
engine.echo = True


# Bill Data
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
	session.merge(current_bill)



# Legislator Data
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
	session.merge(current_legislator)



# Contributor Data
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
	session.merge(current_contributor)


# Contribution Data
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
	session.merge(current_contribution)

session.commit()