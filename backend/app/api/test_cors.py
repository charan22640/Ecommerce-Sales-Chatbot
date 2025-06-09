from flask import jsonify
from . import auth_bp

@auth_bp.route('/test-cors', methods=['GET', 'OPTIONS'])
def test_cors():
    response = jsonify({
        'message': 'CORS test successful',
        'status': 'ok'
    })
    return response, 200
