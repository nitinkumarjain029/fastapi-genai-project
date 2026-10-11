from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.db.models import User
from app.db.database import SessionLocal

# client = TestClient(app)   # client jo fastapi app ko test karega

def test_get_users(client):

    response = client.get("/users") # automatically users api call krta hai

def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "age": 25,
            "phone": "9999999999",
            "password": "Test@123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert data["age"] == 25


def test_create_user_invalid_age(client):
    response = client.post(
        "/users",
        json={
            "name": "Invalid User",
            "email": "invalid@example.com",
            "age": "abc",
            "phone": "9999999999",
            "password": "Test@123"
        }
    )

    assert response.status_code == 422    



def test_get_user(client):
    # Step 1: Create a user
    create_response = client.post(
        "/users",
        json={
            "name": "Get User Test",
            "email": "getuser@example.com",
            "age": 28,
            "phone": "8888888888",
            "password": "Test@123"
        }
    )

    assert create_response.status_code == 201

    # Step 2: Get the ID from create response
    created_user = create_response.json()
    user_id = created_user["id"]

    # Step 3: Fetch the same user
    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "Get User Test"
    assert data["email"] == "getuser@example.com"   

def get_fake_users(client):
    response = client.get("/users"/9999)

    assert response.status_code == 400    

    
def test_get_missing_user(client):
    response = client.get("/users/9999")

    assert response.status_code == 404

def test_get_users_pagination(client):
    response = client.get("/users?page=1&limit=3")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert data["page"] == 1
    assert data["limit"] == 3
    assert len(data["items"]) <= 3


def test_get_users_invalid_page(client):
    response = client.get("/users?page=0&limit=10")

    assert response.status_code == 422


def test_get_users_invalid_limit(client):
    response = client.get("/users?page=1&limit=0")

    assert response.status_code == 422


def test_get_users_limit_above_maximum(client):
    response = client.get("/users?page=1&limit=101")

    assert response.status_code == 422


def test_put_update_user(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Before Update",
            "email": "puttest@example.com",
            "age": 25,
            "phone": "9999999999",
            "password": "Test@123"
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={
            "name": "After Update",
            "email": "puttest@example.com",
            "age": 30,
            "phone": "8888888888"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "After Update"
    assert data["age"] == 30




def test_patch_update_user(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Patch User",
            "email": "patchtest@example.com",
            "age": 25,
            "phone": "9999999999",
            "password": "Test@123"
        }
    )

    assert create_response.status_code == 201
    created_user = create_response.json()
    user_id = created_user["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={"age": 31}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["age"] == 31
    assert data["name"] == "Patch User"
    assert data["email"] == "patchtest@example.com"    


    
def test_delete_user_without_token(client):
    response = client.delete("/users/1")
    assert response.status_code == 401


def test_delete_user_as_normal_user(client, db_session):
    user = User(
        name="Normal User",
        email="normal-delete@example.com",
        age=25,
        phone="9999999999",
        password="hashed-password",
        role="user",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    user_id = user.id
    token = create_access_token({"sub": str(user_id)})

    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_delete_user_as_admin(client, db_session):
    admin = User(
        name="Test Admin",
        email="admin-delete@example.com",
        age=30,
        phone="8888888888",
        password="hashed-password",
        role="admin",
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)

    admin_id = admin.id
    token = create_access_token({"sub": str(admin_id)})

    response = client.delete(
        f"/users/{admin_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204    



def test_login_success(client):
    # Arrange: pehle user create karo
    create_response = client.post(
        "/users",
        json={
            "name": "Login Test",
            "email": "login-test@example.com",
            "age": 25,
            "phone": "9999999999",
            "password": "Test@123"
        }
    )
    assert create_response.status_code == 201

    # Act: correct credentials se login
    response = client.post(
        "/users/login",
        json={
            "email": "login-test@example.com",
            "password": "Test@123"
        }
    )

    # Assert: successful login aur tokens
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["refresh_token"]


def test_login_wrong_password(client):
    client.post(
        "/users",
        json={
            "name": "Login Test",
            "email": "wrong-password@example.com",
            "age": 25,
            "phone": "9999999999",
            "password": "Correct@123"
        }
    )

    response = client.post(
        "/users/login",
        json={
            "email": "wrong-password@example.com",
            "password": "Wrong@123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid email and password"


def test_login_nonexistent_email(client):
    response = client.post(
        "/users/login",
        json={
            "email": "missing@example.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid email and password"





    
def test_refresh_token_success(client):
    # User create karo
    create_response = client.post(
        "/users",
        json={
            "name": "Refresh Test",
            "email": "refresh-test@example.com",
            "age": 25,
            "phone": "9999999999",
            "password": "Test@123"
        }
    )
    assert create_response.status_code == 201

    # Login se actual refresh token lo
    login_response = client.post(
        "/users/login",
        json={
            "email": "refresh-test@example.com",
            "password": "Test@123"
        }
    )
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]

    # Refresh endpoint call karo
    response = client.post(
        "/users/refresh",
        json={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_refresh_token_invalid(client):
    response = client.post(
        "/users/refresh",
        json={"refresh_token": "invalid.token.value"}
    )

    assert response.status_code == 401


def test_refresh_token_revoked(client):
    # User create karo
    create_response = client.post(
        "/users",
        json={
            "name": "Revoked Test",
            "email": "revoked-test@example.com",
            "age": 25,
            "phone": "9999999999",
            "password": "Test@123"
        }
    )
    assert create_response.status_code == 201

    # Login karke refresh token lo
    login_response = client.post(
        "/users/login",
        json={
            "email": "revoked-test@example.com",
            "password": "Test@123"
        }
    )
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]

    # Logout se token revoke karo
    logout_response = client.post(
        "/users/logout",
        json={"refresh_token": refresh_token}
    )
    assert logout_response.status_code == 200

    # Revoked token dobara use nahi hona chahiye
    response = client.post(
        "/users/refresh",
        json={"refresh_token": refresh_token}
    )

    assert response.status_code == 401   


def test_get_me_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid.token.value"}
    )

    assert response.status_code == 401




def test_get_me_user_not_found(client):
    token = create_access_token({"sub": "999999"})

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401        


def test_normal_user_cannot_delete_user(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Regular User",
            "email": "regular-auth@example.com",
            "age": 25,
            "phone": "9999999999",
            "password": "Test@123"
        }
    )
    assert create_response.status_code == 201

    user_id = create_response.json()["id"]
    token = create_access_token({"sub": str(user_id)})

    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403



def test_get_me_invalid_user_id_in_token(client):
    token = create_access_token({"sub": "abc"})

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401


  