import unittest

from marshmallow import ValidationError
from app import create_app
from app.models import db, Customer


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(name="Test Customer", email="test@test.com", phone="0000000000")
        with self.app.app_context():
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
        return super().tearDown()
    
    def test_create_customer(self):
        payload = {
            "name": "John Doe",
            "phone": "1234567891",
            "email": "jd1@email.com"
        }

        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_create_invalid_customer(self):
        payload = {
            "name": "John Doe",
            "phone": "1234567891"
        }

        response = self.client.post('/customers/', json=payload)
        self.assertRaises(ValidationError) #Good Check
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json)

    def test_unique_email(self):
        payload = {
            "name": "John Doe",
            "phone": "1234567891",
            "email": "test@test.com"
        }

        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Email already taken.')

    def test_get_customers(self):

        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.json[0])

    