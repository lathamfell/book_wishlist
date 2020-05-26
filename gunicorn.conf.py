import os

bind = "0.0.0.0:8000"
workers = 1
worker_class = "gevent"
timeout = 300
graceful_timeout = 300
loglevel = os.getenv("LOG_LEVEL", "info")
keepalive = 300
