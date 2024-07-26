# Backend Developer Assignment

## Description

This is a basic backend service to manage retreat data for a fictional wellness retreat platform built with Flask and SQLAlchemy.

## Using the API

### Retreats

Fetch all retreats:

```bash
curl -X GET http://localhost:5000/retreats
```

Filter retreats by tag:

```bash
curl -X GET http://localhost:5000/retreats?filter=Stress
```

Filter retreats by title:

```bash
curl -X GET http://localhost:5000/retreatstitle=Yoga%20Event%2019
```

Filter retreats by type:

```bash
curl -X GET http://localhost:5000/retreats?type=Signature
```

Filter retreats by duration:

```bash
curl -X GET http://localhost:5000/retreats?duration=3
```

Filter retreats by location:

```bash
curl -X GET http://localhost:5000/retreats?location=Mumbai
```

Search retreats:

```bash
curl -X GET http://localhost:5000/retreats?search=Fitness
```

Pagination Example:

```bash
curl -X GET http://localhost:5000/retreats?page=2&limit=3
```

### Booking for a retreat

Create a booking:

```bash
curl -X POST -H "Content-type: application/json" -d '{
    "user_id": "1232",
    "user_name": "Jag",
    "user_email": "JagTheFriend12@gmail.com",
    "user_phone": "445678",
    "retreat_id": "1232",
    "retreat_title": "Hello",
    "retreat_location": "Pune",
    "retreat_price": "250",
    "retreat_duration": "3",
    "payment_details": "details",
    "booking_date": "1233"
}' 'http://localhost:5000/book'
```

#### Business Logic

- It allows user to book multiple retreats
- It doesn't allow user to double book the same retreat

## Tech Stack

- [Flask](https://flask.palletsprojects.com/en/3.0.x/): To run the web application (API)
- [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/): To interact with the database

## Running the application

### Docker

To simply run the application, you can use the following command:

```bash
docker compose up
```

This will start the application on port 5000.\
You can access the application by navigating to <http://localhost:5000> in your web browser.

### Manually

1. Clone the repository
2. Run `pip install poetry`
3. Install the dependencies `poetry install`
4. Run the application `python main.py`

You can access the application by navigating to <http://localhost:5000> in your web browser.

### Replit

[![Run on Replit](https://replit.com/badge/github/jagtah/backend-developer-assignment)](https://replit.com/@JagTheFriend/Backend-Developer-Assignment)

## Testing

You can run the tests using the following command:

```bash
python -m unittest test/__init__.py
```
