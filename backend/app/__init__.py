from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .models.user import db
from config import config
from datetime import datetime

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
        allowed_origins = [
            'https://ecommerce-frontend-1qfw.onrender.com',
            'https://ecommerce-backend-oyo1.onrender.com'
        ]
    else:
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['DEBUG'] = True
        allowed_origins = [
            'http://localhost:5173',  # Vite dev server
            'http://127.0.0.1:5173',  # Vite dev server alternative
            'http://localhost:5000',  # Flask dev server
            'http://127.0.0.1:5000'   # Flask dev server alternative
        ]
    
    app.config['PROPAGATE_EXCEPTIONS'] = True
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS with more secure options
    CORS(app, 
         resources={r"/*": {  # Allow CORS for all routes in production
             "origins": allowed_origins,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": [
                 "Content-Type",
                 "Authorization",
                 "X-Requested-With",
                 "Accept",
                 "Origin",
                 "Access-Control-Request-Method",
                 "Access-Control-Request-Headers"
             ],
             "supports_credentials": True,
             "expose_headers": ["Content-Range", "X-Content-Range"],
             "max_age": 3600
         }},
         supports_credentials=True)
    
    # Add after_request handler for additional security headers
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin, Access-Control-Request-Method, Access-Control-Request-Headers'
            response.headers['Access-Control-Max-Age'] = '3600'
            response.headers['Access-Control-Expose-Headers'] = 'Content-Range, X-Content-Range'
            # Additional security headers
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    # Add security headers in production
    @app.after_request
    def add_security_headers(response):
        if app.config['ENV'] == 'production':
            # Security headers
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Content-Security-Policy'] = "default-src 'self' https: data: blob: 'unsafe-inline'"
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        return response
    
    # Add OPTIONS handler for preflight requests
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({'status': 'ok'})
            origin = request.headers.get('Origin')
            if origin in allowed_origins:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Max-Age'] = '3600'
            return response
        return None
    
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
        try:
            from .models.product import Product
            product_count = Product.query.count()
            categories = db.session.query(Product.category).distinct().all()
            categories = [cat[0] for cat in categories]
            
            return jsonify({
                'status': 'ok',
                'message': 'E-commerce API is running',
                'database_status': 'connected',
                'products_count': product_count,
                'categories': categories,
                'timestamp': str(datetime.utcnow())
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e),
                'database_status': 'error',
                'timestamp': str(datetime.utcnow())
            }), 500
    
    # Health check route
    @app.route('/health')
    def health_check():
        try:
            # Check database connection
            db.session.execute('SELECT 1')
            db_status = 'healthy'
        except Exception as e:
            app.logger.error(f'Database health check failed: {str(e)}')
            db_status = 'unhealthy'

        # Check Redis connection if used
        redis_status = 'not_configured'
        if app.config.get('REDIS_URL'):
            try:
                from redis import Redis
                redis_client = Redis.from_url(app.config['REDIS_URL'])
                redis_client.ping()
                redis_status = 'healthy'
            except Exception as e:
                app.logger.error(f'Redis health check failed: {str(e)}')
                redis_status = 'unhealthy'

        response = {
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
            'components': {
                'database': db_status,
                'redis': redis_status
            },
            'version': '1.0.0',
            'environment': app.config.get('FLASK_ENV', 'production')
        }
        
        # If any component is unhealthy, return 503
        if 'unhealthy' in [db_status, redis_status]:
            return jsonify(response), 503
            
        return jsonify(response)
    
    # Add database seeding for production
    if config_name == 'production':
        with app.app_context():
            try:
                # Create tables
                db.create_all()
                
                # Check if products exist
                from .models.product import Product
                product_count = Product.query.count()
                
                if product_count == 0:
                    print("No products found. Seeding database...")
                    # Import and use seed data
                    from enhanced_seed_data import get_electronics_products
                    products_data = get_electronics_products()
                    
                    # Add products
                    for product_data in products_data:
                        product = Product(**product_data)
                        db.session.add(product)
                    
                    # Commit changes
                    db.session.commit()
                    print(f"Successfully seeded database with {len(products_data)} products!")
                else:
                    print(f"Database already contains {product_count} products.")
                    
            except Exception as e:
                print(f"Error during database initialization: {str(e)}")
                # Continue with application startup even if seeding fails
    
    return app