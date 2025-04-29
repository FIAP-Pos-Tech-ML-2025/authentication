from flask import Blueprint, request, jsonify
from src.auth.manager import authenticate, generate_token
from src.utils import get_logger

logger = get_logger('auth-routes')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    user = data.get('username')
    pwd = data.get('password')
    if not user or not pwd:
        return jsonify({'error': 'username and password required'}), 400
    if not authenticate(user, pwd):
        return jsonify({'error': 'invalid credentials'}), 401
    token = generate_token(user)
    logger.info('User %s logged in', user)
    return jsonify({'access_token': token}), 200