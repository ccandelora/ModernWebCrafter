import multiprocessing
import os

# Project paths
project_dir = '/var/www/ModernWebCrafter'
venv_path = '/var/www/ModernWebCrafter/venv/lib/python3.12/site-packages'

# Gunicorn settings
bind = "unix:/var/www/ModernWebCrafter/modernwebcrafter.sock"
workers = multiprocessing.cpu_count() * 2 + 1
pythonpath = project_dir
preload_app = True

# Logging
accesslog = "/var/www/ModernWebCrafter/logs/gunicorn-access.log"
errorlog = "/var/www/ModernWebCrafter/logs/gunicorn-error.log"
loglevel = "debug"
