from flask import Flask
from flask_cors import CORS
from views.routes import initialize_routes
from config.settings import FLASK_CONFIG

app = Flask(__name__)
CORS(app)

# Initialize the routes
initialize_routes(app)

if __name__ == '__main__':
    app.run(**FLASK_CONFIG)
