-- MySQL Database Setup Script for Restro Backend
-- Run this in MySQL Workbench or MySQL command line

-- Create the database
CREATE DATABASE IF NOT EXISTS restro_backend;

-- Use the database
USE restro_backend;

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_roles_name (name)
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_phone (phone_number),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Insert default roles
INSERT IGNORE INTO roles (name, description) VALUES 
('admin', 'Administrator role with full access'),
('employee', 'Employee role with limited access'),
('customer', 'Customer role for restaurant customers');

-- Show the created tables
SHOW TABLES;

-- Show the roles
SELECT * FROM roles;
