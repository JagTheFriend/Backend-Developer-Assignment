import unittest
from assignment import app
import os
import json
from random import randint


class FlaskAPITestCase(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_booking_retreat(self):
        data = {
            "user_id": f"{randint(1000, 9999)}",
            "user_name": "Dane",
            "user_email": "fake_email@fake_mail.com",
            "user_phone": f"{randint(1000, 9999)}",
            "retreat_id": f"{randint(1000, 9999)}",
            "retreat_title": "De-engineered fresh-thinking protocol",
            "retreat_location": "Pune",
            "retreat_price": f"{randint(100, 999)}",
            "retreat_duration": f"{randint(1, 10)}",
            "payment_details": "Home Loan Account",
            "booking_date": f"{randint(1000, 4000)}",
        }

        response = self.client.post("/book", json=data)
        self.assertEqual(response.status_code, 201)

        # Should return 409 since user has already booked
        response = self.client.post("/book", json=data)
        self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
