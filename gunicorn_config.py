"""
Gunicorn configuration file for production deployment on Render
"""
import os

# Server Socket - CRITICAL: Must bind to Render's PORT
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
backlog = 2048

# Worker Processes - Keep LOW for free tier (512MB RAM limit)
workers = 1  # Start with 1 worker for stability
worker_class = 'sync'
worker_connections = 100
max_requests = 500
max_requests_jitter = 25
timeout = 180  # Longer timeout for ML model loading
keepalive = 5

# Server Mechanics
daemon = False
pidfile = None

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process Naming
proc_name = 'health_assessment_app'

# Preloading - Disabled to reduce memory usage on startup
preload_app = False

# Server Hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    port = os.environ.get('PORT', '10000')
    print(f"🚀 Starting Health Assessment Application on port {port}...")

def when_ready(server):
    """Called just after the server is started."""
    port = os.environ.get('PORT', '10000')
    print(f"✅ Health Assessment Application is ready!")
    print(f"🌐 Listening on 0.0.0.0:{port}")

def on_exit(server):
    """Called just before exiting Gunicorn."""
    print("👋 Shutting down Health Assessment Application...")
