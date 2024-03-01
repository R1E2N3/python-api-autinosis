import requests

base_url = 'https://python-api-autinosis.onrender.com/predict_adult'

params = {
"Ethnicity": "",
"jundice": 1,
"A1": 1,
"A2": 1,
"A3": 0,
"A4": 0,
"A5": 0,
"A6": 1,
"A7": 0,
"A8": 2,
"A9": 0,
"A10": 0,
"Age": 10
}

response = requests.get(base_url, params)

print(response.json())