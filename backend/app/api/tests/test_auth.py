from fastapi.testclient import TestClient
import datetime

from api.main import app
from api.auth import deps
from api.config import settings

client = TestClient(app)

def custom_get_datetime_now():
    """ This function allows to mock the current time at testing """
    return datetime.datetime.now() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def test_token_generation_valid_auth():
    response = client.post("/auth", files={"user_id": (None, f"{settings.DEMO_USER_ID}"), "password":(None, f"{settings.DEMO_USER_PASSWORD}")})
    
    assert response.status_code == 200
    assert response.json()
    assert response.json().get("token")

def test_token_generation_incorrect_user_auth():
    response = client.post("/auth", files={"user_id": (None, f"{settings.DEMO_USER_ID}1"), "password":(None, f"{settings.DEMO_USER_PASSWORD}")})
    
    assert response.status_code == 400
    assert response.json()
    assert response.json().get("token") == None

def test_token_generation_incorrect_password_auth():
    response = client.post("/auth", files={"user_id": (None, f"{settings.DEMO_USER_ID}"), "password":(None, f"{settings.DEMO_USER_PASSWORD}1")})
    
    assert response.status_code == 400
    assert response.json()
    assert response.json().get("token") == None

def test_token_generation_invalid_auth_args_data():
    response = client.post("/auth", data={"user_id": f"{settings.DEMO_USER_ID}1", "password":f"{settings.DEMO_USER_PASSWORD}"})
    
    assert response.status_code == 400
    assert response.json()
    assert response.json().get("token") == None

def test_token_generation_invalid_auth_args_json():
    response = client.post("/auth", json={"user_id": f"{settings.DEMO_USER_ID}1", "password":f"{settings.DEMO_USER_PASSWORD}"})
    
    assert response.status_code == 400
    assert response.json()
    assert response.json().get("token") == None

def test_token_not_time_expired():
    response = client.post("/auth", files={"user_id": (None, f"{settings.DEMO_USER_ID}"), "password":(None, f"{settings.DEMO_USER_PASSWORD}")})
    
    assert response.status_code == 200
    assert response.json()
    assert response.json().get("token")

    response = client.get("/me", headers={"Authorization": f"Bearer {response.json().get('token')}"})
    assert response.status_code == 200, response.json()
    assert response.json()

def test_token_time_expired():
    # Override the time method to add an extra N minutes and don't wait for the test
    app.dependency_overrides[deps.get_datetime_now] = custom_get_datetime_now
    response = client.post("/auth", files={"user_id": (None, f"{settings.DEMO_USER_ID}"), "password":(None, f"{settings.DEMO_USER_PASSWORD}")})
    
    assert response.status_code == 200
    assert response.json()
    assert response.json().get("token")

    response = client.get("/me", headers={"Authorization": f"Bearer {response.json().get('token')}"})
    assert response.status_code == 401
    assert response.json()
    app.dependency_overrides = {}

def test_token_not_quota_expired():
    response = client.post("/auth", files={"user_id": (None, f"{settings.DEMO_USER_ID}"), "password":(None, f"{settings.DEMO_USER_PASSWORD}")})
    
    assert response.status_code == 200
    assert response.json()
    assert response.json().get("token")

    for _ in range(settings.ACCESS_TOKEN_EXPIRE_QUOTA):
        temporal_response = client.get("/me", headers={"Authorization": f"Bearer {response.json().get('token')}"})
        assert temporal_response.status_code == 200
        assert temporal_response.json()

def test_token_quota_expired():
    response = client.post("/auth", files={"user_id": (None, f"{settings.DEMO_USER_ID}"), "password":(None, f"{settings.DEMO_USER_PASSWORD}")})
    
    assert response.status_code == 200
    assert response.json()
    assert response.json().get("token")

    for _ in range(settings.ACCESS_TOKEN_EXPIRE_QUOTA):
        temporal_response = client.get("/me", headers={"Authorization": f"Bearer {response.json().get('token')}"})
        assert temporal_response.status_code == 200
        assert temporal_response.json()
    
    temporal_response = client.get("/me", headers={"Authorization": f"Bearer {response.json().get('token')}"})
    assert temporal_response.status_code == 401
    assert temporal_response.json()
