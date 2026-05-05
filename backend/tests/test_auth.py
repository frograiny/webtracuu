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
