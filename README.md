# Hair And Nail Salon Appointment Manager

Hair And Nail Salon Appointment Manager is a web application designed to simplify the process of scheduling and managing appointments for hair and nail salons. Built with FastAPI for the backend, Streamlit for the frontend, and MongoDB as the database, this application provides functionality for user authentication, appointment booking, and administrative controls. Users can create, update, and delete their appointments, while administrators have additional capabilities to manage users, view, update, and delete all appointments.

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
- Docker Compose
- Python
- pytest


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

## How to Use

#### Access the frontend at [http://localhost:8501/](http://localhost:8501/)
- Register as a user and log in to start booking appointments.
  
- To log in as an admin and manage users and appointments, use the following credentials: <br />
  Phone: `admin` <br />
  Password: `admin`

#### Access the backend API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)


## Testing 
To run the tests:

1. Make sure the Docker containers are up and running (`docker-compose up --build`).
2. Open a new terminal.
3. Make sure you are in the project directory (`cd appointment-manager`).
4. Set environment variables for the test database:
```
export MONGO_URL='mongodb://admin:admin@localhost:27017'
export DATABASE_NAME='appointment_manager_test'
```
5. Run the tests
```
pytest ./backend/tests/unit_test.py
pytest ./backend/tests/integration_test.py
```

## Video Demo

#### https://www.youtube.com/watch?v=Rz4gto2uwWw


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Rz4gto2uwWw/0.jpg)](https://www.youtube.com/watch?v=Rz4gto2uwWw)


## Illustration

![image](https://github.com/user-attachments/assets/4e35f1ae-183e-4c23-8a1a-11f8f62bb19e)



## Built with

- **Backend** - Python, FastAPI 
- **Frontend** - Streamlit
- **Database** - MongoDB


