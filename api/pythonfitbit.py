import requests
import json

refresh_token = "sitenitsen"
url = 'https://api.fitbit.com/oauth2/token'
data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic MjJCNVhYOmVjYzdiOWNmODk0ZjJhOTZiYzg4OWJkZjQxOTQwYTQ4"}

req = requests.post(url, data=data, headers=headers)
out=json.loads(req.text)
print (req.text)
print(out["success"])
