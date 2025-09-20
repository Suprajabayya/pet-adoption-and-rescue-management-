import requests

API_BASE = "http://127.0.0.1:8000/api/users"
token = "30e19ff0b8f984887bfe284f5264e724b1924c15"

headers = {
    "Authorization": f"Token {token}"
}

resp = requests.get(f"{API_BASE}/pets/", headers=headers)

print(resp.status_code)  # should print 200 if successful
print(resp.json())       # should print your pets data
