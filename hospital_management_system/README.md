# Hospital Management System (Flask + MySQL)

A simple DBMS mini project that integrates a website with a MySQL database.

## Features
- Admin login
- Dashboard with counts
- Patient CRUD
- Doctor CRUD
- Appointment CRUD
- Search for patients and doctors
- JOIN query for appointment list

## Tools Used
- Python
- Flask
- MySQL
- Bootstrap 5

## Database Tables
- admin
- patients
- doctors
- appointments

## How to Run
1. Install Python and MySQL.
2. Open terminal in this project folder.
3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create the database by importing `hospital_db.sql` into MySQL or phpMyAdmin.
5. Update database credentials in `config.py`:
   - MYSQL_HOST
   - MYSQL_USER
   - MYSQL_PASSWORD
   - MYSQL_DATABASE
6. Run the Flask app:
   ```bash
   python app.py
   ```
7. Open in browser:
   ```
   http://127.0.0.1:5000
   ```

## Demo Login
- Username: admin
- Password: admin123

## DBMS Concepts Used
- Primary Key
- Foreign Key
- CRUD Operations
- JOIN Query
- Relational Database Design
