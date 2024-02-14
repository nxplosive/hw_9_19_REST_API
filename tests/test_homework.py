import json
from jsonschema import validate
import requests

from utils.utils import load_schema

base_url = "https://reqres.in/api/"


def test_get_user():
    response = requests.get(f"{base_url}users/2")
    assert response.json()["data"]["first_name"] == "Janet"


def test_not_found_404():
    response = requests.get(f"{base_url}unknown/23")
    assert response.status_code == 404


def test_create_user():
    name = "Anton"
    job = "QA"
    response = requests.post(f"{base_url}users", json={
        "name": name,
        "job": job
    })
    assert response.status_code == 201
    assert response.json()["name"] == name
    assert response.json()["job"] == job


def test_update_user():
    name = "Sergey"
    job = "Teacher"
    response = requests.put(f"{base_url}users/2", json={
        "name": name,
        "job": job
    })
    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["job"] == job


def test_delete_user():
    response = requests.delete(f"{base_url}users/2")
    assert response.status_code == 204


def test_get_list_users():
    response = requests.get(f"{base_url}users", params={
        "page": 2
    })
    body = response.json()
    schema_path = load_schema("users_list.json")
    with open(schema_path) as file:
        schema = json.load(file)
    validate(body, schema=schema)


def test_get_list_resource():
    response = requests.get(f"{base_url}unknown")
    body = response.json()
    schema_path = load_schema("list_resource.json")
    with open(schema_path) as file:
        schema = json.load(file)
    validate(body, schema=schema)


def test_successful_register():
    response = requests.post(f"{base_url}register", json={
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    })
    body = response.json()
    schema_path = load_schema("response_successful_register.json")
    with open(schema_path) as file:
        schema = json.load(file)
    validate(body, schema=schema)


def test_get_single_user():
    response = requests.get(f"{base_url}users/2")
    body = response.json()
    schema_path = load_schema("only_user.json")
    with open(schema_path) as file:
        schema = json.load(file)
    validate(body, schema=schema)


def test_unsuccessful_register():
    response = requests.post(f"{base_url}register", json={
        "email": "sydney@fife"
    })
    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_unsuccessful_login():
    response = requests.post(f"{base_url}login", json={
        "email": "peter@klaven"
    })
    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"