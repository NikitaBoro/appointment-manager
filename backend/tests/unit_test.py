import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient
import sys

sys.path.append("./backend")
from backend.main import app

# Use a separate database for tests
client_for_test = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
test_db = client_for_test["appointment_manager_test"]
test_users_collection = test_db["users"]
test_appointments_collection = test_db["appointments"]


# Helper function to register a user
async def register_user(
    phone: str = "1234567890",
    full_name: str = "Test User",
    email: str = "test@example.com",
    password: str = "password123",
    role: str = "user",
):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/v1/register",
            json={"phone": phone, "full_name": full_name, "email": email, "role": role},
            params={"password": password},
        )
    return response


# Helper function to login and get token
async def login_user(phone: str, password: str):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/v1/token", data={"username": phone, "password": password}
        )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# Helper function to create an appointment
async def create_appointment(
    token_headers: dict,
    appointment_data: dict = {
        "id": 0,
        "name": "Test User",
        "phone": "1234567890",
        "date": "17-10-2025",
        "time": "10:00",
        "service": "Manicure",
    },
):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/v1/appointments", json=appointment_data, headers=token_headers
        )
    return response


# Helper function to clear database
async def clean_test_db():
    test_appointments_collection.delete_many({})
    test_users_collection.delete_many({})


# User Tests -----------------------------------------------------------------------------------------------------


# Test user registration
@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/v1/register",
            json={
                "phone": "1234567890",
                "full_name": "Test User",
                "email": "test@example.com",
                "role": "user",
            },
            params={"password": "password123"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "1234567890"
    assert data["full_name"] == "Test User"
    assert data["email"] == "test@example.com"

    user_in_db = await test_users_collection.find_one({"phone": "1234567890"})
    assert user_in_db is not None
    assert user_in_db["full_name"] == "Test User"
    assert user_in_db["email"] == "test@example.com"

    await clean_test_db()  # Clean test database


# Test login for access token
@pytest.mark.asyncio
async def test_login_for_access_token():
    await register_user()
    user_data = {"username": "1234567890", "password": "password123"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/token", data=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    await clean_test_db()  # Clean test database


# Test get current user info
@pytest.mark.asyncio
async def test_read_users_me():
    # Register user and login
    await register_user()
    headers = await login_user("1234567890", "password123")

    # Get user info
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "1234567890"
    assert data["full_name"] == "Test User"

    await clean_test_db()  # Clean test database


# Test create appointment
@pytest.mark.asyncio
async def test_create_appointment():
    # Register and login user:
    await register_user()
    headers = await login_user("1234567890", "password123")

    # Create an appointmnet:
    response = await create_appointment(headers)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "1234567890"
    assert data["name"] == "Test User"
    assert data["date"] == "17-10-2025"
    assert data["time"] == "10:00"
    assert data["service"] == "Manicure"

    await clean_test_db()  # Clean test database


# Test get appointments
@pytest.mark.asyncio
async def test_get_appointments():
    # Register and login user:
    await register_user()
    headers = await login_user("1234567890", "password123")

    # Create an appointmnet:
    await create_appointment(headers)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/appointments", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["phone"] == "1234567890"
    assert data[0]["name"] == "Test User"
    assert data[0]["date"] == "17-10-2025"
    assert data[0]["time"] == "10:00"
    assert data[0]["service"] == "Manicure"

    await clean_test_db()  # Clean test database


# Test to update appointment
@pytest.mark.asyncio
async def test_update_appointment():
    # Register and login user::
    await register_user()
    headers = await login_user("1234567890", "password123")

    # Create an appointmnet:
    create_response = await create_appointment(headers)
    assert create_response.status_code == 200
    appointment_id = create_response.json()["id"]

    # Update appointment
    async with AsyncClient(app=app, base_url="http://test") as ac:
        update_response = await ac.put(
            f"/v1/appointments/{appointment_id}",
            json={
                "id": appointment_id,
                "name": "Test User",
                "phone": "1234567890",
                "date": "18-10-2025",
                "time": "11:00",
                "service": "Pedicure",
            },
            headers=headers,
        )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Test User"
    assert data["date"] == "18-10-2025"
    assert data["time"] == "11:00"
    assert data["service"] == "Pedicure"

    await clean_test_db()  # Clean test database


# Test to delete appointment
@pytest.mark.asyncio
async def test_delete_appointment():
    # Register and login user:
    await register_user()
    headers = await login_user("1234567890", "password123")

    # Create an appointment:
    create_response = await create_appointment(headers)
    assert create_response.status_code == 200
    create_data = create_response.json()
    appointment_id = create_data["id"]

    # Delete the appointment:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        delete_response = await ac.delete(
            f"/v1/appointments/{appointment_id}", headers=headers
        )
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["id"] == appointment_id

    # Verify the appointment is deleted:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        get_response = await ac.get("/v1/appointments", headers=headers)
    assert get_response.status_code == 404

    await clean_test_db()  # Clean test database


# Admin Tests -------------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_admin_user_exists():
    # Create admin user
    await register_user("admin", "admin admin", "admin@example.com", "admin", "admin")
    admin_user = await test_users_collection.find_one({"phone": "admin"})
    assert admin_user is not None
    assert admin_user["full_name"] == "admin admin"
    assert admin_user["email"] == "admin@example.com"

    clean_test_db()  # Clean test database


# Test admin login
@pytest.mark.asyncio
async def test_admin_login():
    # Create admin user
    await register_user("admin", "admin admin", "admin@example.com", "admin", "admin")

    # Login as admin
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/v1/token", data={"username": "admin", "password": "admin"}
        )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    clean_test_db()  # Clean test database


