import multiprocessing

bind = ":8000"
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
graceful_timeout = 30
keepalive = 15
accesslog = "-"
errorlog = "-"
loglevel = "info"
