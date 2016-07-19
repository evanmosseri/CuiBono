import os
from flask import Flask, render_template, jsonify, request
from unittest import main, TestCase
from models_new import *

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:database@cuibono.io/cuibono"
db = SQLAlchemy(app)

class FlaskTest(TestCase):

    def test_get(self):
        bill = db.session.query(Bill).get("TXB00000001")
        self.assertEqual(bill.prefix, "SB")
        self.assertEqual(bill.session, "81")

    def test_get2(self):
        legi = db.session.query(Legislator).get("TXL000201")
        self.assertEqual(legi.filer_id, 20745)
        self.assertEqual(legi.district, -1)

    def test_get3(self):
        tributor = db.session.query(Contributor).get(39945)
        self.assertEqual(tributor.name, "El Paso Corp./Coastal Emp. Action Fund")
        self.assertEqual(tributor.type, "entity")
    
    def test_get4(self):
        con = db.session.query(Contribution).get(1)
        assert(con == None)
    
    def test_add(self):
        db.session.add(Bill(id = "TX1234567890", prefix = "House"))
        db.session.commit()
        bill = db.session.query(Bill).get("TX1234567890")
        self.assertEqual(bill.prefix, "House")

    def test_add2(self):
        db.session.add(Legislator(id = "38777738", filer_id = 3883))
        db.session.commit()
        legi = db.session.query(Legislator).get("38777738")
        self.assertEqual(legi.filer_id, 3883)

    def test_add3(self):
        db.session.add(Contributor(id = 8888888, name = "evan"))
        db.session.commit()
        contri = db.session.query(Contributor).get(8888888)
        self.assertEqual(contri.name, "evan")

    def test_add4(self):
        db.session.add(Contribution(id = 209383000, amount = 8800))
        db.session.commit()
        contrib = db.session.query(Contribution).get(209383000)
        self.assertEqual(contrib.amount, 8800)
        check = db.session.query(Contributor).get(38203000)
        assert(check == None)
    
    def test_delete(self):
        bill = db.session.query(Bill).get("TX1234567890")
        assert(bill != None)
        db.session.delete(bill)
        db.session.commit()
        check = db.session.query(Bill).get("TX1234567890")
        assert(check == None)
    
    def test_delete2(self):
        legi = db.session.query(Legislator).get("38777738")
        assert(legi != None)
        db.session.delete(legi)
        db.session.commit()

        check = db.session.query(Legislator).get("38777738")
        assert(check == None)
    
    def test_delete3(self):
        c = db.session.query(Contributor).get(8888888)
        assert(c != None)
        db.session.delete(c)
        db.session.commit()
    
    def test_delete4(self):
        con = db.session.query(Contribution).get(209383000)
        assert(con != None)
        db.session.delete(con)
        db.session.commit()
        check = db.session.query(Contribution).get(209383000)
        assert(check == None)



if __name__ == '__main__':
    main()
