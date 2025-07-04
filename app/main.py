from flask import Flask, render_template
from .routes import routes
from .training import check_and_retrain

app = Flask(__name__)
app.register_blueprint(routes.bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    check_and_retrain()  # Initial training check
    app.run(host='0.0.0.0', port=5000)