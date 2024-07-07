# Hair And Nail Salon Appointment Manager

Hair And Nail Salon Appointment Manager is a web application designed to simplify the process of scheduling and managing appointments. Built with FastAPI for the backend and Streamlit for the frontend (MongoDB for the database will be added in the future). This application provides functionality for user authentication, appointment booking, and administrative controls. Users can create, update, and delete their appointments, while administrators have additional capabilities to manage users and view all appointments.

## Features

### Users and Admins:

- Registration and Login
- Get user's information
- Create appointment
- Update appointment
- Delete appointment

### Admins:

- Get all users
- Delete users
- Get appointments for specific user by phone number
- Get appointments for specific month


## Prerequisites

- Docker


## Installation

Clone the project using:
```
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-V/appointment-manager.git
```

Go to project directory:
```
cd appointment-manager 
```

Build the Docker containers:
```
docker-compose up --build
```

Run unit and integration tests using:
```
pytest ./backend/unit_test.py 
pytest integration_test.py  
```

## Access

- Access the frontend at http://localhost:8501/
- Access the backend at http://localhost:8000/docs

## Illustration

![image](https://github.com/EASS-HIT-PART-A-2024-CLASS-V/appointment-manager/assets/133001359/4b48f406-90bd-441d-9dce-4ee25791d5c6)

## Built with

- **Backend** - Python, FastAPI 
- **Frontend** - Streamlit


