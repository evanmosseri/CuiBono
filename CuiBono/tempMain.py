from flask import Flask, render_template, jsonify
# from models_new import *
from flask.ext.sqlalchemy import SQLAlchemy
from models_new import *
from flask import request

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///database"
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
	if not(id):
		page = int(request.args.get("page")) if request.args.get("page") else 0
		num_per_page = int(request.args.get("num_per_page")) if request.args.get("num_per_page") else 20
		return render_template("legislators.html", legislators = db.session.query(Legislator).offset(2*page).limit(num_per_page))
	else:
		return render_template("legislator.html", legislator = db.session.query(Legislator).get(id))


@app.route("/bills/<id>")
@app.route("/bills/")
def bills(id=None, methods=["GET"]):
	if not(id):
		page = int(request.args.get("page")) if request.args.get("page") else 0
		num_per_page = int(request.args.get("num_per_page")) if request.args.get("num_per_page") else 20
		return render_template("bills.html", bills = db.session.query(Bill).offset(2*page).limit(num_per_page),page=page) 
	else:
		return render_template("bill.html", bill = db.session.query(Bill).get(id))

@app.route("/contributors/<int:id>")
@app.route("/contributors/")
def contributors(id=None):
	if not(id):
		page = int(request.args.get("page")) if request.args.get("page") else 0
		num_per_page = int(request.args.get("num_per_page")) if request.args.get("num_per_page") else 20
		return render_template("contributors.html", contributors = db.session.query(Contributor).offset(2*page).limit(num_per_page))
	else:
		return render_template("contributor.html", contributor = db.session.query(Contributor).get(id))


@app.route("/contributions/<int:id>")
@app.route("/contributions")
def contributions(id=None):
	if not(id):
		page = int(request.args.get("page")) if request.args.get("page") else 0	
		num_per_page = int(request.args.get("num_per_page")) if request.args.get("num_per_page") else 20
		temp = db.session.query(Contribution).filter(Contribution.legislator != None).offset(2*page).limit(num_per_page)
		return render_template("contributions.html",contributions = temp) 	
	else:
		return render_template("contribution.html", contribution= db.session.query(Contribution).get(id))

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

@app.route("/api/bill")
def get_all_bills():
	bills = db.session.query(Bill).all()
	return jsonify(response=bills)

@app.route("/api/legislator")
def get_all_legislators():
	legislator = db.session.query(Legislator).all()
	return jsonify(response=legislator)

@app.route("/api/contributor")
def get_all_contributor():
	contributors = db.session.query(Contributor).all()
	return jsonify(response=contributors)

@app.route("/api/contribution")
def get_all_legislators():
	contributions = db.session.query(Contribution).all()
	return jsonify(response=contributions)

if __name__ == "__main__":
	app.run("0.0.0.0",debug=True)


