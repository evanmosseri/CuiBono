from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://:evan@localhost/testdb"
db = SQLAlchemy(app)

class Test(db.Model):
	id = db.Column(db.INTEGER,primary_key=True)
	name = db.Column(db.String(80))

if __name__ == "__main__":
	db.create_all()