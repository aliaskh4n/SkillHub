from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Подключаем конфигурацию
    app.config.from_object('config.Config')

    # Инициализация всех расширений с приложением
    try:
        print('sucsess')
        db.init_app(app)
        migrate.init_app(app, db)
    except:
        print('error')
    # Импортируем и регистрируем маршруты
    from app.routes.main_routes import main_routes
    from app.routes.course_routes import course_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(course_routes)

    # Импорт моделей и создание таблиц в контексте приложения
    with app.app_context():
        from app.models import User, Course, Lesson, Quiz, Question, Payment
        db.create_all()  # Создайте все таблицы, если они еще не существуют

    return app
