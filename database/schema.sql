# Create database
CREATE DATABASE dsa_tracker;
USE dsa_tracker;
# Create user table to store login credentials
CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'Apprentice') NOT NULL,
    line_manager_id INT NULL,
    cohort INT NULL,
    start_date DATE NULL,
    end_date DATE NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (line_manager_id) REFERENCES User(id)
);
# Create project table to store what each apprentice is working on
CREATE TABLE Project (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    status ENUM('Ongoing', 'Completed') DEFAULT 'Ongoing' NOT NULL,
    apprentice_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (apprentice_id) REFERENCES User(id)
);
# Create exam table to store exam progress
CREATE TABLE Exam (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    exam_date DATE NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Unsuccessful') DEFAULT 'Scheduled' NOT NULL,
    apprentice_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (apprentice_id) REFERENCES User(id)
);
# Create leave table for storing time off
CREATE TABLE Leave_Request (
    id INT AUTO_INCREMENT PRIMARY KEY,
    apprentice_id INT NOT NULL,
    leave_type ENUM('Sick', 'Annual', 'Maternity', 'Paternity', 'Unpaid', 'Other') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (apprentice_id) REFERENCES User(id)
);