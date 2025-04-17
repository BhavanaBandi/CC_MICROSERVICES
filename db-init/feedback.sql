create table student 
(stu_id varchar(15) primary key not null,
stu_name varchar(50) not null);

create table professor
(prof_id varchar(15) primary key not null,
prof_name varchar(50) not null);

CREATE TABLE stu_feedback (
stu_feed_id INT AUTO_INCREMENT PRIMARY KEY,
stu_id VARCHAR(15) NOT NULL,
prof_id VARCHAR(15) NOT NULL,
feedback_given_by_student VARCHAR(100),
time_of_feed_stu DATETIME,
CONSTRAINT fk_stu_feedback_student FOREIGN KEY (stu_id) REFERENCES student(stu_id) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT fk_stu_feedback_professor FOREIGN KEY (prof_id) REFERENCES professor(prof_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE prof_feedback (
prof_feed_id INT AUTO_INCREMENT PRIMARY KEY,
prof_id VARCHAR(15) NOT NULL,
stu_id VARCHAR(15) NOT NULL,
feedback_given_by_prof VARCHAR(100),
time_of_feed_prof DATETIME,
CONSTRAINT fk_prof_feedback_professor FOREIGN KEY (prof_id) REFERENCES professor(prof_id) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT fk_prof_feedback_student FOREIGN KEY (stu_id) REFERENCES student(stu_id) ON DELETE CASCADE ON UPDATE CASCADE
);

create table faculty
(id varchar(20) primary key not null,
name varchar(50) not null,
password varchar(50) not null,
role varchar(20) not null);

create table course_feedback 
(id int auto_increment primary key,
faculty_id varchar(20) not null,
course_id varchar(20) not null,
feedback_text varchar(200) not null,
timestamp datetime not null);

INSERT INTO student (stu_id, stu_name) VALUES
('S1001', 'Emily Carter'),
('S1002', 'James Wilson'),
('S1003', 'Ava Patel'),
('S1004', 'Liam Nguyen'),
('S1005', 'Sophia Ramirez'),
('S1006', 'Ethan Scott'),
('S1007', 'Isabella Lopez'),
('S1008', 'Noah Khan'),
('S1009', 'Mia Zhang'),
('S1010', 'Lucas Adams');

INSERT INTO professor (prof_id, prof_name) VALUES
('P2001', 'Dr. Robert Smith'),
('P2002', 'Dr. Anita Sharma'),
('P2003', 'Professor Karen Lee'),
('P2004', 'Dr. Daniel Kim'),
('P2005', 'Professor Susan Clark'),
('P2006', 'Dr. Rajesh Verma'),
('P2007', 'Professor Linda Moore'),
('P2008', 'Dr. Thomas Nguyen'),
('P2009', 'Dr. Aisha Khan'),
('P2010', 'Professor David Chen');

INSERT INTO stu_feedback (stu_id, prof_id, feedback_given_by_student, time_of_feed_stu) VALUES
('S1001', 'P2001', 'Very engaging lectures and helpful guidance.', '2025-04-10 09:30:00'),
('S1003', 'P2004', 'Explains concepts clearly and with real-world examples.', '2025-04-11 11:45:00'),
('S1005', 'P2002', 'Helpful during project work, always available for queries.', '2025-04-12 14:20:00');

INSERT INTO prof_feedback (prof_id, stu_id, feedback_given_by_prof, time_of_feed_prof) VALUES
('P2001', 'S1001', 'Shows great interest and asks insightful questions.', '2025-04-11 10:00:00'),
('P2002', 'S1005', 'Consistent performance and active in discussions.', '2025-04-12 15:10:00'),
('P2004', 'S1003', 'Needs to participate more actively in class.', '2025-04-13 13:30:00');

INSERT INTO faculty (id, name, password, role) VALUES
('F001', 'Dr. Robert Smith', 'pass1234', 'professor'),
('F002', 'Professor Karen Lee', 'teach2024', 'professor'),
('F003', 'Dr. Anita Sharma', 'sharma@321', 'head'),
('F004', 'Professor Linda Moore', 'moore456', 'dean'),
('F005', 'Dr. Daniel Kim', 'kimsecure!', 'professor');

INSERT INTO course_feedback (faculty_id, course_id, feedback_text, timestamp) VALUES
('F001', 'CSE101', 'Great course structure and excellent delivery by the faculty.', '2025-04-10 10:15:00'),
('F002', 'ECE202', 'Very informative sessions, but pacing was a bit fast.', '2025-04-11 13:45:00'),
('F003', 'MATH301', 'Well-organized lectures and helpful course materials.', '2025-04-12 09:30:00'),
('F005', 'PHY105', 'Faculty explained complex topics in a simplified way.', '2025-04-13 15:20:00');
