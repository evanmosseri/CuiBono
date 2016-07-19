from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:database@cuibono.io/cuibono?charset=utf8"
db = SQLAlchemy(app)




if __name__ == "__main__":
	app.run("0.0.0.0",debug=True)


