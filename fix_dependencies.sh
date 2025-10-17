#!/bin/bash

# Quick fix for missing dependencies on Linux
echo "🔧 Fixing missing dependencies..."

# Activate virtual environment
source venv/bin/activate

# Install missing cryptography module
echo "📦 Installing cryptography..."
pip install cryptography

# Install other potentially missing modules
echo "📦 Installing other dependencies..."
pip install bcrypt
pip install python-dotenv
pip install marshmallow
pip install requests

# Verify installation
echo "🔍 Verifying cryptography installation..."
python -c "
try:
    from cryptography.fernet import Fernet
    print('✅ Cryptography module installed successfully!')
except ImportError as e:
    print(f'❌ Cryptography import failed: {e}')
    exit(1)
"

echo "✅ Dependencies fixed! You can now run: python app/main.py"
