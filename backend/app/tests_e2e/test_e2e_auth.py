from api.config import settings

import datetime
import requests


def custom_get_datetime_now():
    """ This function allows to mock the current time at testing """
    return datetime.datetime.now() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def test_token_generation_valid_auth():
    response = requests.post("http://localhost/auth", files={"user_id": (
        None, f"{settings.DEMO_USER_ID}"), "password": (None, f"{settings.DEMO_USER_PASSWORD}")})

    assert response.status_code == 200
    assert response.json()
    assert response.json().get("token")


def test_token_generation_incorrect_user_auth():
    response = requests.post("http://localhost/auth", files={"user_id": (
        None, f"{settings.DEMO_USER_ID}1"), "password": (None, f"{settings.DEMO_USER_PASSWORD}")})

    assert response.status_code == 400
    assert response.json()
    assert response.json().get("token") == None


def test_token_generation_incorrect_password_auth():
    response = requests.post("http://localhost/auth", files={"user_id": (
        None, f"{settings.DEMO_USER_ID}"), "password": (None, f"{settings.DEMO_USER_PASSWORD}1")})

    assert response.status_code == 400
    assert response.json()
    assert response.json().get("token") == None


def test_token_generation_invalid_auth_args_data():
    response = requests.post("http://localhost/auth", data={
                             "user_id": f"{settings.DEMO_USER_ID}1", "password": f"{settings.DEMO_USER_PASSWORD}"})

    assert response.status_code == 400
    assert response.json()
    assert response.json().get("token") == None


def test_token_generation_invalid_auth_args_json():
    response = requests.post("http://localhost/auth", json={
                             "user_id": f"{settings.DEMO_USER_ID}1", "password": f"{settings.DEMO_USER_PASSWORD}"})

    assert response.status_code == 400
    assert response.json()
    assert response.json().get("token") == None


def test_token_not_time_expired():
    response = requests.post("http://localhost/auth", files={"user_id": (
        None, f"{settings.DEMO_USER_ID}"), "password": (None, f"{settings.DEMO_USER_PASSWORD}")})

    assert response.status_code == 200
    assert response.json()
    assert response.json().get("token")

    response = requests.get(
        "http://localhost/me", headers={"Authorization": f"Bearer {response.json().get('token')}"})
    assert response.status_code == 200, response.json()
    assert response.json()


def test_token_not_quota_expired():
    response = requests.post("http://localhost/auth", files={"user_id": (
        None, f"{settings.DEMO_USER_ID}"), "password": (None, f"{settings.DEMO_USER_PASSWORD}")})

    assert response.status_code == 200
    assert response.json()
    assert response.json().get("token")

    for _ in range(settings.ACCESS_TOKEN_EXPIRE_QUOTA):
        temporal_response = requests.get(
            "http://localhost/me", headers={"Authorization": f"Bearer {response.json().get('token')}"})
        assert temporal_response.status_code == 200
        assert temporal_response.json()


def test_token_quota_expired():
    response = requests.post("http://localhost/auth", files={"user_id": (
        None, f"{settings.DEMO_USER_ID}"), "password": (None, f"{settings.DEMO_USER_PASSWORD}")})

    assert response.status_code == 200
    assert response.json()
    assert response.json().get("token")

    for _ in range(settings.ACCESS_TOKEN_EXPIRE_QUOTA):
        temporal_response = requests.get(
            "http://localhost/me", headers={"Authorization": f"Bearer {response.json().get('token')}"})
        assert temporal_response.status_code == 200
        assert temporal_response.json()

    temporal_response = requests.get(
        "http://localhost/me", headers={"Authorization": f"Bearer {response.json().get('token')}"})
    assert temporal_response.status_code == 401
    assert temporal_response.json()
