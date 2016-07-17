from flask import Flask, render_template, jsonify
# from models_new import *
from flask.ext.sqlalchemy import SQLAlchemy
from models_new import *
from flask import request

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:database@cuibono.io/database"
db = SQLAlchemy(app)

# billz = db.session.query(Bill).limit(5).all()
# legislatorz = db.session.query(Legislator).limit(5).all()
# contributorz = db.session.query(Contributor).limit(5).all()
# contributionz = db.session.query(Contribution).filter(Contribution.legislator != None).limit(5).all()

@app.route("/")
def index():
	return render_template("index.html")
	

@app.route("/legislators/<id>")
@app.route("/legislators/")
def legislators(id=None):
	page = int(request.args.get("page")) if request.args.get("page") else 0
	num_per_page = int(request.args.get("num_per_page")) if request.args.get("num_per_page") else 20
	sort = request.args.get("sort") if request.args.get("sort") else 0	
	if not(id):
		return render_template("legislators.html", legislators = db.session.query(Legislator).order_by(sort if sort else id).offset(2*page).limit(num_per_page),page=page)
	else:
		return render_template("legislator.html", legislator = db.session.query(Legislator).get(id),page=page)


@app.route("/bills/<id>")
@app.route("/bills/")
def bills(id=None, methods=["GET"]):
	page = int(request.args.get("page")) if request.args.get("page") else 0
	num_per_page = int(request.args.get("num_per_page")) if request.args.get("num_per_page") else 20
	sort = request.args.get("sort") if request.args.get("sort") else 0	
	if not(id):
		return render_template("bills.html", bills = db.session.query(Bill).order_by(sort if sort else id).offset(2*page).limit(num_per_page),page=page) 
	else:
		return render_template("bill.html", bill = db.session.query(Bill).get(id),page=page)

@app.route("/contributors/<int:id>")
@app.route("/contributors/")
def contributors(id=None):
	page = int(request.args.get("page")) if request.args.get("page") else 0
	num_per_page = int(request.args.get("num_per_page")) if request.args.get("num_per_page") else 20
	sort = request.args.get("sort") if request.args.get("sort") else 0	
	if not(id):
		return render_template("contributors.html", contributors = db.session.query(Contributor).order_by(sort if sort else id).offset(2*page).limit(num_per_page),page=page)
	else:
		return render_template("contributor.html", contributor = db.session.query(Contributor).get(id),page=page)


@app.route("/contributions/<int:id>")
@app.route("/contributions")
def contributions(id=None):
	page = int(request.args.get("page")) if request.args.get("page") else 0	
	num_per_page = int(request.args.get("num_per_page")) if request.args.get("num_per_page") else 20
	sort = request.args.get("sort") if request.args.get("sort") else 0	
	if not(id):
		temp = db.session.query(Contribution).filter(Contribution.legislator != None).order_by(sort if sort else id).offset(2*page).limit(num_per_page)
		return render_template("contributions.html",contributions = temp,page=page) 	
	else:
		return render_template("contribution.html", contribution= db.session.query(Contribution).get(id),page=page)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route('/unittest/')
@app.route('/unittest/<name>')
def unittest(name = None):
	contents = ""
	with open("TestResult", "r") as file:
		for line in file:
			contents +="\n"+line+"\n"
	file.close()
	return render_template('unittest.html',name = contents)

@app.route("/api/bill/")
def get_all_bills():
	bills = db.session.query(Bill).all()
	return jsonify([bill_to_dict(bil)for bil in bills])

@app.route("/api/legislator/")
def get_all_legislators():
	legislators = db.session.query(Legislator).all()
	return jsonify([legis_to_dict(never_skip_leg_day) for never_skip_leg_day in legislators])

@app.route("/api/contributor/")
def get_all_contributor():
	contributors = db.session.query(Contributor).all()
	return jsonify([contributor_to_dict(contra) for contra in contributors])

@app.route("/api/contribution/")
def get_all_legislator():
	contributions = db.session.query(Contribution).all()
	return jsonify([contribution_to_dict(x) for x in contributions])

def bill_to_dict(bill):
	if bill is None:
		return None
	bill_temp = {"id" : bill.id, "no_count" : bill.no_count, "no_votes" : bill.no_votes, "yes_count" : bill.yes_count, "yes_votes" : bill.yes_votes, "prefix" : bill.prefix, "number": bill.number, "session": bill.session, "sources": bill.sources,"sponsor_meta" : bill.sponsor_meta, "subjects" : bill.subjects, "title" : bill.title }
	sponsors_list = []
	for x in bill.sponsors :
		sponsors_list.append(legis_to_dict(x))
	bill_temp["sponsors"] = sponsors_list
	return bill_temp

def legis_to_dict(legis):
	if legis is None:
		return None 
	legis_dict = {"id" : legis.id, "filer_id" : legis.filer_id, "sources" : legis.sources , "offices" : legis.offices, "first_name" : legis.first_name , "middle_name" : legis.middle_name, "last_name" : legis.last_name, "district" : legis.district, "party" : legis.party, "photo_url" : legis.photo_url}
	return legis_dict

def contributor_to_dict(contra):
	if contra is None:
		return None
	contra_temp = {"id" : contra.id, "name" : contra.name, "type" : contra.type, "zip" : contra.zip}
	contribution_list = []
	for contribution in contra.contributions:
		contribution_list.append(contribution_to_dict(contribution))
	contra_temp["contributions"] = contribution_list
	return contra_temp

def contribution_to_dict(contra):
	if contra is None:
		return None
	contra_temp = {"id" : contra.id, "amount" : contra.amount, "filer_id" : contra.filer_id, "submitted_date" : contra.submitted_date, "contributor_id" : contra.contributor_id, "legislator_id": contra.legislator_id}
	contributor_list = []
	legislator_list = []

	contra_temp["contributor"] = contra.contributor.name
	if contra.legislator is not None:
		contra_temp["legislator"] = contra.legislator.first_name + " " + contra.legislator.last_name
	else:
		contra_temp["legislator"] = None
	return contra_temp

if __name__ == "__main__":
	app.run("0.0.0.0",debug=True)


