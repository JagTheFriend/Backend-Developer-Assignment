# Backend Developer Assignment

## Description

This is a basic backend service to manage retreat data for a fictional wellness retreat platform built with Flask and SQLAlchemy.

## Using the API

### Retreats

To Fetch all retreats:

```bash
curl -X GET http://localhost:5000/retreats
```

To filter retreats by tag:

```bash
curl -X GET http://localhost:5000/retreats?filter=Stress
```

To filter retreats by location:

```bash
curl -X GET http://localhost:5000/retreats?location=Mumbai
```

To search retreats:

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
}' 'http://localhost:5000/retreats/book'
```

#### Business Logic

- Don't allow user to double book a retreat

## Tech Stack

- [Flask](https://flask.palletsprojects.com/en/3.0.x/): To run the web application (API)
- [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/): To interact with the database

## Running the application

To simply run the application, you can use the following command:

```bash
docker compose up
```

This will start the application on port 5000.
You can access the application by navigating to <http://localhost:5000> in your web browser.
