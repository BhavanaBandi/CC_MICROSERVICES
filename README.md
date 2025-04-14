# Cloud Computing Project - University Feedback & Parking System

## Subject: Cloud Computing
This project was developed as part of our Cloud Computing coursework. The aim was to design and deploy microservices for two university-centric domains:
- **Feedback Management System**
- **Parking Management System**

---

## Technologies Used

| Tool      | Purpose                        |
|-----------|--------------------------------|
| Python    | Backend service logic          |
| Flask     | API creation and routing       |
| Docker    | Containerization of services   |
| MySQL     | Database management            |

All services are containerized using Docker and interact with each other as independent microservices.

---

## Project Structure
.
├── db-init
│   ├── feedback.sql
│   └── parking.sql
├── docker-compose.yml
├── feedback_display
│   ├── Dockerfile
│   ├── app.py
│   ├── display.py
│   └── requirements.txt
├── feedback_submission
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── submissions.py
├── parking_service
│   ├── Dockerfile
│   ├── app.py
│   ├── parking_functions.py
│   └── requirements.txt
├── subscription_service
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── subscriptions_functions.py
├── tree.txt
└── vehicle_details_service
    ├── Dockerfile
    ├── app.py
    ├── requirements.txt
    └── vehicle_functions.py

7 directories, 24 files

---

## Microservices Overview

### 1 Feedback Display

#### Endpoints:
| Method | Endpoint                        | Description                                  |
|--------|----------------------------------|----------------------------------------------|
| GET    | `/`                              | Health check – confirms service is running   |
| GET    | `/feedback/<user_id>`           | Retrieve feedback entries for a user         |
| GET    | `/view-feedback`                | View all feedback entries                    |
| GET    | `/feedback-count/course`        | Get feedback count grouped by course         |
| GET    | `/feedback-count/faculty`       | Get feedback count grouped by faculty        |
| GET    | `/top-courses`                  | List courses with the highest feedback count |
| GET    | `/least-feedback-courses`       | List courses with the least feedback         |
| GET    | `/most-active-faculty`          | Identify faculty with most feedback entries  |
| GET    | `/recent-feedback`              | View the most recent feedback entries        |

---

### 2️ Feedback Submission

#### Endpoints:

| Method | Endpoint                     | Description                                           |
|--------|------------------------------|-------------------------------------------------------|
| GET    | `/`                          | Health check – confirms the service is running        |
| POST   | `/submit-student-feedback`   | Submit feedback from a student to a faculty           |
| POST   | `/submit-prof-feedback`      | Submit feedback from a faculty to a student           |
| POST   | `/submit-course-feedback`    | Submit feedback from a faculty about a course         |


---

### 3 Parking Service

#### Endpoints:
| Method | Endpoint            | Description                                           |
|--------|---------------------|-------------------------------------------------------|
| GET    | `/`                 | Service status check                                  |
| GET    | `/available-slots`  | Get available parking slots by type (or all)          |
| POST   | `/assign-parking`   | Assign a parking slot to a vehicle                    |
| POST   | `/unassign-parking` | Unassign a parking slot from a vehicle                |
| GET    | `/history`          | Retrieve parking history for a date range and user    |

---

### 4 Subscription Service

#### Endpoints:

| Method | Endpoint              | Description                        |
|--------|-----------------------|------------------------------------|
| GET    | `/`                   | Service status check               |
| POST   | `/create-subscription`| Create a new subscription          |
| POST   | `/create-payment`     | Initiate a new payment             |
| POST   | `/complete-payment`   | Complete an initiated payment      |

---

### 5 Vehicle Details

#### Endpoints:

| Method | Endpoint         | Description                                |
|--------|------------------|--------------------------------------------|
| GET    | `/`              | Service status check                       |
| POST   | `/register`      | Register a new vehicle                     |
| PUT    | `/update`        | Update registered vehicle information      |
| DELETE | `/remove`        | Remove a vehicle from the records          |
| GET    | `/check-vehicle` | Check details of a specific vehicle        |
---

##  Running the Project

Ensure Docker and Docker Compose are installed.

```bash
# Build and run all services
docker-compose up --build
