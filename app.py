from flask import Flask, Response, render_template, request, jsonify, render_template_string
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import requests
import os

app = Flask(__name__, template_folder='templates')

# Prometheus metrics
requests_total = Counter('requests_total', 'Total number of requests received')

# Email API configuration
# EMAIL_API_URL = os.getenv('EMAIL_API_URL', 'http://email-api:5000/send_email')

EMAIL_API_URL = os.getenv('EMAIL_API_URL', 'http://email-api:5000/send_email')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app')
def app_route():
    return render_template('app.html')

@app.route('/kavin')
def kavins():
        return render_template_string('''
    <html>
        <head>
            <title>Display Message</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 100px;
                }
                .message {
                    font-size: 20px;
                    color: #333;
                    padding: 10px;
                    border: 1px solid #ccc;
                    display: inline-block;
                    background-color: #f9f9f9;
                }
            </style>
        </head>
        <body>
            <div class="message">
                Hello, this is a small display message!
            </div>
        </body>
    </html>
    ''')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    app.logger.info(f'Received data: {data}')

    # Ensure required fields are present
    if 'to_email' not in data or 'subject' not in data or 'body' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        response = requests.post(EMAIL_API_URL, json=data)
        response.raise_for_status()
        app.logger.info(f'Email sent successfully: {response.json()}')
        return jsonify({"message": "Email sent successfully"}), 200
    except requests.exceptions.HTTPError as e:
        app.logger.error(f'Failed to send email: {response.text}')
        return jsonify({"error": "Failed to send email"}), response.status_code
    except requests.exceptions.RequestException as e:
        app.logger.error(f'Request exception: {e}')
        return jsonify({"error": "Failed to send email"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

