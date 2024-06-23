# Appointment Manager

Appointment Manager is a web application designed to simplify the process of scheduling and managing appointments. Built with FastAPI for the backend (Streamlit for the frontend and MongoDB for the database will be added in the future). This application provides functionality for user authentication, appointment booking, and administrative controls. Users can create, update, and delete their appointments, while administrators have additional capabilities to manage users and view all appointments.

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

Build the Docker container:
```
docker build -t appointment-manager . -f Dockerfile
```

Run the Docker container:
```
docker run -p8000:8000 appointment-manager
```

Run unit and integration tests using:
```
pytest ./backend/unit_test.py 
pytest integration_test.py  
```

## Access

Once the containers are running, you can access the backend in your web browser at http://localhost:8000/docs

## Illustration

![image](https://github.com/EASS-HIT-PART-A-2024-CLASS-V/appointment-manager/assets/133001359/4b48f406-90bd-441d-9dce-4ee25791d5c6)

## Built with

**Backend** - Python, FastAPI


