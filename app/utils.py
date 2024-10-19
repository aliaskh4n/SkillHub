from functools import wraps
from flask import session, abort, request, jsonify
from app.models import User, Course
import hashlib
import time

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        if not user_id:  # Если user_id нет в cookies
            return jsonify({"error": "Access denied: user_id not found in cookies."}), 403

        user = User.query.get(user_id)
        if not user:  # Если пользователь не найден
            return jsonify({"error": "Access denied: user not found."}), 403

        user_token = session.get('user_token')  # Получаем токен из сессии
        if not user_token or user_token != user.token:
            return jsonify({"error": "Access denied: invalid user token."}), 403

        return f(*args, **kwargs)
    return decorated_function


def token_author(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        if not user_id:  # Если user_id нет в cookies
            return jsonify({"error": "Access denied: user_id not found in cookies."}), 403

        user = User.query.get(user_id)
        if not user:  # Если пользователь не найден
            return jsonify({"error": "Access denied: user not found."}), 403

        course_id = kwargs.get('course_id')
        course = Course.query.get(course_id)
        if not course:  # Если курс не найден
            return jsonify({"error": "Course not found."}), 404

        user_token = session.get('user_token')  # Получаем токен из сессии
        if not user_token or user_token != user.token:
            return jsonify({"error": "Access denied: invalid user token."}), 403

        if str(user_id) != str(course.author_id):
            return jsonify({"error": "Access denied: user is not the course author."}), 403

        return f(*args, **kwargs)
    return decorated_function

def generate_token(user_id):
    # Генерация токена с использованием user_id и времени
    token_data = f"{user_id}:{time.time()}"
    token = hashlib.sha256(token_data.encode()).hexdigest()
    
    return token
