import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from models import *


app = Flask(__name__)
app.config.update(PROPAGATE_EXCEPTIONS = True)
app.url_map.strict_slashes = False

engine = create_engine('URI') ##### CHANGE #####
Session = sessionmaker(bind=engine)
db_session = Session()



"""

ROUTING CODE HERE

"""


def run_server():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
	run_server()