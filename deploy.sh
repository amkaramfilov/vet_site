#!/bin/bash
# Deployment script for Vet Clinic Management System
# Run this script on your Hetzner server

set -e  # Exit on error

# Configuration
APP_DIR="/var/www/vet_clinic"
VENV_DIR="$APP_DIR/.venv"
USER="www-data"

echo "=== Vet Clinic Deployment Script ==="

# Navigate to app directory
cd $APP_DIR

# Pull latest code (if using git)
echo "Pulling latest code..."
git pull origin main

# Activate virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Restart Gunicorn
echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

# Restart Nginx
echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "=== Deployment Complete ==="