# Test admin get all users
@pytest.mark.asyncio
async def test_admin_get_all_users():
    # Create admin user
    await register_user("admin", "admin admin", "admin@example.com", "admin", "admin")

    # Create some users
    await register_user(
        phone="1111111111",
        full_name="Test User",
        email="test@example.com",
        password="password123",
        role="user",
    )
    await register_user(
        phone="2222222222",
        full_name="Test User2",
        email="test2@example.com",
        password="password123",
        role="user",
    )

    # Login as admin
    admin_headers = await login_user("admin", "admin")

    # Get users
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/admin/users", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    await clean_test_db()  # Clean test database


# Test admin delete user
@pytest.mark.asyncio
async def test_admin_delete_user():
    # Create admin user
    await register_user("admin", "admin admin", "admin@example.com", "admin", "admin")

    # Register a new user
    await register_user()

    # Login as admin
    admin_headers = await login_user("admin", "admin")

    # Delete user as admin
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/v1/admin/users/1234567890", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "1234567890"
    assert data["full_name"] == "Test User"

    # Verify user is deleted
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_response = await ac.delete(
            "/v1/admin/users/1234567890", headers=admin_headers
        )
    assert user_response.status_code == 404

    await clean_test_db()  # Clean test database


# Test admin get all appointments
@pytest.mark.asyncio
async def test_admin_get_appointments():
    # Create admin user
    await register_user("admin", "admin admin", "admin@example.com", "admin", "admin")

    # Register and login user to create appointments
    await register_user()
    user_headers = await login_user("1234567890", "password123")

    # Create the first appointment
    await create_appointment(user_headers)

    # Create the second appointment
    await create_appointment(
        user_headers,
        {
            "id": 0,
            "name": "Test User",
            "phone": "1234567890",
            "date": "18-10-2025",
            "time": "11:00",
            "service": "Pedicure",
        },
    )

    # Login as admin
    admin_headers = await login_user("admin", "admin")

    # Get all appointments as admin
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/appointments/all", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    await clean_test_db()  # Clean test database


# Test admin get appointments by phone
@pytest.mark.asyncio
async def test_admin_get_appointments_by_phone():
    # Create admin user
    await register_user("admin", "admin admin", "admin@example.com", "admin", "admin")

    # Register and login user to create appointments
    await register_user()
    user_headers = await login_user("1234567890", "password123")

    # Create the first appointment
    await create_appointment(user_headers)

    # Login as admin
    admin_headers = await login_user("admin", "admin")

    # Get appointments by phone as admin
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/v1/admin/appointments/phone/1234567890", headers=admin_headers
        )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["phone"] == "1234567890"

    await clean_test_db()  # Clean test database


# Test admin get appointments by month and year
@pytest.mark.asyncio
async def test_admin_get_appointments_by_month():
    # Create admin user
    await register_user("admin", "admin admin", "admin@example.com", "admin", "admin")

    # Register and login user to create appointments
    await register_user()
    user_headers = await login_user("1234567890", "password123")

    # Create the first appointment
    await create_appointment(user_headers)

    # Login as admin
    admin_headers = await login_user("admin", "admin")

    # Get appointmen by month and year as admin
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/v1/admin/appointments/month/10/year/2025", headers=admin_headers
        )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["date"].split("-")[1] == "10"

    await clean_test_db()  # Clean test database
