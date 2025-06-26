import unittest
from init import create_app
from configuration import TestConfig

class ManagersRoute(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False

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

    def login_as_admin(self):
        with self.client.session_transaction() as sess:
            sess['user'] = self.admin_user
            sess['line_managers'] = {
                1: {
                    "id": 1,
                    "email": "admin1@gmail.com",
                    "first_name": "Maddison",
                    "last_name": "Forrester"
                }
            }
            sess['apprentices'] = {
                2: "Helen Attwood"
            }

    def login_as_apprentice(self):
        with self.client.session_transaction() as sess:
            sess['user'] = self.apprentice_user
            sess['line_managers'] = {
                1: {
                    "id": 1,
                    "email": "admin1@gmail.com",
                    "first_name": "Maddison",
                    "last_name": "Forrester"
                }
            }
            sess['apprentices'] = {
                2: "Helen Attwood"
            }

    def test_managers_page_loads_as_admin(self):
        self.login_as_admin()
        response = self.client.get('/managers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Line Manager', response.data)

    def test_managers_page_loads_as_apprentice(self):
        self.login_as_apprentice()
        response = self.client.get('/managers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Line Manager', response.data)

    def test_managers_redirects_if_not_logged_in(self):
        response = self.client.get('/managers', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_admin_sees_all_line_managers(self):
        self.login_as_admin()
        response = self.client.get('/managers')
        self.assertIn(b'All Line Managers', response.data)
        self.assertIn(b'Add Line Manager', response.data)

if __name__ == '__main__':
    unittest.main()
