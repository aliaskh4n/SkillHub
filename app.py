from app import create_app

# Создаём приложение с помощью фабричной функции

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
