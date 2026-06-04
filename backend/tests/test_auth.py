def test_login(client, admin_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_invalid(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "notfound@test.com", "password": "wrong"},
    )
    assert response.status_code == 401

def test_list_users_pagination(client, admin_user):
    # Login to get token
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    token = login_resp.json()["access_token"]
    
    # Request users list
    response = client.get(
        "/api/v1/auth/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "total" in data["data"]
    assert "items" in data["data"]


def test_register_admin_email_rejected(client):
    from app.core.config import settings
    # Try to register the admin email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": settings.ADMIN_EMAIL,
            "password": "somepassword123",
            "full_name": "Fake Admin",
        },
    )
    assert response.status_code == 409


def test_register_regular_user_role(client, db):
    # Register a new user
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "first_user@test.com",
            "password": "password123",
            "full_name": "First User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "viewer"  # Must be viewer, not admin


def test_admin_user_modification_protection(client, db, admin_user):
    from app.core.config import settings
    from app.models.user import User
    from app.core.security import get_password_hash
    
    # Seed the system admin user manually in the test database
    system_admin = User(
        id="sys-admin-id",
        email=settings.ADMIN_EMAIL.lower(),
        full_name="System Admin",
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        role="admin",
        is_active=True,
    )
    db.add(system_admin)
    db.commit()
    
    # Login as admin_user to get access token
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Try to update system admin's role
    resp = client.patch(
        f"/api/v1/auth/users/sys-admin-id",
        json={"role": "viewer"},
        headers=headers,
    )
    assert resp.status_code == 409
    
    # 2. Try to deactivate system admin
    resp = client.patch(
        f"/api/v1/auth/users/sys-admin-id/deactivate",
        headers=headers,
    )
    assert resp.status_code == 409
    
    # 3. Try to delete system admin
    resp = client.delete(
        f"/api/v1/auth/users/sys-admin-id",
        headers=headers,
    )
    assert resp.status_code == 409

