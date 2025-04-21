from flask import Flask
from models import db
from routes import app_routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key'

    db.init_app(app)
    app.register_blueprint(app_routes)

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0', port=5004, debug=True)
