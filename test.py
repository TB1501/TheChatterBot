import unittest
import os
from app import app
from io import BytesIO

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_register_and_login(self):
        # Register
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        self.assertIn(b'Please log in', response.data)

        # Login
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        self.assertIn(b'chat', response.data)

    def test_upload_pdf(self):
        with open("testFile/example.pdf", "rb") as f:
            data = {
                'file': (BytesIO(f.read()), 'example.pdf')
            }
            response = self.client.post('/pdf', content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Successfully uploaded', response.data)

    def test_missing_pdf(self):
        response = self.client.post('/pdf', data={})
        self.assertEqual(response.status_code, 400)

    def test_ask_missing_query(self):
        response = self.client.post('/ask', json={})
        self.assertEqual(response.status_code, 400)

# Run the tests
if __name__ == '__main__':
    unittest.main()
