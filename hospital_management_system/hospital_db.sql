CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS admin;

CREATE TABLE admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    phone VARCHAR(15) NOT NULL,
    address TEXT NOT NULL,
    disease VARCHAR(255) NOT NULL
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    room_no VARCHAR(10) NOT NULL
);

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Scheduled',
    CONSTRAINT fk_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    CONSTRAINT fk_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

INSERT INTO admin (username, password) VALUES
('admin', 'admin123');

INSERT INTO patients (name, age, gender, phone, address, disease) VALUES
('Rahul Sharma', 28, 'Male', '9876543210', 'Rourkela, Odisha', 'Fever'),
('Priya Das', 34, 'Female', '9123456780', 'Bhubaneswar, Odisha', 'Diabetes'),
('Aman Verma', 42, 'Male', '9988776655', 'Cuttack, Odisha', 'Back Pain');

INSERT INTO doctors (name, specialization, phone, room_no) VALUES
('Anil Mehta', 'Cardiology', '9876501234', 'A101'),
('Sonia Roy', 'Neurology', '9765401234', 'B205'),
('Ritesh Sen', 'General Medicine', '9654301234', 'C110');

INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status) VALUES
(1, 3, '2026-04-20', '10:00:00', 'Scheduled'),
(2, 1, '2026-04-21', '12:30:00', 'Completed'),
(3, 2, '2026-04-22', '09:15:00', 'Cancelled');
