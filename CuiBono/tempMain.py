from flask import Flask, render_template
app = Flask(__name__)

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
	return render_template("bills.html") 

@app.route("/contributors/<id>")
@app.route("/contributors")
def contributors(id=None):
	return render_template("contributors.html") 

@app.route("/about")
def about():
	return render_template("about.html") 

@app.route("/hb1")
def hb1():
	return render_template("hb1.html") 

@app.route("/hb15")
def hb15():
	return render_template("hb15.html") 




if __name__ == "__main__":
	app.run("0.0.0.0",debug=True)


