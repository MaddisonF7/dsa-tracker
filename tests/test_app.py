import unittest
from init import create_app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Disable CSRF
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True

    def test_login_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_wrong_login(self):
        response = self.client.post('/', data={
            'email': 'fake@user.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Invalid', response.data)

    def test_home_redirects(self):
        response = self.client.get('/home', follow_redirects=True)
        self.assertIn(b'Login', response.data)

if __name__ == "__main__":
    unittest.main()
