import unittest

from marshmallow import ValidationError
from app import create_app
from app.models import db, Mechanic
from werkzeug.security import generate_password_hash
from app.utils.auth import encode_token


class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(name="Test Mechanic", email="test@test.com", phone="0000000000", salary=100000.00, password=generate_password_hash('123')) #Need to manually generate hashed password
        with self.app.app_context():
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
        return super().tearDown()
    
    def test_mechanic_login(self):
        payload = {
            "email": "test@test.com",
            "password": '123'
        }

        response = self.client.post('/mechanics/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
    

    def test_mechanic_update(self):
        update_payload = {
            "name": "Test Mechanic",
            "email": "changed@test.com",
            "phone": "0000000000",
            "salary": 100000.00
        }

        headers = {'Authorization': "Bearer " + self.token}

        response = self.client.put('/mechanics/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'changed@test.com')
    
    def test_mechanic_delete(self):
        headers = {'Authorization': "Bearer " + self.token}

        response = self.client.delete('/mechanics/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 'mechanic deleted')

    

