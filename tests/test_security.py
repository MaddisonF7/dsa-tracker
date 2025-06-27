import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from init import create_app
from configuration import TestConfig


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True

    # A02:2021 – Cryptographic Failures
    def test_password_hashing(self):
        password = "SecurePassword123!"
        hashed = generate_password_hash(password)
        self.assertNotEqual(password, hashed)
        self.assertTrue(check_password_hash(hashed, password))

    # A03:2021 – SQL Injection Protection
    def test_sql_injection_login_attempt(self):
        response = self.client.post('/', data={
            'email': "' OR '1'='1",
            'password': 'irrelevant'
        }, follow_redirects=True)
        self.assertIn(b'Invalid', response.data)

    # A07:2021 – Session Security
    def test_session_cookie_secure_flag_enabled(self):
        self.assertTrue(self.app.config['SESSION_COOKIE_SECURE'])

    def test_logout_clears_session(self):
        with self.client.session_transaction() as session:
            session['user'] = {
                'email': 'admin1@gmail.com',
                'role': 'Admin'
            }
        self.client.post('/logout', follow_redirects=True)
        with self.client.session_transaction() as session:
            self.assertNotIn('user', session)


if __name__ == "__main__":
    unittest.main()
