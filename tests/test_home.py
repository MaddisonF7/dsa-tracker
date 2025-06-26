import unittest
from init import create_app
from configuration import TestConfig


class HomeRoute(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False

        # Mock Admin
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
            'modified_on': None,
        }

        # Mock Apprentice
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
            'modified_on': None,
        }

    def test_home_redirects_if_not_logged_in(self):
        response = self.client.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_home_page_loads_for_logged_in_user(self):
        with self.client.session_transaction() as sess:
            sess['user'] = self.apprentice_user

        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Digital Skills Academy Tracker', response.data)
        self.assertIn(b'Welcome, Helen!', response.data)

    def test_home_sets_line_managers_and_apprentices(self):
        with self.client.session_transaction() as sess:
            sess['user'] = self.apprentice_user
            sess.pop('line_managers', None)
            sess.pop('apprentices', None)

        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as sess:
            self.assertIn('line_managers', sess)
            self.assertIn('apprentices', sess)


if __name__ == '__main__':
    unittest.main()
