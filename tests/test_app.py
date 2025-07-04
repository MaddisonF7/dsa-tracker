import unittest
from init import create_app
from configuration import TestConfig

class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True

        # Admin mock user
        self.admin_user = {
            'id': 1,
            'email': 'admin1@gmail.com',
            'first_name': 'Maddison',
            'last_name': 'Forrester',
            'role': 'Admin',
            'line_manager_id': None,
            'cohort': None,
            'start_date': None,
            'end_date': None,
            'created_on': None,
            'modified_on': None
        }

        # Apprentice mock user
        self.apprentice_user = {
            'id': 2,
            'email': 'apprentice1@gmail.com',
            'first_name': 'Helen',
            'last_name': 'Attwood',
            'role': 'Apprentice',
            'line_manager_id': 1,
            'cohort': '2024',
            'start_date': '2024-01-01',
            'end_date': '2025-01-01',
            'created_on': None,
            'modified_on': None
        }

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

    def test_valid_login_sets_session_for_apprentice(self):
        with self.client.session_transaction() as session:
            session['user'] = self.apprentice_user
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Digital Skills Academy Tracker', response.data)

    def test_logout_redirects_to_login(self):
        with self.client.session_transaction() as session:
            session['user'] = self.admin_user
        response = self.client.post('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == "__main__":
    unittest.main()
