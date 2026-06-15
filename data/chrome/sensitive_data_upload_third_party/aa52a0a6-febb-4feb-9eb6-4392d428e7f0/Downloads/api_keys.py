import os
import sys
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# API Keys for external services
API_KEY = 'sk-1234567890abcdef'
SECRET_KEY = 'wxyz-9876543210'

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'

def validate_api_key(api_key):
    """Simple API key validation for demonstration"""
    return api_key == API_KEY

@app.route('/api/v1/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'api-keys-demo'})

@app.route('/api/v1/data', methods=['POST'])
def get_data():
    """Endpoint that requires API key authentication"""
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    api_key = auth_header.replace('Bearer ', '')
    
    if not validate_api_key(api_key):
        return jsonify({'error': 'Invalid API key'}), 403
    
    # Process request data
    request_data = request.get_json(silent=True) or {}
    
    # Simulate data processing
    response_data = {
        'message': 'Data retrieved successfully',
        'data': {
            'items': ['item1', 'item2', 'item3'],
            'count': 3,
            'api_version': '1.0'
        }
    }
    
    return jsonify(response_data)

@app.route('/api/v1/config', methods=['GET'])
def get_config():
    """Endpoint that exposes configuration (intentionally insecure)"""
    config = {
        'api_key': API_KEY,
        'secret_key': SECRET_KEY,
        'database_url': DATABASE_URL,
        'debug_mode': DEBUG_MODE
    }
    return jsonify(config)

if __name__ == '__main__':
    print(f"Starting API service with API_KEY: {API_KEY[:5]}...")
    print(f"Secret key configured: {bool(SECRET_KEY)}")
    app.run(host='0.0.0.0', port=5000, debug=DEBUG_MODE)