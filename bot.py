import telebot
from telebot import types
from app import create_app, db
from app.models import User
from app.utils import generate_token

# Токен от бота
TOKEN = '7482250325:AAEPLvrSN2OgRPx1x6bUmXnbGKATJtqIBzs'
bot = telebot.TeleBot(TOKEN)

app = create_app()

def webAppKeyboard(user_id): #создание клавиатуры с webapp кнопкой
   keyboard = types.InlineKeyboardMarkup()
   url = f"https://0f98-2a03-32c0-f000-8984-61dc-c98b-7b75-da63.ngrok-free.app/?user_id={user_id}"
   webAppTest = types.WebAppInfo(url) #создаем webappinfo - формат хранения url
   one_butt = types.InlineKeyboardButton(text="Тестовая страница", web_app=webAppTest) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру

   return keyboard #возвращаем клавиатуру

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_photos = bot.get_user_profile_photos(user_id)
    token = generate_token(user_id)

    with app.app_context():  # Activate application context
        # Use the session to check if the user already exists
        existing_user = db.session.get(User, user_id)
        if existing_user is None:
            # User does not exist, create a new one
            if user_photos.total_count > 0:
                # Получаем первую фотографию (самая последняя)
                photo_file_id = user_photos.photos[0][0].file_id
                
                # Загружаем файл фотографии
                photo_file_info = bot.get_file(photo_file_id)
                photo_url = f'https://api.telegram.org/file/bot{bot.token}/{photo_file_info.file_path}'
                new_user = User(username=user_name, id=user_id, photo=photo_url, token=token)
                db.session.add(new_user)
                db.session.commit()
        else:
            # User already exists, you can update their info if needed
            existing_user.username = user_name
            existing_user.token = token
            if user_photos.total_count > 0:
                photo_file_id = user_photos.photos[0][0].file_id
                photo_file_info = bot.get_file(photo_file_id)
                photo_url = f'https://api.telegram.org/file/bot{bot.token}/{photo_file_info.file_path}'
                existing_user.photo = photo_url
            db.session.commit()

    bot.send_message(message.chat.id, 'Привет, я бот для проверки телеграмм webapps!)', reply_markup=webAppKeyboard(message.chat.id))



# Запуск бота
if __name__ == '__main__':
    bot.polling()
