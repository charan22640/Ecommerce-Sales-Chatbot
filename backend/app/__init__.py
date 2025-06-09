from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .models.user import db
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
      # Load configuration
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging
    app.config['DEBUG'] = True  # Enable debug mode
    app.config['PROPAGATE_EXCEPTIONS'] = True  # Show detailed errors
    config[config_name].init_app(app)
      # Initialize extensions
    db.init_app(app)  # Initialize SQLAlchemy first
    
    # Configure CORS
    CORS(app,
         origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
         allow_credentials=True,
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         expose_headers=["Content-Range", "X-Content-Range"])
      # Add after_request handler to ensure CORS headers are always present
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://127.0.0.1:5173', 'http://localhost:5174', 'http://127.0.0.1:5174']:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        return response
    
    # Global OPTIONS handler for preflight requests
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({'status': 'ok'})
            origin = request.headers.get('Origin')
            if origin in ['http://localhost:5173', 'http://127.0.0.1:5173', 'http://localhost:5174', 'http://127.0.0.1:5174']:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
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
    from .api.chat import chat_bp
    from .api.products import products_bp
    from .api.cart import cart_bp
    from .api.orders import order_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    
    # Add health check route
    @app.route('/')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'E-commerce API is running'})
    
    @app.route('/api')
    def api_info():
        return jsonify({
            'status': 'ok',
            'message': 'E-commerce API',
            'endpoints': [
                '/api/auth/login',
                '/api/auth/register',
                '/api/products',
                '/api/cart',
                '/api/orders'
            ]
        })
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app