from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template
from user import user_blueprint
from trip import trip_blueprint

app = Flask(__name__)

app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(trip_blueprint, url_prefix='/trip')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
