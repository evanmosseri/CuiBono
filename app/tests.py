import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
            ),  follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    def register(self, username, password, password2=None, email=None):

        if password2 is None:
            password2 = password
        if email is None:
            email = username + '@example.com'
        return self.post('/register', data={
            'username':     username,
            'password':     password,
            'password2':    password2,
            'email':        email,
        }, follow_redirects=True)



    def register_and_login(self, username, password):
        register(self, username, password)
        return login(self, username, password)


    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    def test_messages1(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

    def test_messages2(self):
        self.login('admin', "default")
        rv = self.app.post('/add', data = dict(title = "Hi there", text = "Well isn't that something"), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert "Hi there" in rv.data
        assert "Well isn't that something" in rv.data


    def test_messages3(self):
        self.login('admin', "default")
        rv = self.app.post('/add', data = dict(title = "This is a test", text = "Let's hope this works"), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert "This is a test" in rv.data
        assert "Let's hope this works" in rv.data


    def test_login_logout(self):
        rv = register_and_login(self, 'user1', 'default')
        assert 'You were logged in' in rv.data
        rv = logout(self)
        assert 'You were logged out' in rv.data
        rv = login(self, 'user1', 'wrongpassword')
        assert 'Invalid password' in rv.data
        rv = login(self, 'user2', 'wrongpassword')
        assert 'Invalid username' in rv.data

    def test_register1(self):
        rv = register(self, 'user1', 'default')
        assert 'You were successfully registered ' \
               'and can login now' in rv.data
        rv = register(self, 'user1', 'default')
        assert 'The username is already taken' in rv.data
        rv = register(client, 'dur', 'x', 'x')
        assert 'The two passwords do match' in rv.data
        rv = register(client, 'boo', 'foo', email='broken')
        assert 'You have to enter a valid email address' in rv.data
        rv = register(client, 'boo', 'foo')
        assert 'You were successfully registered ' \
               'and can login now' in rv.data

    def test_register2(self):
        rv = register(self, "user2", "password")]
        rv = self.login("user2", "password")
        assert "You were logged in" in rv.data
        rv = register(self, "user2", "ader")
        assert "The username is already taken" in rv.data

    def test_register3(self):
        rv = register(self, "adminz", "admin")
        rv = self.login("adminz","admin")
        assert "You werer logged in" in rv.data
        rv = register(self, "user12", "user")
        assert "You were successfully registered"

if __name__ == '__main__':
    unittest.main()
