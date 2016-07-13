from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from models import Bill, Legislator, Contributor, Contribution
from loader import my_create_db
from db import *

@manager.command
def create_db():
	app.config['SQLALCHEMY_ECHO'] = True
	my_create_db()

@manager.command
def create_test_db():
	app.config['SQLALCHEMY_DATABASE_URI'] = ''
	app.config['SQLALCHEMY_ECHO'] = True
	db.create_all()

@manager.command
def drop_db():
	app.config['SQLALCHEMY_ECHO'] = True
	db.drop_all()


# BILL

# Get all bills
def get_bills(args, verbose):
	result = []
	session = Session()
	query = session.query(Bill).order_by(Bill.id).filter_by(**args)
	session.close()
	for row in query:
		data = Bill.serialize(row)
		result.append(data)
	return result

# Get bill by id
def get_bill_by_id(bill_id, verbose):
	session = Session()
	row = session.query(Bill).filter(Bill.id == bill_id).first()
	session.close()
	result = {}
	if row:
		result = Bill.serialize(row)
	return result	



# LEGISLATOR

# Get all legislators
def get_legislators(args, verbose):
	result = []
	session = Session()
	query = session.query(Legislator).order_by(Legislator.id).filter_by(**args)
	session.close()
	for row in query:
		data = Legislator.serialize(row)
		result.append(data)
	return result

# Get legislator by id
def get_legislator_by_id(legislator_id, verbose):
	session = Session()
	row = session.query(Legislator.filter(Legislator.id == legislator_id).first()
	session.close()
	result = {}
	if row:
		result = Legislator.serialize(row)
	return result



# CONTRIBUTOR

# Get all contributors
def get_contributors(args, verbose):
	result = []
	session = Session()
	query = session.query(Contributor).order_by(Contributor.id).filter_by(**args)
	session.close()
	for row in query:
		data = Contributor.serialize(row)
		result.append(data)
	return result

# Get contributor by id
def get_contributor_by_id(contributor_id, verbose):
	session = Session()
	row = session.query(Contributor).filter(Contributor.id == contributor_id).first()
	session.close()
	result = {}
	if row:
		result = Contributor.serialize(row)
	return result



# CONTRIBUTION

# Get all contributions
def get_contributions(args, verbose):
	result = []
	session = Session()
	query = session.query(Contribution).order_by(Contribution.id).filter_by(**args)
	session.close()
	for row in query:
		data = Contribution.serialize(row)
		result.append(data)
	return result

# Get contribution by id
def get_contribution_by_id(contribution_id, verbose):
	session = Session()
	row = session.query(Contribution).filter(Contribution.id == contribution_id).first()
	session.close()
	result = {}
	if row:
		result = Contribution.serialize(row)
	return result

if __name__ == "__main__":
	manager.run()


