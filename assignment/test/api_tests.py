import unittest
from .. import app
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

    def test_double_booking(self):
        json_data = {
            # User details
            "user_id": f"{randint(1000, 9999)}",
            "user_name": "Jag",
            "user_email": "JagTheFriend12@gmail.com",
            "user_phone": f"{randint(1000, 9999)}",
            # Retreat details
            "retreat_title": "Hello",
            "retreat_location": "Pune",
            "retreat_price": f"{randint(100, 300)}",
            "retreat_duration": f"{randint(1, 9)}",
            "retreat_id": f"{randint(1000, 9999)}",
            # Payment details
            "payment_details": "details",
            "booking_date": f"{randint(1000, 9990)}",
        }

        response = self.client.post(
            "/book", json=json_data, content_type="application/json"
        )
        # It should pass the first time
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            "/book", json=json_data, content_type="application/json"
        )
        # It should fail the second time since the user has already booked the retreat
        self.assertEqual(response.status_code, 409)

    def test_filter_by_tag(self):
        response = self.client.get("/retreats?filter=Stress")
        response_data = [
            {
                "condition": "Stress Relief",
                "date": 1692921600,
                "description": "A weekend retreat focused on yoga and meditation to relieve stress.",
                "duration": 3,
                "id": 1,
                "image": "https://cdn.midjourney.com/a287f9bc-d0fb-4e78-a0fa-e8136d3c408a/0_0.jpeg",
                "location": "Goa",
                "price": 200,
                "tags": ["relaxation", "meditation", "weekend"],
                "title": "Yoga for Stress Relief",
                "type": "Signature",
            },
            {
                "condition": "Stress Relief",
                "date": 1727628942,
                "description": "A description for Yoga Event 18.",
                "duration": 2,
                "id": 18,
                "image": "https://cdn.midjourney.com/873b60f7-f026-40f9-b2d7-184e981ee1f5/0_3.jpeg",
                "location": "Goa",
                "price": 414,
                "tags": ["weight loss", "workshop", "pain management"],
                "title": "Yoga Event 18",
                "type": "Standalone",
            },
            {
                "condition": "Stress Relief",
                "date": 1725581902,
                "description": "A description for Yoga Event 20.",
                "duration": 2,
                "id": 20,
                "image": "https://cdn.midjourney.com/5d5f32ef-c40a-4258-9856-85db2f4f943a/0_0.jpeg",
                "location": "Varanasi",
                "price": 142,
                "tags": ["weight loss", "camp", "yoga"],
                "title": "Yoga Event 20",
                "type": "Signature",
            },
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(response.get_json()), json.dumps(response_data))

    def test_filter_by_title(self):
        response = self.client.get("/retreats?title=Wellness")
        response_data = [
            {
                "condition": "Mental Wellness",
                "date": 1701734400,
                "description": "A 4-day retreat focused on mental wellness through yoga and meditation.",
                "duration": 4,
                "id": 6,
                "image": "https://cdn.midjourney.com/32923aeb-db8c-4c27-8e9d-fb82928b7fc1/0_2.jpeg",
                "location": "Pune",
                "price": 400,
                "tags": ["mental wellness", "meditation", "yoga"],
                "title": "Mental Wellness Retreat",
                "type": "Standalone",
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(response.get_json()), json.dumps(response_data))

    def test_filter_by_duration(self):
        response = self.client.get("/retreats?duration=5")
        response_data = [
            {
                "condition": "Flexibility Improvement",
                "date": 1694304000,
                "description": "A 5-day workshop designed to improve flexibility through yoga.",
                "duration": 5,
                "id": 2,
                "image": "https://cdn.midjourney.com/4eef5d57-1601-4b80-8e82-523003e9f95d/0_0.jpeg",
                "location": "Rishikesh",
                "price": 500,
                "tags": ["flexibility", "yoga", "workshop"],
                "title": "Flexibility Improvement Workshop",
                "type": "Standalone",
            },
            {
                "condition": "Detox",
                "date": 1699574400,
                "description": "A 5-day detox retreat to cleanse the body and mind.",
                "duration": 5,
                "id": 8,
                "image": "https://cdn.midjourney.com/873b60f7-f026-40f9-b2d7-184e981ee1f5/0_3.jpeg",
                "location": "Hyderabad",
                "price": 550,
                "tags": ["detox", "cleanse", "yoga"],
                "title": "Detox Retreat",
                "type": "Signature",
            },
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(response.get_json()), json.dumps(response_data))

    def test_filter_by_type(self):
        response = self.client.get("/retreats?type=Standalone")
        response_data = [
            {
                "condition": "Flexibility Improvement",
                "date": 1694304000,
                "description": "A 5-day workshop designed to improve flexibility through yoga.",
                "duration": 5,
                "id": 2,
                "image": "https://cdn.midjourney.com/4eef5d57-1601-4b80-8e82-523003e9f95d/0_0.jpeg",
                "location": "Rishikesh",
                "price": 500,
                "tags": ["flexibility", "yoga", "workshop"],
                "title": "Flexibility Improvement Workshop",
                "type": "Standalone",
            },
            {
                "condition": "General Fitness",
                "date": 1694736000,
                "description": "A 3-day yoga camp to enhance overall fitness and well-being.",
                "duration": 3,
                "id": 4,
                "image": "https://cdn.midjourney.com/930ec767-aa6d-46e6-92a6-f019a9718304/0_3.jpeg",
                "location": "Mumbai",
                "price": 300,
                "tags": ["fitness", "yoga", "camp"],
                "title": "General Fitness Yoga Camp",
                "type": "Standalone",
            },
            {
                "condition": "Mental Wellness",
                "date": 1701734400,
                "description": "A 4-day retreat focused on mental wellness through yoga and meditation.",
                "duration": 4,
                "id": 6,
                "image": "https://cdn.midjourney.com/32923aeb-db8c-4c27-8e9d-fb82928b7fc1/0_2.jpeg",
                "location": "Pune",
                "price": 400,
                "tags": ["mental wellness", "meditation", "yoga"],
                "title": "Mental Wellness Retreat",
                "type": "Standalone",
            },
            {
                "condition": "Pre/Post-Natal",
                "date": 1693872000,
                "description": "A specialized yoga program for pre and post-natal women.",
                "duration": 3,
                "id": 7,
                "image": "https://cdn.midjourney.com/1bf1a655-289a-48e4-a156-0dde0cf1b7ce/0_1.jpeg",
                "location": "Chennai",
                "price": 350,
                "tags": ["pre-natal", "post-natal", "yoga"],
                "title": "Pre/Post-Natal Yoga",
                "type": "Standalone",
            },
            {
                "condition": "General Fitness",
                "date": 1695168000,
                "description": "A 3-day yoga camp to enhance overall fitness and well-being.",
                "duration": 3,
                "id": 10,
                "image": "https://cdn.midjourney.com/5d5f32ef-c40a-4258-9856-85db2f4f943a/0_0.jpeg",
                "location": "Kolkata",
                "price": 350,
                "tags": ["fitness", "yoga", "camp"],
                "title": "General Fitness Yoga Camp",
                "type": "Standalone",
            },
            {
                "condition": "Mental Wellness",
                "date": 1734056561,
                "description": "A description for Yoga Event 14.",
                "duration": 7,
                "id": 14,
                "image": "https://cdn.midjourney.com/e6c8452a-af8e-4cd3-b15a-c3dcf2a696a5/0_3.jpeg",
                "location": "Chennai",
                "price": 107,
                "tags": ["workshop", "weight loss", "meditation"],
                "title": "Yoga Event 14",
                "type": "Standalone",
            },
            {
                "condition": "Mental Wellness",
                "date": 1734972658,
                "description": "A description for Yoga Event 17.",
                "duration": 6,
                "id": 17,
                "image": "https://cdn.midjourney.com/2f72aafd-e2f2-4bec-8afc-80877aa4634f/0_0.jpeg",
                "location": "Goa",
                "price": 555,
                "tags": ["yoga", "camp", "weekend"],
                "title": "Yoga Event 17",
                "type": "Standalone",
            },
            {
                "condition": "Stress Relief",
                "date": 1727628942,
                "description": "A description for Yoga Event 18.",
                "duration": 2,
                "id": 18,
                "image": "https://cdn.midjourney.com/873b60f7-f026-40f9-b2d7-184e981ee1f5/0_3.jpeg",
                "location": "Goa",
                "price": 414,
                "tags": ["weight loss", "workshop", "pain management"],
                "title": "Yoga Event 18",
                "type": "Standalone",
            },
            {
                "condition": "Mental Wellness",
                "date": 1732255454,
                "description": "A description for Yoga Event 19.",
                "duration": 7,
                "id": 19,
                "image": "https://cdn.midjourney.com/e0dba42d-84bc-45e6-acca-bbaf8f817371/0_1.jpeg",
                "location": "Rishikesh",
                "price": 219,
                "tags": ["diet", "weekend", "flexibility"],
                "title": "Yoga Event 19",
                "type": "Standalone",
            },
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(response.get_json()), json.dumps(response_data))

    def test_filter_by_location(self):
        response = self.client.get("/retreats?location=Pune")
        response_data = [
            {
                "condition": "Mental Wellness",
                "date": 1701734400,
                "description": "A 4-day retreat focused on mental wellness through yoga and meditation.",
                "duration": 4,
                "id": 6,
                "image": "https://cdn.midjourney.com/32923aeb-db8c-4c27-8e9d-fb82928b7fc1/0_2.jpeg",
                "location": "Pune",
                "price": 400,
                "tags": ["mental wellness", "meditation", "yoga"],
                "title": "Mental Wellness Retreat",
                "type": "Standalone",
            },
            {
                "condition": "Chronic Pain Management",
                "date": 1723566880,
                "description": "A description for Yoga Event 11.",
                "duration": 10,
                "id": 11,
                "image": "https://cdn.midjourney.com/ec4680e8-d074-4a69-a24b-3d3f3946907b/0_2.jpeg",
                "location": "Pune",
                "price": 704,
                "tags": ["yoga", "camp", "weekend"],
                "title": "Yoga Event 11",
                "type": "Signature",
            },
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(response.get_json()), json.dumps(response_data))

    def test_filter_by_search(self):
        response = self.client.get("/retreats?search=Flexibility")
        response_data = [
            {
                "condition": "Flexibility Improvement",
                "date": 1694304000,
                "description": "A 5-day workshop designed to improve flexibility through yoga.",
                "duration": 5,
                "id": 2,
                "image": "https://cdn.midjourney.com/4eef5d57-1601-4b80-8e82-523003e9f95d/0_0.jpeg",
                "location": "Rishikesh",
                "price": 500,
                "tags": ["flexibility", "yoga", "workshop"],
                "title": "Flexibility Improvement Workshop",
                "type": "Standalone",
            },
            {
                "condition": "Flexibility Improvement",
                "date": 1725472451,
                "description": "A description for Yoga Event 16.",
                "duration": 3,
                "id": 16,
                "image": "https://cdn.midjourney.com/2f9daef3-406b-4266-835e-a07fb09b4820/0_0.jpeg",
                "location": "Delhi",
                "price": 311,
                "tags": ["relaxation", "spiritual growth", "flexibility"],
                "title": "Yoga Event 16",
                "type": "Signature",
            },
            {
                "condition": "Mental Wellness",
                "date": 1732255454,
                "description": "A description for Yoga Event 19.",
                "duration": 7,
                "id": 19,
                "image": "https://cdn.midjourney.com/e0dba42d-84bc-45e6-acca-bbaf8f817371/0_1.jpeg",
                "location": "Rishikesh",
                "price": 219,
                "tags": ["diet", "weekend", "flexibility"],
                "title": "Yoga Event 19",
                "type": "Standalone",
            },
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(response.get_json()), json.dumps(response_data))


if __name__ == "__main__":
    unittest.main()
