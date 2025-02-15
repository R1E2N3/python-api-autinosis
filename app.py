from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import joblib
import pandas as pd
from flask_cors import CORS
import resend

print('hey there! I ran')

###############################################################################
#                               Flask + CORS Setup
###############################################################################
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/send-email": {"origins": ["http://localhost:3000", "https://nextjs-flask-lime.vercel.app"]}})


###############################################################################
#                          Resend Configuration
###############################################################################
# Set your Resend API key (ideally from environment variables in production):
resend.api_key = "re_9ogVDcHs_JwNABUN8PUi1LuB1KtsW3kzN"

# If you need to create an API Key (only once, usually in a setup script):
# params: resend.ApiKeys.CreateParams = { "name": "Production" }
# resend.ApiKeys.create(params)

###############################################################################
#                              Helper Functions
###############################################################################
def processes_data(question, value):
    """
    Convert certain answers (1 or 2) to 1, otherwise 0.
    You can adjust this logic as needed.
    """
    if question in ['A1', 'A2', 'A3', 'A4', 'A10', 'A5', 'A6', 'A7', 'A8', 'A9', 'A11', 'A12', 'A13']:
        if value in ['1','2', 1, 2]:
            return 1
        else:
            return 0
    return value

###############################################################################
#                         Resource: PredictAdult
###############################################################################
class PredictAdult(Resource):
    def post(self):
        model = joblib.load("adult.joblib")

        if request.is_json:
            data = request.get_json()
            required_fields = ['Ethnicity', 'jundice', 'A1', 'A2', 'A3', 'A4',
                               'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Age']

            if all(key in data for key in required_fields):
                # Preprocess
                for key in data:
                    data[key] = processes_data(key, data[key])

                # Predict
                input_data = pd.DataFrame([data])
                prediction = model.predict_proba(input_data)[0][1]
                pred = round(prediction * 100)
                return jsonify({"Result": pred})
            else:
                return jsonify({"error": "Invalid request format. Please provide all required fields."}), 400
        else:
            return jsonify({"error": "Request must contain JSON data."}), 400

###############################################################################
#                        Resource: PredictChild
###############################################################################
class PredictChild(Resource):
    def post(self):
        model = joblib.load('child.joblib')

        if request.is_json:
            data = request.get_json()
            # Preprocess
            for key in data:
                data[key] = processes_data(key, data[key])

            # Predict
            input_data = pd.DataFrame([data])
            prediction = model.predict_proba(input_data)[0][1]
            pred = round(prediction * 100)

            return jsonify({"Result": pred})
        else:
            return jsonify({"error": "Request must contain JSON data."}), 400

###############################################################################
#                      Resource: PredictAdolescent
###############################################################################
class PredictAdolescent(Resource):
    def post(self):
        model = joblib.load('adolescent.joblib')

        if request.is_json:
            data = request.get_json()
            required_fields = ['Ethnicity', 'jundice', 'A1', 'A2', 'A3', 'A4',
                               'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Age']

            if all(key in data for key in required_fields):
                # Preprocess
                for key in data:
                    data[key] = processes_data(key, data[key])

                # Predict
                input_data = pd.DataFrame([data])
                prediction = model.predict_proba(input_data)[0][1]
                pred = round(prediction * 100)

                return jsonify({"Result": pred})
            else:
                return jsonify({"error": "Invalid request format. Please provide all required fields."}), 400
        else:
            return jsonify({"error": "Request must contain JSON data."}), 400

###############################################################################
#                           Resource: SendEmail
###############################################################################
class SendEmail(Resource):
    """
    Expects JSON like:
    {
      "email": "someuser@example.com",
      "result": 85
    }
    Will send an email via Resend with that information.
    """
    def post(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        email = data.get("email")
        result = data.get("result")

        if not email or result is None:
            return jsonify({"error": "Missing 'email' or 'result' in JSON body"}), 400

        # Prepare the email
        params = {
            "from": "Autism Test <onboarding@resend.dev>",  # Must be verified in your Resend dashboard
            "to": [email],  # Pass as an array if your Resend version requires it
            "subject": "Your Autism Test Results",
            "html": f"""
              <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #333; text-align: center;">Your Autism Test Results</h1>

                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                  <p style="font-size: 18px; text-align: center;">Your result score is:</p>
                  <h2 style="color: #FF5722; text-align: center; font-size: 36px;">{result}%</h2>
                </div>

                <div style="margin-top: 20px; padding: 20px; border-top: 1px solid #eee;">
                  <p style="color: #666;">Important Note:</p>
                  <p style="color: #666; font-size: 14px;">
                    This test result is for screening only and should not be considered a diagnosis.
                    Please consult a qualified healthcare professional if you have concerns.
                  </p>
                </div>

                <footer style="margin-top: 30px; text-align: center; color: #888; font-size: 12px;">
                  <p>This email was sent based on your request after completing the autism screening test.</p>
                </footer>
              </div>
            """,
        }

        try:
            response = resend.Emails.send(params)
            return jsonify({"message": "Email sent successfully", "data": response}), 200
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({"error": str(e)}), 500

###############################################################################
#                         Register All Resources
###############################################################################
api.add_resource(PredictAdult, '/predict_adult')
api.add_resource(PredictAdolescent, '/predict_adolescent')
api.add_resource(PredictChild, '/predict_child')
api.add_resource(SendEmail, '/send-email')

###############################################################################
#                                   Main
###############################################################################
if __name__ == "__main__":
    # In production on Render, you'd typically not run with debug=True.
    # But for local tests:
    app.run(debug=True)
