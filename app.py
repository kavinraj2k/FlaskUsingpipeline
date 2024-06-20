from flask import Flask, Response,render_template
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import random
import time

app = Flask(__name__, template_folder='templates')

    
requests_total = Counter('requests_total', 'Total number of requests received')


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/app")
def app_route():
    return render_template('app.html')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
