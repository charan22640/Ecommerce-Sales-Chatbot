import multiprocessing
import os

# Server socket - Use PORT from environment (Render requirement)
port = os.getenv('PORT', '5000')
bind = f"0.0.0.0:{port}"
backlog = 2048

# Worker processes - Limit for free tier
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)
worker_class = 'sync'  # Using sync workers for better compatibility
worker_connections = 1000
timeout = 120  # Increased timeout for production
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
capture_output = True

# Process naming
proc_name = 'ecommerce_sales_bot'

# SSL
keyfile = os.getenv('SSL_KEYFILE')
certfile = os.getenv('SSL_CERTFILE')

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Server hooks
def on_starting(server):
    pass

def on_reload(server):
    pass

def on_exit(server):
    pass 