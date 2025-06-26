import unittest
from init import create_app, mysql
from configuration import TestConfig

class ApprenticesRoute(unittest.TestCase):
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
                '1': {
                    "id": 1,
                    "email": "admin1@gmail.com",
                    "first_name": "Maddison",
                    "last_name": "Forrester"
                }
            }
            sess['apprentices'] = {
                '2': "Helen Attwood"
            }

    def login_as_apprentice(self):
        with self.client.session_transaction() as sess:
            sess['user'] = self.apprentice_user
            sess['line_managers'] = {
                '1': {
                    "id": 1,
                    "email": "admin1@gmail.com",
                    "first_name": "Maddison",
                    "last_name": "Forrester"
                }
            }
            sess['apprentices'] = {
                '2': "Helen Attwood"
            }

    def test_apprentices_redirects_if_not_logged_in(self):
        response = self.client.get('/apprentices', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_assigned_apprentices_section_visible_for_admin(self):
        self.login_as_admin()
        response = self.client.get('/apprentices')
        self.assertIn(b'Your Apprentices', response.data)

    def test_assigned_apprentices_section_hidden_for_apprentice(self):
        self.login_as_apprentice()
        response = self.client.get('/apprentices')
        self.assertNotIn(b'Assigned Apprentices', response.data)

    def test_add_apprentice_invalid_email(self):
        self.login_as_admin()
        response = self.client.post('/add/User', data={
            'first_name': 'Helen',
            'last_name': 'Attwood',
            'email': 'invalid-email',
            'password': 'apprenticepass123',
            'role': 'Apprentice',
            'cohort': '2024',
            'start_date': '2024-06-26',
            'line_manager_id': '1'
        }, follow_redirects=True)
        self.assertIn(b'Invalid email format', response.data)

    def test_add_apprentice_invalid_password(self):
        self.login_as_admin()
        response = self.client.post('/add/User', data={
            'first_name': 'Helen',
            'last_name': 'Attwood',
            'email': 'apprentice1@gmail.com',
            'password': '123',
            'role': 'Apprentice',
            'cohort': '2024',
            'start_date': '2024-06-26',
            'line_manager_id': '1'
        }, follow_redirects=True)
        self.assertIn(b'Password must be at least 6 characters', response.data)

    def test_add_edit_and_delete_apprentice_valid_data(self):
        self.login_as_admin()
        email = 'test.user@dsa.com'
        updated_last_name = 'UpdatedSmith'

        self.client.post('/add/User', data={
            'first_name': 'Test',
            'last_name': 'Smith',
            'email': email,
            'password': 'securepass123',
            'role': 'Apprentice',
            'cohort': '2024',
            'start_date': '2024-01-01',
            'end_date': '2024-11-03',
            'line_manager_id': '1'
        }, follow_redirects=True)

        response = self.client.get('/apprentices')
        self.assertIn(email.encode(), response.data)

        with self.app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM User WHERE email = %s", (email,))
            result = cur.fetchone()
            cur.close()

        self.assertIsNotNone(result)
        apprentice_id = result[0]

        edit_response = self.client.post(f'/edit/User/{apprentice_id}', data={
            'first_name': 'Test',
            'last_name': updated_last_name,
            'email': email,
            'password': '',
            'role': 'Apprentice',
            'cohort': '2024',
            'start_date': '2024-01-01',
            'end_date': '2025-11-03',
            'line_manager_id': '1'
        }, follow_redirects=True)
        self.assertIn(b'Record successfully updated', edit_response.data)

        delete_response = self.client.post(
            f'/delete/User/{apprentice_id}',
            headers={'Referer': '/apprentices'},
            follow_redirects=True
        )
        self.assertIn(b'Record successfully deleted', delete_response.data)


if __name__ == '__main__':
    unittest.main()
