import requests
from requests.auth import HTTPBasicAuth
import json

ENDPOINT_PATH = 'http://localhost:8000/api/v1/'


def fetch_register(username, password):
    endpoint = ENDPOINT_PATH + 'user/add/'
    headers = {
        'username': username,
        'password': password,
        'password2': password,
    }
    response = requests.post(endpoint, json=headers)
    details = json.loads(response.content)
    if response.status_code == 201:
        print(f'User {username} created. Details {details}')
        return username, password, response.status_code

    print(f"User {username} not created. Details {details}")
    return None, None, response.status_code


def fetch_set_email(username, password, email, verbose=False):
    endpoint = ENDPOINT_PATH + f'user/{username.lower()}/edit/'
    content = {
        'username': username,
        'email': email
    }
    response = requests.put(endpoint, auth=HTTPBasicAuth(username, password), json=content)
    # data = ''
    data = str(response.content)
    # if response.content:
    #     data = json.loads(response.content)
    if verbose:
        return f"{'Login OK' if response.status_code == 200 else 'Login failed'}, details: {data}"
    return response, response.content


def fetch_status(verbose=False):
    endpoint = ENDPOINT_PATH + ''
    response = requests.get(endpoint)
    urls = ''
    if response.content:
        data = json.loads(response.content)
        urls = '\n'.join((f"{key}: {val}" for key, val in data.items()))
    if verbose:
        return f"{'Server is OK,' if response.status_code == 200 else 'Server encountered problem.'} Status code: {response.status_code}.\n" + urls
    return response.status_code, urls
