import requests

base_url = 'https://python-api-autinosis.onrender.com/uppercase'

params = {'text': 'hey there I\'m here'}

response = requests.get(base_url, params)

print(response.json())