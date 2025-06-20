import os
from app import create_app
from config import config

# Get the environment from environment variable, default to development
env = os.getenv('FLASK_ENV', 'development')
if env not in config:
    env = 'production'  # Force production if invalid environment
app = create_app(env)

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # For production with Gunicorn
    application = app