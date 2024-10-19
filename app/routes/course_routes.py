from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app.utils import token_required, token_author
from app.models import db, Course, Lesson
import os

course_routes = Blueprint('course_routes', __name__)

# Путь для сохранения загружаемых файлов
UPLOAD_FOLDER = 'app/static/uploads'  # Убедитесь, что эта папка существует
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename).replace('\\', '/')
        file.save(file_path)
        return filename
    return None

@course_routes.route('/add_course', methods=['POST'])
@token_required
def add_course():
    user_id = request.cookies.get('user_id') # Получите ID текущего пользователя из сессии
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    cover_image = request.files.get('cover_image')

    if not title or not description or not price or not cover_image:
        return jsonify({'message': 'All fields are required'}), 400
    
    cover_image_path = save_file(cover_image)
    new_course = Course(title=title, description=description, price=price, cover_image=cover_image_path, author_id=user_id)
    db.session.add(new_course)
    db.session.commit()

    return redirect(url_for('main_routes.index'))

@course_routes.route('/add_lesson/<int:course_id>', methods=['POST'])
@token_required
def add_lesson(course_id):
    title = request.form['title']
    video_1 = request.files.get('video_1')
    video_2 = request.files.get('video_2')
    quest = request.form['quest']
    quiz_id = request.form['quiz_id']  # При необходимости, используйте quiz_id

    if not title or not video_1:
        return jsonify({'message': 'Title and at least one video are required'}), 400

    video_1_path = save_file(video_1)
    video_2_path = save_file(video_2) if video_2 else None

    new_lesson = Lesson(title=title, course_id=course_id, video_1=video_1_path, video_2=video_2_path, quest=quest, quiz_id=quiz_id)
    db.session.add(new_lesson)
    db.session.commit()

    return jsonify({'message': 'Lesson added successfully!', 'lesson_id': new_lesson.id})


@course_routes.route('/edit_course/<int:course_id>', methods=['POST'])
@token_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    cover_image = request.files.get('cover_image')

    if title:
        course.title = title
    if description:
        course.description = description
    if price:
        course.price = price
    if cover_image:
        course.cover_image = save_file(cover_image)

    db.session.commit()
    return redirect(url_for('main_routes.my_courses', course_id=course_id))

@course_routes.route('/delete_course/<int:course_id>', methods=['POST'])
@token_author
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('main_routes.my_courses'))

@course_routes.route('/edit_lesson/<int:lesson_id>', methods=['POST'])
@token_required
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    title = request.form.get('title')
    video_1 = request.files.get('video_1')
    video_2 = request.files.get('video_2')
    quest = request.form.get('quest')

    if title:
        lesson.title = title
    if video_1:
        lesson.video_1 = save_file(video_1)
    if video_2:
        lesson.video_2 = save_file(video_2)
    if quest:
        lesson.quest = quest

    db.session.commit()
    return redirect(url_for('main_routes.edit_course_form', lesson_id=lesson_id))

@course_routes.route('/delete_lesson/<int:lesson_id>', methods=['POST'])
@token_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    return redirect(url_for('course_routes.create_lesson_form', course_id=lesson.course_id))
