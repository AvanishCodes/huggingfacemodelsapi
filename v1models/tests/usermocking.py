import requests

USERNAME = "testuser"
PASSWORD = "TestUser@123"

def create_user():
    url = "http://localhost:8000/authentication/register/"
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "password2": PASSWORD,
        "email": "testuser@gmail.com",
        "first_name": "Test",
        "last_name": "User",
    }
    response = requests.post(url, data=data)
    return {
        "username": USERNAME, # "testuser",
        "password": PASSWORD,
    }

def get_token(username=USERNAME, password=PASSWORD):
    url = "http://localhost:8000/authentication/token/"
    data = {
        "username": username,
        "password": password,
    }
    response = requests.post(url, data=data)
    return response.json()