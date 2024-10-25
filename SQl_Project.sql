CREATE DATABASE StudentDB;

USE StudentDB;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(15) NOT NULL
);

INSERT INTO students (first_name, last_name, date_of_birth, gender, email, phone_number) 
VALUES 
('John', 'Doe', '2000-01-01', 'Male', 'john.doe@example.com', '1234567890'),
('Jane', 'Smith', '2001-02-02', 'Female', 'jane.smith@example.com', '0987654321');

SELECT * FROM students;


