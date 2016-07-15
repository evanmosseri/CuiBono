import os
import flask
import unittest
import tempfile
from unittest import main, TestCase

from tempMain import db
from models_new import *

class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class FlaskTest(MyTest):

    def test_add(self):
        db.session.add(Bill(id = "TX0000000", prefix = "House"))
        db.sessino.commit()
        bill = db.session.query(Bill).get("TX0000000")
        self.assertEqual(bill.prefix, "House")

    def test_add1(self):
        db.session.add(Legislator(id = "3838", filer_id = 3883))
        db.sessino.commit()
        legi = db.session.query(Legislator).get("3838")
        self.assertEqual(legi.filer_id, 3883)

    def test_add2(self):
        db.session.add(Contributor(id = 38203, name = "evan"))
        db.sessino.commit()
        contri = db.session.query(Contributor).get(38203)
        self.assertEqual(contri.name, "evan")

    def test_add3(self):
        db.session.add(Contribution(id = 209383, amount = 8800))
        db.sessino.commit()
        contrib = db.session.query(Contribution).get(209383)
        self.assertEqual(contrib.amount, 8800)

    def test_delete(self):
        db.session.add(Bill(id = "TX0000000", prefix = "House"))
        db.session.commit()
        b = db.session.query(Bill).filter(Bill.id=="TX0000000")
        assert(b != None)
        db.session.delete(b)
        db.session.commit()

        check = db.session.query(Bill).filter(Bill.id=="TX0000000")
        assert(check == None)

    def test_delete1(self):
        db.session.add(Legislator(id = "3838", filer_id = 3883))
        db.sessino.commit()
        legi = db.session.query(Legislator).filter(Legislator.id=="3838")
        assert(legi != None)
        db.session.delete(legi)
        db.session.commit()

        check = db.session.query(Legislator).filter(Legislator.id=="3838")
        assert(check == None)

    def test_delete2(self):
        db.session.add(Contributor(id = 38203, name = "evan"))
        db.sessino.commit()
        c = db.session.query(Contributor).filter(Contributor.id==38203)
        assert(c != None)
        db.session.delete(c)
        db.session.commit()

        check = db.session.query(Contributor).filter(Contributor.id==38203)
        assert(check == None)

    def test_delete3(self):
        db.session.add(Contribution(id = 209383, amount = 8800))
        db.sessino.commit()
        con = db.session.query(Contribution).filter(Contribution.id==209383)
        assert(con != None)
        db.session.delete(contribution)
        db.session.commit()

        check = db.session.query(Contribution).filter(Contribution.id==209383)
        assert(check == None)








if __name__ == '__main__':
    main()
