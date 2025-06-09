from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .models.user import db
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Store config name for use throughout the function
    app.config_name = config_name
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Set configuration based on environment
    if config_name == 'production':
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['DEBUG'] = False
    else:
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['DEBUG'] = True
    
    app.config['PROPAGATE_EXCEPTIONS'] = True
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)  # Initialize SQLAlchemy first
    
    # Configure CORS
    CORS(app, 
         resources={r"/*": {
             "origins": ["https://ecommerce-frontend-1qfw.onrender.com"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
             "supports_credentials": True,
             "expose_headers": ["Content-Range", "X-Content-Range"]
         }},
         supports_credentials=True)
    
    # Add after_request handler to ensure CORS headers are always present
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin == 'https://ecommerce-frontend-1qfw.onrender.com':
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
            response.headers['Access-Control-Max-Age'] = '3600'
        return response
    
    # Add OPTIONS handler for preflight requests
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({'status': 'ok'})
            origin = request.headers.get('Origin')
            if origin == 'https://ecommerce-frontend-1qfw.onrender.com':
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Max-Age'] = '3600'
                return response
            return response
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Handle JWT errors without redirects
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is required'}), 401
    
    Migrate(app, db)
    
    # Register blueprints
    from .api.auth import auth_bp
    from .api.products import products_bp
    from .api.orders import order_bp
    from .api.cart import cart_bp
    from .api.chat import chat_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    # Add health check route
    @app.route('/')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'E-commerce API is running'})
    
    return app