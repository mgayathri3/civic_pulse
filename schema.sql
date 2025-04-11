-- Database schema for CivicPulse

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Departments table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Authorities table (admin users)
CREATE TABLE IF NOT EXISTS authorities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    department_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Complaints table
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference_id VARCHAR(20) UNIQUE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    landmark VARCHAR(255),
    contact_info VARCHAR(100),
    status ENUM('New', 'Assigned', 'In Progress', 'Resolved') DEFAULT 'New',
    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    department_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Complaint updates table (for timeline)
CREATE TABLE IF NOT EXISTS complaint_updates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE
);

-- Complaint images table
CREATE TABLE IF NOT EXISTS complaint_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE
);

-- Insert default departments
INSERT INTO departments (name, description) VALUES
('Sanitation', 'Responsible for waste management and cleanliness'),
('Roads & Transport', 'Manages road infrastructure and public transportation'),
('Water Services', 'Handles water supply and sewage systems'),
('Parks & Recreation', 'Maintains public parks and recreational facilities'),
('Police Department', 'Ensures public safety and law enforcement'),
('Electricity Services', 'Manages electrical infrastructure and power supply'),
('Health Department', 'Oversees public health initiatives and medical services');

-- Insert sample data for testing
INSERT INTO users (name, email, password) VALUES
('John Doe', 'john@example.com', 'pbkdf2:sha256:150000$abc123$abcdef123456789'),
('Jane Smith', 'jane@example.com', 'pbkdf2:sha256:150000$def456$ghijkl789012345');

INSERT INTO authorities (name, email, password, department_id) VALUES
('Admin User', 'admin@civicpulse.com', 'pbkdf2:sha256:150000$xyz789$mnopqr456789012', 1);

