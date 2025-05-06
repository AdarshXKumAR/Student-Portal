-- Create database
CREATE DATABASE IF NOT EXISTS user_auth_db;

-- Use the database
USE user_auth_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    username VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create grades table
CREATE TABLE IF NOT EXISTS grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    grade CHAR(2) NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert sample grades data (for testing)
INSERT INTO grades (user_id, subject, score, grade) VALUES
(1, 'Computer Networks', 90, 'E'),
(1, 'Software Engineering', 88, 'E'),
(1, 'Deep Learning', 95, 'O'),
(1, 'Database Management System', 87, 'A+'),
(1, 'Operating System', 79, 'A+'),
(1, 'Web Technology Applications', 97, 'O');

INSERT INTO grades (user_id, subject, score, grade) VALUES
(2, 'Computer Networks', 90, 'E'),
(2, 'Software Engineering', 60, 'B'),
(2, 'Deep Learning', 95, 'O'),
(2, 'Database Management System', 87, 'A+'),
(2, 'Operating System', 69, 'B+'),
(2, 'Web Technology Applications', 97, 'O');

SELECT * FROM grades;

DROP table grades;