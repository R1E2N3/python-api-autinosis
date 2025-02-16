from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import joblib
import pandas as pd
from flask_cors import CORS
import os
import resend

# Set the Resend API key (for production, store this in an environment variable)
resend.api_key = os.environ.get("RESEND_API_KEY", "re_9ogVDcHs_JwNABUN8PUi1LuB1KtsW3kzN")

print('hey there! I ran')

app = Flask(__name__)
api = Api(app)
CORS(app)

def processes_data(question, value):
    if question in ['A1', 'A2', 'A3', 'A4', 'A10', 'A5', 'A6', 'A7', 'A8', 'A9', 'A11', 'A12', 'A13']:
        if value in ['1', '2', 1, 2]:
            return 1
        else:
            return 0
    return value

def send_email_resend(to_email, subject, html_body):
    """
    Uses the Resend package to send an email.
    """
    params = {
        "from": "Acme <onboarding@resend.dev>",  # This must be verified in your Resend account
        "to": [to_email],
        "subject": subject,
        "html": html_body
    }
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print("Error sending email:", e)
        return None

class PredictAdult(Resource):
    def post(self):
        # Load the model
        model = joblib.load("adult.joblib")

        if request.is_json:
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

                # If an Email field is provided, send the results via Resend
                if "Email" in data and data["Email"]:
                    subject = "Os resultados do seu teste de autismo. (Adulto)"
                    html_body = f"Olá! Obrigado por usar Autinosis. <br/> <br/> <p>Seu resultado foi: <strong>{pred}%</strong></p>"
                    send_email_resend(data["Email"], subject, html_body)

                return jsonify({"Result": pred})
            else:
                return jsonify({"error": "Invalid request format. Please provide all required fields."}), 400
        else:
            return jsonify({"error": "Request must contain JSON data."}), 400

class PredictChild(Resource):
    def post(self):
        model = joblib.load('child.joblib')
        if request.is_json:
            data = request.get_json()

            # Perform data preprocessing
            for key in data:
                data[key] = processes_data(key, data[key])

            # Perform prediction with the loaded model
            input_data = pd.DataFrame([data])
            prediction = model.predict_proba(input_data)[0][1]
            pred = round(prediction * 100)

            # Send email if provided
            if "Email" in data and data["Email"]:
                subject = "Os resultados do seu teste de autismo (Criança)"
                html_body = f"Olá! Obrigado por usar Autinosis! <br/> <br/> <p>: <strong>{pred}%</strong></p>"
                send_email_resend(data["Email"], subject, html_body)

            return jsonify({"Result": pred})
        else:
            return jsonify({"error": "Request must contain JSON data."}), 400

class PredictAdolescent(Resource):
    def post(self):
        model = joblib.load('adolescent.joblib')
        if request.is_json:
            data = request.get_json()

            if all(key in data for key in ['Ethnicity', 'jundice', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Age']):
                # Perform data preprocessing
                for key in data:
                    data[key] = processes_data(key, data[key])

                # Perform prediction with the loaded model
                input_data = pd.DataFrame([data])
                prediction = model.predict_proba(input_data)[0][1]
                pred = round(prediction * 100)

                # Send email if an Email field is provided
                if "Email" in data and data["Email"]:
                    subject = "Os resultados do seu teste de autismo. (Adolescent)"
                    html_body = f"Olá! Obrigado por usar Autinosis! <br/> <br/> <p>Your test result is: <strong>{pred}%</strong></p>"
                    send_email_resend(data["Email"], subject, html_body)

                return jsonify({"Result": pred})
            else:
                return jsonify({"error": "Invalid request format. Please provide all required fields."}), 400
        else:
            return jsonify({"error": "Request must contain JSON data."}), 400

api.add_resource(PredictAdult, '/predict_adult')
api.add_resource(PredictAdolescent, '/predict_adolescent')
api.add_resource(PredictChild, '/predict_child')

if __name__ == "__main__":
    app.run(debug=True)
