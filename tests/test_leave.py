import unittest
from init import create_app, mysql
from configuration import TestConfig

class LeaveRoute(unittest.TestCase):
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

        with self.app.app_context():
            cur = mysql.connection.cursor()
            # Ensure admin and apprentice are in DB
            cur.execute("""
                INSERT IGNORE INTO User (id, email, password, first_name, last_name, role, line_manager_id, cohort, start_date, end_date, created_at, modified_date)
                VALUES 
                (1, 'admin1@gmail.com', '', 'Maddison', 'Forrester', 'Admin', NULL, NULL, NULL, NULL, NOW(), NOW()),
                (2, 'apprentice1@gmail.com', '', 'Helen', 'Attwood', 'Apprentice', 1, '2024', '2024-01-01', '2025-01-01', NOW(), NOW())
            """)
            mysql.connection.commit()
            cur.close()

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

    def test_leave_page_access_admin(self):
        self.login_as_admin()
        response = self.client.get('/leave')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Leave', response.data)

    def test_leave_page_access_apprentice(self):
        self.login_as_apprentice()
        response = self.client.get('/leave')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Leave', response.data)

    def test_leave_page_redirects_if_not_logged_in(self):
        response = self.client.get('/leave', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_add_leave_valid(self):
        self.login_as_admin()
        response = self.client.post('/add/Leave_request', data={
            'leave_type': 'Sick',
            'start_date': '2024-09-01',
            'end_date': '2024-09-03',
            'status': 'Pending',
            'apprentice_id': '2'
        }, follow_redirects=True)
        self.assertIn(b'Record successfully added', response.data)

    def test_add_leave_missing_required_field(self):
        self.login_as_admin()
        response = self.client.post('/add/Leave_request', data={
            'leave_type': 'Annual',
            'start_date': '',
            'end_date': '2024-10-01',
            'status': 'Pending',
            'apprentice_id': '2'
        }, follow_redirects=True)
        self.assertIn(b"Column 'start_date' cannot be null", response.data)

    def test_add_edit_and_delete_leave(self):
        self.login_as_admin()

        # Add leave
        self.client.post('/add/Leave_request', data={
            'leave_type': 'Sick',
            'start_date': '2024-08-01',
            'end_date': '2024-08-05',
            'status': 'Pending',
            'apprentice_id': '2'
        }, follow_redirects=True)

        with self.app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM Leave_request WHERE leave_type = %s AND apprentice_id = %s", ('Sick', 2))
            result = cur.fetchone()
            cur.close()

        self.assertIsNotNone(result)
        leave_id = result[0]

        # Edit leave
        edit_response = self.client.post(f'/edit/Leave_request/{leave_id}', data={
            'leave_type': 'Annual',
            'start_date': '2024-08-02',
            'end_date': '2024-08-06',
            'status': 'Approved',
            'apprentice_id': '2'
        }, follow_redirects=True)
        self.assertIn(b'Record successfully updated', edit_response.data)

        # Delete leave
        delete_response = self.client.post(
            f'/delete/Leave_request/{leave_id}',
            headers={'Referer': '/leave'},
            follow_redirects=True
        )
        self.assertIn(b'Record successfully deleted', delete_response.data)


if __name__ == '__main__':
    unittest.main()
