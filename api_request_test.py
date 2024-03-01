import requests

base_url = 'https://python-api-autinosis.onrender.com/uppercase?text=hello world'

# params = {'text': 'hello world'}

response = requests.get(base_url)

print(response.json())