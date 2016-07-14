from flask import Flask, render_template
# from models_new import *
from flask.ext.sqlalchemy import SQLAlchemy
from models_new import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///database"
db = SQLAlchemy(app)

billz = db.session.query(Bill).all()
legislatorz = db.session.query(Legislator).all()
contributorz = db.session.query(Contributor).all()
contributionz = db.session.query(Contribution).all()

print(billz[0].sponsors[0].contributions)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/legislators/<int:id>")
@app.route("/legislators")
def legislators(id=None):
	return render_template("legislators.html") 

@app.route("/bills/<id>")
@app.route("/bills")
def bills(id=None):	
	return render_template("bills.html",bills = billz) 

@app.route("/contributors/<id>")
@app.route("/contributors")
def contributors(id=None):
	return render_template("contributors.html") 

@app.route("/contributions")
def contributions():
	return render_template("contributions.html") 	

@app.route("/about")
def about():
	return render_template("about.html") 

@app.route("/bills/hb1")
def hb1():
	return render_template("hb1.html") 

@app.route("/bills/hb15")
def hb15():
	return render_template("hb15.html") 

@app.route("/bills/hb24")
def hb24():
	return render_template("hb24.html") 

@app.route("/legislators/54588")
def otto():
	return render_template("otto.html") 

@app.route("/legislators/58277")
def walle():
	return render_template("walle.html") 

@app.route("/legislators/66272")
def davis():
	return render_template("davis.html") 

@app.route("/contributors/borderhealthpac")
def borderhealthpac():
	return render_template("borderhealthpac.html") 

@app.route("/contributors/ampac")
def AMpac():
	return render_template("AMpac.html") 

@app.route("/contributors/plumberspac")
def plumberspac():
	return render_template("plumberspac.html") 

@app.route('/unittest/')
@app.route('/unittest/<name>')
def unittest(name = None):
	contents = ""
	with open("TestResult", "r") as file:
		for line in file:
			contents +="\n"+line+"\n"
	file.close()
	return render_template('unittest.html',name = contents)

if __name__ == "__main__":
	app.run("0.0.0.0",debug=True)


