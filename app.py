from flask import Flask
from flask_cors import CORS
from config import Config
from routes import councillors_bp, councillor_votes_bp, votes_bp, meetings_bp
from routes.base import base_bp
from models.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # More permissive CORS configuration
    CORS(app, 
         resources={r"/*": {
             "origins": "*",
             "send_wildcard": True,
             "expose_headers": ["Content-Type", "Authorization"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "max_age": 600
         }})
    
    @app.after_request
    def add_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)  # Initialize the app with SQLAlchemy

    # Register blueprints with URL prefixes
    app.register_blueprint(councillors_bp, url_prefix='/councillors')
    app.register_blueprint(councillor_votes_bp, url_prefix='/councillor_votes')
    app.register_blueprint(votes_bp, url_prefix='/votes')
    app.register_blueprint(meetings_bp, url_prefix='/meetings')
    app.register_blueprint(base_bp)

    with app.app_context():
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5099)
