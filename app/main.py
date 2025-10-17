"""
Main Flask application for HubSpot Logging AI Agent
"""

import os
import sys
from pathlib import Path

# Add parent directory to Python path so we can import app modules
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database instance from the centralized location
from app.db.database import db

# Initialize extensions
jwt = JWTManager()
migrate = Migrate()
cors = CORS()

def create_app(config_class=None):
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    if config_class is None:
        # Check if running in Docker
        if os.getenv('DOCKER_ENV') == 'true' or os.path.exists('/.dockerenv'):
            from app.config import DockerConfig
            app.config.from_object(DockerConfig)
        else:
            app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
            
            # Handle database path correctly regardless of working directory
            db_url = os.getenv('DATABASE_URL', 'sqlite:///data/database.db')
            if db_url.startswith('sqlite:///') and not db_url.startswith('sqlite:////'):
                # Make path absolute relative to project root
                project_root = Path(__file__).parent.parent
                db_path = db_url.replace('sqlite:///', '')
                absolute_db_path = project_root / db_path
                app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{absolute_db_path}'
            else:
                app.config['SQLALCHEMY_DATABASE_URI'] = db_url
                
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
            app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
            
            # HubSpot Configuration
            app.config['HUBSPOT_API_URL'] = os.getenv('HUBSPOT_API_URL', 'https://api.hubapi.com')
            app.config['HUBSPOT_ACCESS_TOKEN'] = os.getenv('HUBSPOT_ACCESS_TOKEN')
    else:
        app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize migrate before importing models
    migrate.init_app(app, db)

    # Import models after database and migrate are initialized
    # This ensures models are only registered once
    try:
        from app.models import User, ChatSession, ChatMessage, Log
    except Exception as e:
        print(f"[WARNING] Model import error: {e}")
        # Continue without models for now

    # Register blueprints - import after models are loaded
    try:
        from app.api.v1 import auth, users, sessions, messages, logs, stats, health, help, whatsapp
        from app.api.v1.hubspot import contacts_bp, companies_bp, deals_bp, notes_bp, tasks_bp, activities_bp, associations_bp, leads_bp
    except Exception as e:
        print(f"[WARNING] Blueprint import error: {e}")
        # Continue without some blueprints if needed
    
    # Core API blueprints
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(users.bp, url_prefix='/api/users')
    app.register_blueprint(sessions.bp, url_prefix='/api/sessions')
    app.register_blueprint(messages.bp, url_prefix='/api/messages')
    app.register_blueprint(logs.bp, url_prefix='/api/logs')
    app.register_blueprint(stats.bp, url_prefix='/api/stats')
    app.register_blueprint(health.bp, url_prefix='/api/health')
    app.register_blueprint(help.bp, url_prefix='/api/help')
    app.register_blueprint(whatsapp.bp, url_prefix='/api/whatsapp')
    
    # Legacy HubSpot blueprint (for backward compatibility)
    try:
        from app.api.v1 import hubspot_legacy
        app.register_blueprint(hubspot_legacy.bp, url_prefix='/api/hubspot')
    except ImportError:
        pass  # Legacy hubspot module not available
    
    # New organized HubSpot blueprints
    app.register_blueprint(contacts_bp, url_prefix='/api/hubspot/contacts')
    app.register_blueprint(companies_bp, url_prefix='/api/hubspot/companies')
    app.register_blueprint(deals_bp, url_prefix='/api/hubspot/deals')
    app.register_blueprint(notes_bp, url_prefix='/api/hubspot/notes')
    app.register_blueprint(tasks_bp, url_prefix='/api/hubspot/tasks')
    app.register_blueprint(activities_bp, url_prefix='/api/hubspot/activities')
    app.register_blueprint(associations_bp, url_prefix='/api/hubspot/associations')
    app.register_blueprint(leads_bp, url_prefix='/api/hubspot/leads')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

# Create app instance for direct running
app = create_app()

# Initialize database tables when running directly
if __name__ == '__main__':
    with app.app_context():
        try:
            # Check if we should ignore database persistence (Docker mode)
            if app.config.get('IGNORE_DATABASE_PERSISTENCE', False):
                print("[INFO] Docker mode: Using in-memory database (no persistence)")
                # Create tables in memory
                db.create_all()
                print("[OK] In-memory database tables created successfully!")
            else:
                db.create_all()
                print("[OK] Database tables created successfully!")
        except Exception as e:
            print(f"[ERROR] Database initialization error: {e}")
    
    print("[START] Starting Flask application...")
    print("[INFO] Server will be available at: http://127.0.0.1:5000")
    print("[INFO] Health check: http://127.0.0.1:5000/api/health")
    
    # Use Gunicorn in production/Docker, Flask dev server otherwise
    if app.config.get('FLASK_ENV') == 'production' or app.config.get('IGNORE_DATABASE_PERSISTENCE', False):
        print("[INFO] Starting with Gunicorn for production...")
        # This will be handled by the Dockerfile CMD
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)