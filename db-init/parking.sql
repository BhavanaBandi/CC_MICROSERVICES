CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role enum('faculty', 'student')
);

CREATE TABLE vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_number VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type ENUM('2 wheeler', '4 wheeler') NOT NULL
);

CREATE TABLE parking_slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('2 wheeler', '4 wheeler') NOT NULL,
    location VARCHAR(255) NOT NULL,
    slot_status ENUM('available', 'occupied') DEFAULT 'available'
);

CREATE TABLE assigned_slots (
    assign_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_id INT NOT NULL,
    vehicle_number varchar(20) NOT NULL,
    assigned_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    released_timestamp TIMESTAMP NULL,
    status ENUM('active', 'released') DEFAULT 'active'
);

CREATE TABLE subscriptions (
    sub_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plan_type ENUM('monthly', 'yearly') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    sub_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('card', 'UPI', 'net banking', 'cash') NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending'
);

INSERT INTO users (name, role) VALUES
('Alice Johnson', 'student'),
('Dr. Robert Smith', 'faculty'),
('Emily Davis', 'student'),
('Professor Karen Lee', 'faculty'),
('Michael Thompson', 'student'),
('Dr. Anita Sharma', 'faculty'),
('Sophie Martinez', 'student'),
('James Brown', 'student'),
('Professor Daniel Kim', 'faculty'),
('Isabella Chen', 'student');

INSERT INTO vehicles (user_id, vehicle_number, vehicle_type) VALUES
(1, 'MH12AB1234', '2 wheeler'),
(2, 'KA05CD5678', '4 wheeler'),
(3, 'DL8CAF3456', '2 wheeler'),
(4, 'TN09XY7890', '4 wheeler'),
(5, 'GJ01GH4321', '2 wheeler'),
(6, 'MH14MN0987', '4 wheeler'),
(7, 'RJ19QR7654', '2 wheeler'),
(8, 'UP32ZX1122', '4 wheeler'),
(9, 'KL07AS3344', '2 wheeler'),
(10, 'WB24RT5566', '4 wheeler');

INSERT INTO parking_slots (type, location, slot_status) VALUES
('2 wheeler', 'Ground 1', 'available'),
('4 wheeler', 'Ground 1', 'available'),
('2 wheeler', 'Ground 1', 'available'),
('4 wheeler', 'Ground 1', 'available'),
('2 wheeler', 'Ground 1', 'available'),
('4 wheeler', 'Ground 1', 'available'),
('2 wheeler', 'Ground 1', 'available'),
('4 wheeler', 'Ground 1', 'available'),
('2 wheeler', 'Ground 1', 'available'),
('4 wheeler', 'Ground 1', 'available'),

('2 wheeler', 'Basement 1', 'available'),
('4 wheeler', 'Basement 1', 'available'),
('2 wheeler', 'Basement 1', 'available'),
('4 wheeler', 'Basement 1', 'available'),
('2 wheeler', 'Basement 1', 'available'),
('4 wheeler', 'Basement 1', 'available'),
('2 wheeler', 'Basement 1', 'available'),
('4 wheeler', 'Basement 1', 'available'),
('2 wheeler', 'Basement 1', 'available'),
('4 wheeler', 'Basement 1', 'available'),

('2 wheeler', 'Basement 2', 'available'),
('4 wheeler', 'Basement 2', 'available'),
('2 wheeler', 'Basement 2', 'available'),
('4 wheeler', 'Basement 2', 'available'),
('2 wheeler', 'Basement 2', 'available'),
('4 wheeler', 'Basement 2', 'available'),
('2 wheeler', 'Basement 2', 'available'),
('4 wheeler', 'Basement 2', 'available'),
('2 wheeler', 'Basement 2', 'available'),
('4 wheeler', 'Basement 2', 'available');
