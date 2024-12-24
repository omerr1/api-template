from flask import Flask
from db import db
from db_models import Property, Unit, Lease, Tenant
from setup_db import initialize_database
from routes import register_routes

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # Example with SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Register the routes
register_routes(app)

# Initialize and populate the database
with app.app_context():
    initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
