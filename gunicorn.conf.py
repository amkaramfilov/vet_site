# Gunicorn configuration file
import multiprocessing

# Bind to localhost
bind = "127.0.0.1:8000"

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "sync"

# Timeout for requests
timeout = 120

# Access log
accesslog = "-"

# Error log
errorlog = "-"

# Log level
loglevel = "info"

# Reload on code changes (disable in production)
reload = False

# Max requests per worker before restart
max_requests = 1000
max_requests_jitter = 50
