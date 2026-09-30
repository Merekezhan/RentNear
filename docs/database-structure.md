# RentNear — Initial Database Structure

## User
- id
- name
- email
- password
- phone

## Item
- id
- owner_id
- title
- description
- category
- price_per_day
- location
- availability

## Booking
- id
- renter_id
- item_id
- start_date
- end_date
- total_price
- status

## Initial Relationships
- One User can own many Items.
- One User can create many Bookings.
- One Item can have many Bookings.
- Each Booking belongs to one User and one Item.
