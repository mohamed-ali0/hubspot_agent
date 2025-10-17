"""
Help API endpoint - Returns documentation for all endpoints
"""

import os
import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from pathlib import Path

bp = Blueprint('help', __name__)

def load_help_data(module_name, endpoint_name=None):
    """Load help data from JSON files"""
    try:
        help_dir = Path(__file__).parent / 'help' / module_name
        
        if endpoint_name:
            # Load specific endpoint help
            help_file = help_dir / f"{endpoint_name}.json"
            if help_file.exists():
                with open(help_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return None
        else:
            # Load all endpoints for a module
            help_data = {}
            if help_dir.exists():
                for help_file in help_dir.glob("*.json"):
                    endpoint = help_file.stem
                    with open(help_file, 'r', encoding='utf-8') as f:
                        help_data[endpoint] = json.load(f)
            return help_data
    except Exception as e:
        return {"error": f"Failed to load help data: {str(e)}"}

@bp.route('', methods=['GET'])
def get_help_overview():
    """Get overview of all available help documentation"""
    try:
        help_dir = Path(__file__).parent / 'help'
        modules = {}
        
        if help_dir.exists():
            for module_dir in help_dir.iterdir():
                if module_dir.is_dir():
                    module_name = module_dir.name
                    endpoints = []
                    
                    for help_file in module_dir.glob("*.json"):
                        endpoint = help_file.stem
                        endpoints.append(endpoint)
                    
                    modules[module_name] = {
                        "endpoints": endpoints,
                        "count": len(endpoints)
                    }
        
        return jsonify({
            "title": "HubSpot Logging AI Agent - API Help",
            "description": "Comprehensive API documentation with request/response formats and usage tips",
            "version": "1.0.0",
            "modules": modules,
            "usage": {
                "get_all_endpoints": "/api/help/{module}",
                "get_specific_endpoint": "/api/help/{module}/{endpoint}",
                "search_endpoints": "/api/help/search?q={query}"
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<module>', methods=['GET'])
def get_module_help(module):
    """Get help documentation for all endpoints in a module"""
    try:
        help_data = load_help_data(module)
        
        if help_data is None:
            return jsonify({'error': f'Module "{module}" not found'}), 404
        
        if "error" in help_data:
            return jsonify(help_data), 500
        
        return jsonify({
            "module": module,
            "endpoints": help_data,
            "count": len(help_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<module>/<endpoint>', methods=['GET'])
def get_endpoint_help(module, endpoint):
    """Get help documentation for a specific endpoint"""
    try:
        help_data = load_help_data(module, endpoint)
        
        if help_data is None:
            return jsonify({'error': f'Endpoint "{endpoint}" not found in module "{module}"'}), 404
        
        if "error" in help_data:
            return jsonify(help_data), 500
        
        return jsonify({
            "module": module,
            "endpoint": endpoint,
            "documentation": help_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['GET'])
def search_help():
    """Search help documentation"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        help_dir = Path(__file__).parent / 'help'
        results = []
        
        if help_dir.exists():
            for module_dir in help_dir.iterdir():
                if module_dir.is_dir():
                    module_name = module_dir.name
                    
                    for help_file in module_dir.glob("*.json"):
                        endpoint = help_file.stem
                        
                        try:
                            with open(help_file, 'r', encoding='utf-8') as f:
                                help_data = json.load(f)
                                
                            # Search in title, description, and tips
                            searchable_text = f"{help_data.get('title', '')} {help_data.get('description', '')} {help_data.get('tips', '')}".lower()
                            
                            if query in searchable_text:
                                results.append({
                                    "module": module_name,
                                    "endpoint": endpoint,
                                    "title": help_data.get('title', ''),
                                    "description": help_data.get('description', ''),
                                    "url": f"/api/help/{module_name}/{endpoint}"
                                })
                        except Exception:
                            continue
        
        return jsonify({
            "query": query,
            "results": results,
            "count": len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/modules', methods=['GET'])
def get_modules():
    """Get list of all available modules"""
    try:
        help_dir = Path(__file__).parent / 'help'
        modules = []
        
        if help_dir.exists():
            for module_dir in help_dir.iterdir():
                if module_dir.is_dir():
                    module_name = module_dir.name
                    endpoint_count = len(list(module_dir.glob("*.json")))
                    
                    modules.append({
                        "name": module_name,
                        "endpoint_count": endpoint_count,
                        "url": f"/api/help/{module_name}"
                    })
        
        return jsonify({
            "modules": modules,
            "count": len(modules)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
