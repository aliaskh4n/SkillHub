from flask import Blueprint, jsonify, redirect, url_for, render_template, session, request
from app.utils import token_required, token_author
from app.models import User, Course, Lesson

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/', methods=['GET'])
def index():
    courses = Course.query.all()
    if request.cookies.get('user_id'):
        user_id = request.cookies.get('user_id')
    else:
        user_id = request.args.get('user_id')
    user = User.query.get(user_id)

    try:
        session['user_token'] = user.token
    except: 
        pass

    for course in courses:
        author = User.query.get(course.author_id)  # Найдем пользователя по author_id
        if author:
            setattr(author, 'author_name', author.username)  # Временное добавление имени автора
            setattr(author, 'author_photo', author.photo)  # Временное добавление фото автора
            course.author_name = author.author_name  # Добавляем имя автора к курсу
            course.author_photo = author.author_photo

    return render_template('index.html', courses=courses, photo=user.photo)

@main_routes.route('/course/<int:course_id>', methods=['GET'])
@token_required
def course(course_id):
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)
    course = Course.query.get(course_id)
    author = User.query.get(course.author_id)
    lessons = len(Lesson.query.filter_by(course_id=course_id).all())
    if author:
        setattr(author, 'author_name', author.username)
        setattr(author, 'author_photo', author.photo)  # Временное добавление фото автора
        course.author_name = author.author_name  # Добавляем имя автора к курсу\
        course.author_photo = author.author_photo 
    return render_template('course.html', course=course, photo=user.photo, lesson_count=lessons)

@main_routes.route('/create_course', methods=['GET'])
@token_required
def create_course_form():
    return render_template('create_course.html')


@main_routes.route('/my_courses', methods=['GET'])
@token_required
def my_courses():
    user_id = request.cookies.get('user_id')
    courses = Course.query.filter_by(author_id=user_id).all()
    return render_template('my_courses.html', courses=courses)

@main_routes.route('/my_lessons/<int:course_id>', methods=['GET'])
@token_required
def my_lessons(course_id):
    lesson = Lesson.query.filter_by(course_id=course_id).all()
    return render_template('my_lessons.html', lessons=lesson, course_id=course_id)    

@main_routes.route('/create_lesson/<int:course_id>', methods=['GET'])
@token_author
def create_lesson_form(course_id):
    return render_template('create_lesson.html', course_id=course_id)

@main_routes.route('/edit_course/<int:course_id>', methods=['GET'])
@token_required
def edit_course_form(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('edit_course.html', course=course)
    
@main_routes.route('/edit_lesson/<int:lesson_id>', methods=['GET'])
@token_required
def edit_lesson_form(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('edit_lesson.html', lesson=lesson)

@main_routes.route('/profile/<int:user_id>', methods=['GET'])
@token_required
def profile(user_id):
    if str(user_id) == request.cookies.get('user_id'):
        courses = Course.query.filter_by(author_id=user_id).all()
        return render_template('my_profile.html', courses=courses)
    else:
        return render_template('profile.html')