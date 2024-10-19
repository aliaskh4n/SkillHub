from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    token = db.Column(db.String(128), nullable=False)
    is_author = db.Column(db.Boolean, default=False)
    courses = db.relationship('Course', backref='author', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    photo = db.Column(db.String(255))

# Модель курса
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cover_image = db.Column(db.String(255))  # Обложка курса (изображение)
    lessons = db.relationship('Lesson', backref='course', lazy=True)

    def can_add_lesson(self):
        return len(self.lessons) < 10

# Модель урока
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    video_1 = db.Column(db.String(255))  # Первое видео
    video_2 = db.Column(db.String(255))  # Второе видео
    quest = db.Column(db.Text)           # Квест (задание)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))  # Связь с квизом

# Модель квиза
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

# Модель вопроса для квиза
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)

# Модель платежей
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
