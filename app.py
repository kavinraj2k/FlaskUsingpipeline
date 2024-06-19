from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/app")
def app_route():
    return render_template('app.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
