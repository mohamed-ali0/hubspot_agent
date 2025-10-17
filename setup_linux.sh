#!/bin/bash

# HubSpot Logging AI Agent - Linux Setup Script
# This script installs all dependencies and sets up the environment

echo "🚀 HubSpot Logging AI Agent - Linux Setup"
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ Python 3 and pip3 are available"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Check if all dependencies are installed
echo "🔍 Verifying installation..."
python -c "
import flask
import flask_sqlalchemy
import flask_migrate
import flask_jwt_extended
import flask_cors
import sqlalchemy
import cryptography
import bcrypt
import requests
import marshmallow
import dotenv
print('✅ All dependencies installed successfully!')
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Copy .env.example to .env and configure your settings"
    echo "2. Run: python app/main.py"
    echo "3. Test the API at: http://localhost:5000/api/health"
    echo ""
    echo "🔧 To activate the virtual environment in the future:"
    echo "   source venv/bin/activate"
    echo ""
else
    echo "❌ Some dependencies failed to install. Please check the error messages above."
    exit 1
fi
