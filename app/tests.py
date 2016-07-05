import os
import flaskr
import unittest
import tempfile

from flask_testing import TestCase
from myapp import create_app, db


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

        def test_bill1(self):
           bill1 = query.filter_by(number=1, prefix = "House")
           assert bill1.Authors is "John Otto"
           assert bill1.sessionID is "84R"
           assert bill1.sessionYear is "2015"
           assert bill1.Sponsors is "Senator Jane Nelson"

        def test_bill2(self):
           bill2 = query.filter_by(number=15,  prefix = "House")
           assert bill2.Authors is "John Otto, Armando Walle"
           assert bill2.sessionID is "84R"
           assert bill2.sessionYear is "2015"
           assert bill2.Sponsors is "Senator Kevin Eltife"

        def test_bill3(self):
           bill3 = query.filter_by(number=24,  prefix = "House")
           assert bill3.Authors is "Sarah Davis"
           assert bill3.sessionID is "84R"
           assert bill3.sessionYear is "2015"
           assert bill3.Sponsors is "Representative Sarah Davis"

        def test_legislators1(self):
            legis1 = query.filter_by(name = "John Otto")
            assert legis1.district is "18"
            assert legis1.party is "Republican"
            assert legis1.hometown is "Dayton, TX"
            assert legis1.bills is "House Bill 1, House Bill 15"
            assert legis1.contributors is "N/A"

        def test_legislators2(self):
            legis2 = query.filter_by(name = "Armando Walle")
            assert legis2.district is "140"
            assert legis2.party is "Democratic"
            assert legis2.hometown is "Houston, TX"
            assert legis2.bills is "House Bill 15"
            assert legis2.contributors is "Border Health PAC, Plumbers Local Union No. 68 PAC Fund"

        def test_legislators3(self):
            legis3 = query.filter_by(name = "Sarah Davis")
            assert legis3.district is "134"
            assert legis3.party is "Republican"
            assert legis3.hometown is "Charleston, WVA"
            assert legis3.bills is "House Bill 24"
            assert legis3.contributors is "A&M PAC"

        def test_contributors1(self):
            contributor1 = query.filter.by(name = "Border Health PAC")
            assert contributor1.type is "Entity"
            assert contributor1.website is "borderhealthpac.com"
            assert contributor1.contributors is "Walle: $5,000"
            assert contributor3.city is "McAllen, TX"
            assert contributor3.zipCode is "78504"

        def test_contributors2(self):
            contributor2 = query.filter.by(name = "Plumbers Local Union No. 68 PAC Fund")
            assert contributor2.type is "Entity"
            assert contributor2.website is "Plumber's PAC"
            assert contributor2.contributors is "Walle: $2,000"
            assert contributor3.city is "Houston, TX"
            assert contributor3.zipCode is "77249"

        def test_contributors3(self):
            contributor3 = query.filter.by(name = "A&M PAC")
            assert contributor3.type is "Entity"
            assert contributor3.website is "tamuspac.org"
            assert contributor3.contributors is "Davis: $2,500"
            assert contributor3.city is "Austin, TX"
            assert contributor3.zipCode is "78768"

        def test_contributions1(self):
            contribution1 = query.filter.by(contributor = "Border Health PAC", legislator = "Armando Walle", date = "8-17-2015")
            assert contribution1.amount is "$5,000"

        def test_contributions2(self):
            contribution2 = query.filter.by(contributor = "A&M PAC", legislator = "Sarah Davis", date = "2-26-2016")
            assert contribution2.amount is "$2,500"

        def test_contributions3(self):
            contribution3 = query.filter.by(contributor = "Plumbers Local Union No. 68 PAC Fund", legislator = "Armando Walle", date = "10-20-2015")
            assert contribution3.amount is "$2,000"








if __name__ == '__main__':
    unittest.main()
