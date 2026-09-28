# RentNear — Initial API Structure

## Authentication
POST /api/auth/register — Register a new user  
POST /api/auth/login — Log in

## Users
GET /api/users/{id} — View user profile

## Items
GET /api/items — Get available items  
GET /api/items/{id} — View item details  
POST /api/items — Create an item listing

## Bookings
GET /api/bookings — View user's bookings  
POST /api/bookings — Create a booking  
GET /api/bookings/{id} — View booking details  
PATCH /api/bookings/{id} — Update booking status
