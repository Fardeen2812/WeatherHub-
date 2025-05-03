from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# Removed unnecessary import for sendgrid.exceptions
import os
import requests

app = Flask(__name__)

# Load environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
if not SENDGRID_API_KEY:
    raise ValueError("SENDGRID_API_KEY environment variable is not set!")

FROM_EMAIL = os.getenv('FROM_EMAIL', 'default-email@example.com')

@app.route('/alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400

    email = data['email']
    if not isinstance(email, str) or '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email,
        subject='Weather Alert',
        plain_text_content='Severe weather alert! Stay safe.'
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return jsonify({'message': 'Alert sent', 'status_code': response.status_code})
    except Exception as e:
        return jsonify({'error': 'Failed to send email', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Alert Notification Service is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

url = "http://localhost:5004/alert"
payload = {"email": "test@example.com"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
