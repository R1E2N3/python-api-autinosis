import requests

base_url = 'http://127.0.0.1:5000/uppercase?text=hello world'

# params = {'text': 'hello world'}

response = requests.get(base_url)

print(response.status_code)