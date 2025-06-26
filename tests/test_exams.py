import unittest
from init import create_app, mysql
from configuration import TestConfig

class ExamsRoute(unittest.TestCase):
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

    def test_exams_page_access_as_admin(self):
        self.login_as_admin()
        response = self.client.get('/exams')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exam', response.data)

    def test_exams_page_access_as_apprentice(self):
        self.login_as_apprentice()
        response = self.client.get('/exams')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exam', response.data)

    def test_exams_redirects_if_not_logged_in(self):
        response = self.client.get('/exams', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_add_exam_invalid_date(self):
        self.login_as_admin()
        response = self.client.post('/add/Exam', data={
            'name': 'Python Fundamentals',
            'exam_date': 'invalid-date',
            'status': 'Scheduled',
            'apprentice_id': '2'
        }, follow_redirects=True)
        self.assertIn(b'An error occurred', response.data)

    def test_add_edit_and_delete_exam_valid_data(self):
        self.login_as_admin()
        self.client.post('/add/Exam', data={
            'name': 'Python Basics',
            'exam_date': '2024-09-01',
            'status': 'Scheduled',
            'apprentice_id': '2'
        }, follow_redirects=True)

        response = self.client.get('/exams')
        self.assertIn(b'Python Basics', response.data)

        with self.app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM Exam WHERE name = %s AND apprentice_id = %s", ('Python Basics', 2))
            result = cur.fetchone()
            cur.close()

        self.assertIsNotNone(result)
        exam_id = result[0]

        edit_response = self.client.post(f'/edit/Exam/{exam_id}', data={
            'name': 'Python Basics Updated',
            'exam_date': '2024-10-01',
            'status': 'Completed',
            'apprentice_id': '2'
        }, follow_redirects=True)
        self.assertIn(b'Record successfully updated', edit_response.data)

        delete_response = self.client.post(
            f'/delete/Exam/{exam_id}',
            headers={'Referer': '/exams'},
            follow_redirects=True
        )
        self.assertIn(b'Record successfully deleted', delete_response.data)


if __name__ == '__main__':
    unittest.main()
