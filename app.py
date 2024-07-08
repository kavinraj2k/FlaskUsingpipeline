from flask import Flask, Response,render_template
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import random
import time

app = Flask(__name__, template_folder='templates')

    
requests_total = Counter('requests_total', 'Total number of requests received')

EMAIL_API_URL = os.getenv('EMAIL_API_URL', 'http://localhost:5000/send_email')


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/app")
def app_route():
    return render_template('app.html')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    try:
        response = requests.post(EMAIL_API_URL, json=data)
        response.raise_for_status()
        return jsonify({"message": "Email sent successfully"}), 200
    except requests.exceptions.RequestException as e:
        app.logger.error(f'Failed to send email: {e}')
        return jsonify({"error": "Failed to send email"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
