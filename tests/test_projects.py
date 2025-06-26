import unittest
from init import create_app, mysql
from configuration import TestConfig

class ProjectsRoute(unittest.TestCase):
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

    def test_projects_page_loads_as_admin(self):
        self.login_as_admin()
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Projects', response.data)

    def test_projects_page_loads_as_apprentice(self):
        self.login_as_apprentice()
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Projects', response.data)

    def test_projects_redirects_if_not_logged_in(self):
        response = self.client.get('/projects', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_projects_content_visibility_for_admin(self):
        self.login_as_admin()
        response = self.client.get('/projects')
        self.assertIn(b'Project Name', response.data)

    def test_projects_content_visibility_for_apprentice(self):
        self.login_as_apprentice()
        response = self.client.get('/projects')
        self.assertIn(b'Project Name', response.data)

def test_add_edit_and_delete_project_valid(self):
    self.login_as_admin()

    # Ensure test users exist
    with self.app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT IGNORE INTO User (id, email, password, first_name, last_name, role,
                                     line_manager_id, cohort, start_date, end_date,
                                     created_at, modified_date)
            VALUES 
            (1, 'admin1@gmail.com', '', 'Maddison', 'Forrester', 'Admin', NULL, NULL, NULL, NULL, NOW(), NOW()),
            (2, 'apprentice1@gmail.com', '', 'Helen', 'Attwood', 'Apprentice', 1, '2024', '2024-01-01', '2025-01-01', NOW(), NOW())
        """)
        mysql.connection.commit()
        cur.close()

    # Add project
    self.client.post('/add/Project', data={
        'name': 'DSA Platform',
        'description': 'Internal tracker platform',
        'start_date': '2024-06-01',
        'end_date': '2024-12-01',
        'status': 'Ongoing',
        'apprentice_id': '2'
    }, follow_redirects=True)

    response = self.client.get('/projects')
    self.assertIn(b'DSA Platform', response.data)

    # Get project ID
    with self.app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM Project WHERE name = %s", ('DSA Platform',))
        result = cur.fetchone()
        cur.close()

    self.assertIsNotNone(result)
    project_id = result[0]

    # Edit project
    edit_response = self.client.post(f'/edit/Project/{project_id}', data={
        'name': 'DSA Tracker',
        'description': 'Updated platform name',
        'start_date': '2024-06-01',
        'end_date': '2024-12-31',
        'status': 'Completed',
        'apprentice_id': '2'
    }, follow_redirects=True)
    self.assertIn(b'Record successfully updated', edit_response.data)

    # Delete project
    delete_response = self.client.post(
        f'/delete/Project/{project_id}',
        headers={'Referer': '/projects'},
        follow_redirects=True
    )
    self.assertIn(b'Record successfully deleted', delete_response.data)


if __name__ == '__main__':
    unittest.main()