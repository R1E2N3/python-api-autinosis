from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import joblib
import pandas as pd
import sklearn
from flask_cors import CORS

print('hey there! I ran')

app = Flask(__name__)
api = Api(app)
CORS(app)

def processes_data(question, value):
    if question in ['A1', 'A2', 'A3', 'A4', 'A10', 'A5', 'A6', 'A7', 'A8', 'A9', 'A11', 'A12', 'A13']:
        if value in ['1','2', 1, 2]:
            return 1
        else:
            return 0
    return value

class PredictAdult(Resource):
    def post(self):
        # Load the model
        model = joblib.load("adult.joblib")

        # Check if the request contains JSON data
        if request.is_json:
            # Parse JSON data from the request body
            data = request.get_json()

            # Ensure the JSON data contains the expected keys
            if all(key in data for key in ['Ethnicity', 'jundice', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Age']):
                # Perform data preprocessing
                for key in data:
                    data[key] = processes_data(key, data[key])

                # Perform prediction with the loaded model
                input_data = pd.DataFrame([data])
                prediction = model.predict_proba(input_data)[0][1]
                pred = round(prediction * 100)

                return jsonify({"Result": pred})

            else:
                # If the JSON data does not contain the expected keys, return an error message
                return jsonify({"error": "Invalid request format. Please provide all required fields."}), 400
        else:
            # If the request does not contain JSON data, return an error message
            return jsonify({"error": "Request must contain JSON data."}), 400

class PredictChild(Resource):
    def post(self):
        model = joblib.load('child.joblib')

        if resquest.is_json:
            data = request.get_json()

            if all(key in data for key in ['Ethnicity', 'jundice', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Age']):
                # Perform data preprocessing
                for key in data:
                    data[key] = processes_data(key, data[key])

                # Perform prediction with the loaded model
                input_data = pd.DataFrame([data])
                prediction = model.predict_proba(input_data)[0][1]
                pred = round(prediction * 100)

                return jsonify({"Result": pred})

            else:
                # If the JSON data does not contain the expected keys, return an error message
                return jsonify({"error": "Invalid request format. Please provide all required fields."}), 400
        else:
            # If the request does not contain JSON data, return an error message
            return jsonify({"error": "Request must contain JSON data."}), 400

class PredictAdolescent(Resource):
    def post(self):
        model = joblib.load('adolescent.joblib')

        if resquest.is_json:
            data = request.get_json()

            if all(key in data for key in ['Ethnicity', 'jundice', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Age']):
                # Perform data preprocessing
                for key in data:
                    data[key] = processes_data(key, data[key])

                # Perform prediction with the loaded model
                input_data = pd.DataFrame([data])
                prediction = model.predict_proba(input_data)[0][1]
                pred = round(prediction * 100)

                return jsonify({"Result": pred})

            else:
                # If the JSON data does not contain the expected keys, return an error message
                return jsonify({"error": "Invalid request format. Please provide all required fields."}), 400
        else:
            # If the request does not contain JSON data, return an error message
            return jsonify({"error": "Request must contain JSON data."}), 400


api.add_resource(PredictAdult, '/predict_adult')
api.add_resource(PredictAdolescent, '/predict_adolescent')
api.add_resource(PredictChild, '/predict_child')

if __name__ == "__main__":
    app.run(debug=True)
