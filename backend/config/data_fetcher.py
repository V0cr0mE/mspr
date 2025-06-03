import requests

def get_countries():
    response = requests.get("http://127.0.0.1:5000/country")
    return response.json() if response.status_code == 200 else []

def get_continents():
    response = requests.get("http://127.0.0.1:5000/continent")
    return response.json() if response.status_code == 200 else []

def get_pandemics():
    response = requests.get("http://127.0.0.1:5000/pandemic")
    return response.json() if response.status_code == 200 else []