from flask import Blueprint, request, jsonify
from proj.services.compiler_service import compile_code


compiler_bp = Blueprint('compiler', __name__)

@compiler_bp.route('/compile', methods=['POST', 'OPTIONS'])
def compile():
    if request.method == 'OPTIONS':
        return '', 200  # Handle preflight
    compile_request = request.get_json()
    code = compile_request.get('code', '')
    code = code.encode().decode('unicode_escape')  # Ensure code is a string
    if not code:
        return jsonify({"error": "No code provided"}), 400
    result = compile_code(code)
    return result