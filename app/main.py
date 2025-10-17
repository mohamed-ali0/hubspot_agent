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
        from app.models import import_models
        User, ChatSession, ChatMessage, Log = import_models()
        print("[OK] Models imported successfully")
    except Exception as e:
        print(f"[WARNING] Model import error: {e}")
        # Continue without models for now

    # Register blueprints - handle SQLAlchemy conflicts gracefully
    blueprint_registry = {
        'health': {'module': 'app.api.v1.health', 'url_prefix': '/api/health'},
        'help': {'module': 'app.api.v1.help', 'url_prefix': '/api/help'},
        'auth': {'module': 'app.api.v1.auth', 'url_prefix': '/api/auth'},
        'users': {'module': 'app.api.v1.users', 'url_prefix': '/api/users'},
        'sessions': {'module': 'app.api.v1.sessions', 'url_prefix': '/api/sessions'},
        'messages': {'module': 'app.api.v1.messages', 'url_prefix': '/api/messages'},
        'logs': {'module': 'app.api.v1.logs', 'url_prefix': '/api/logs'},
        'stats': {'module': 'app.api.v1.stats', 'url_prefix': '/api/stats'},
        'whatsapp': {'module': 'app.api.v1.whatsapp', 'url_prefix': '/api/whatsapp'},
    }
    
    registered_blueprints = []
    
    for blueprint_name, config in blueprint_registry.items():
        try:
            # Import the module dynamically
            module = __import__(config['module'], fromlist=['bp'])
            app.register_blueprint(module.bp, url_prefix=config['url_prefix'])
            registered_blueprints.append(blueprint_name)
            print(f"[OK] {blueprint_name.title()} blueprint registered")
        except Exception as e:
            print(f"[WARNING] Could not register {blueprint_name} blueprint: {e}")
    
    print(f"[OK] Successfully registered {len(registered_blueprints)} blueprints: {', '.join(registered_blueprints)}")
    
    # HubSpot blueprints (conditional registration)
    hubspot_blueprints = {
        'hubspot_legacy': {'module': 'app.api.v1.hubspot_legacy', 'url_prefix': '/api/hubspot'},
        'contacts': {'module': 'app.api.v1.hubspot.contacts', 'url_prefix': '/api/hubspot/contacts'},
        'companies': {'module': 'app.api.v1.hubspot.companies', 'url_prefix': '/api/hubspot/companies'},
        'deals': {'module': 'app.api.v1.hubspot.deals', 'url_prefix': '/api/hubspot/deals'},
        'notes': {'module': 'app.api.v1.hubspot.notes', 'url_prefix': '/api/hubspot/notes'},
        'tasks': {'module': 'app.api.v1.hubspot.tasks', 'url_prefix': '/api/hubspot/tasks'},
        'activities': {'module': 'app.api.v1.hubspot.activities', 'url_prefix': '/api/hubspot/activities'},
        'associations': {'module': 'app.api.v1.hubspot.associations', 'url_prefix': '/api/hubspot/associations'},
        'leads': {'module': 'app.api.v1.hubspot.leads', 'url_prefix': '/api/hubspot/leads'},
    }
    
    hubspot_registered = []
    
    for blueprint_name, config in hubspot_blueprints.items():
        try:
            # Import the module dynamically
            module = __import__(config['module'], fromlist=['bp'])
            app.register_blueprint(module.bp, url_prefix=config['url_prefix'])
            hubspot_registered.append(blueprint_name)
            print(f"[OK] {blueprint_name.title()} HubSpot blueprint registered")
        except Exception as e:
            print(f"[WARNING] Could not register {blueprint_name} HubSpot blueprint: {e}")
    
    print(f"[OK] Successfully registered {len(hubspot_registered)} HubSpot blueprints: {', '.join(hubspot_registered)}")

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
        print("[INFO] Server will be available at: http://127.0.0.1:5012")
        print("[INFO] Health check: http://127.0.0.1:5012/api/health")
    
    # Use Gunicorn in production/Docker, Flask dev server otherwise
    if app.config.get('FLASK_ENV') == 'production' or app.config.get('IGNORE_DATABASE_PERSISTENCE', False):
        print("[INFO] Starting with Gunicorn for production...")
        # This will be handled by the Dockerfile CMD
        app.run(host='0.0.0.0', port=5012, debug=False)
    else:
        app.run(debug=True, host='0.0.0.0', port=5012)