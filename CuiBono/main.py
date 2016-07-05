from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/bills")
@app.route("/bills/")
@app.route("/bills/<int:billnumber>")
def bills(billnumber=6):
	return render_template("bills.html",{"bills":[1,2,3,4]})

@app.route("/legistors")
@app.route("/legistors/")
def legislator():
	return render_template("legistors.html")

if __name__ == "__main__":
	app.run(debug=True)