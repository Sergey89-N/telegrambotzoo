import telebot
from telebot import types


TOKEN = '7982205354:AAGszmOKcigPtVba6PX7fZ39DS7lupz459Y'
bot = telebot.TeleBot(TOKEN)


# Вопросы и ответы для викторины
quiz_questions = [
    {
        'question': 'Какое животное считается символом мудрости?',
        'options': ['Сова', 'Панда', 'Рысь', 'Лошадь', 'Попугай', 'Собака'],
        'answer': 'Сова',
    },
    {
        'question': 'Какое животное символизирует силу и мужество?',
        'options': ['Лев', 'Панда', 'Лиса', 'Морж', 'Попугай', 'Пингвин'],
        'answer': 'Лев',
    },
    {
        'question': 'Какое животное вам больше нравится?',
        'options': ['Амурский тигр', 'Африканская соня', 'Белая сова', 'Большая панда', 'Гоголь',
                    'Благородный зелёно-красный попугай'],
        'answer': 'Амурский тигр',
    },
    {
        'question': 'Какой у вас образ жизни?',
        'options': ['Активный', 'Люблю поспать', 'Спокойный', 'Творческий', 'Приключенческий',
                    'Люблю поболтать'],
        'answer': 'Активный',
    },

]

user_scores = {}
user_question_index = {}


# Приветственное сообщение
@bot.message_handler(commands=['start'])
def start_quiz(message):
    bot.send_message(message.chat.id, "Привет! Добро пожаловать в викторину. Начнем!")
    user_scores[message.from_user.id] = 0
    user_question_index[message.from_user.id] = 0
    ask_question(message.chat.id, 0)


# команды
@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message):
    help_text = (
        "Добро пожаловать в викторину о животных!\n"
        "Вот команды, которые вы можете использовать:\n"
        "/start - Начать викторину\n"
        "/feedback - Оставить отзыв\n"
        "/contact - Связаться с нами\n"
        "/share - Поделиться результатами в социальных сетях\n"
        "/help - Получить помощь\n"
        "/options - Программа опеки над животными"
    )
    bot.send_message(message.chat.id, help_text)


# Соц сети
@bot.message_handler(commands=['share'])
def share_results(message: telebot.types.Message):
    user_id = message.from_user.id
    score = user_scores.get(user_id, 0)
    share_text = f"Я прошел викторину на тему животных и набрал {score} баллов! Попробуйте и вы: https://t.me/YamalBoy"
    bot.send_message(message.chat.id, share_text)


# Контакты
@bot.message_handler(commands=['contact'])
def contact(message: telebot.types.Message):
    contact_info = "Если у вас есть вопросы, свяжитесь с нами:\nТелефон: +79129177011\nEmail: Nehoroshkov76@mail.ru"
    bot.send_message(message.chat.id, contact_info)


# Отзыв
@bot.message_handler(commands=['feedback'])
def feedback(message):
    bot.send_message(message.chat.id, "Пожалуйста, оставьте свой отзыв:")
    bot.register_next_step_handler(message, process_feedback)


def process_feedback(message: telebot.types.Message):
    feedback_text = message.text
    with open('feedback.txt', 'a') as f:
        f.write(f"{message.from_user.username}: {feedback_text}\n")
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")


# Программа опеки
@bot.message_handler(commands=['options'])
def care_program(message: telebot.types.Message):
    info = (
        "Программа опеки за животными позволяет вам стать частью заботы о питомцах.\n"
        "Вы можете помочь, участвуя в мероприятиях, финансируя уход за животными или даже усыновив питомца.\n"
        "Если вас интересует, как помочь, свяжитесь с нами!"
    )
    bot.send_message(message.chat.id, info)


# Функция для запроса вопросов
def ask_question(chat_id, question_index):
    if question_index < len(quiz_questions):
        question_data = quiz_questions[question_index]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for option in question_data['options']:
            markup.add(option)
        bot.send_message(chat_id, question_data['question'], reply_markup=markup)
    else:
        show_results(chat_id)


# Обработка ответов
@bot.message_handler(func=lambda message: True)
def handle_answer(message: telebot.types.Message):
    user_id = message.from_user.id
    if user_id not in user_scores:
        user_scores[user_id] = 0
        user_question_index[user_id] = 0

    current_question_index = user_question_index[user_id]

    if current_question_index < len(quiz_questions):
        correct_answer = quiz_questions[current_question_index]['answer']
        if message.text.strip() == correct_answer:
            user_scores[user_id] += 1

        user_question_index[user_id] += 1

        ask_question(message.chat.id, user_question_index[user_id])
    else:
        show_results(message.chat.id)


# Подведение итогов
def show_results(chat_id):
    user_id = chat_id
    score = user_scores.get(user_id, 0)
    bot.send_message(chat_id, f"Ваш результат: {score} из {len(quiz_questions)}")

    if score == 4:
        bot.send_message(chat_id, "Вы идеально подходите для ухода за животными!")
    else:
        bot.send_message(chat_id, "Вы можете попробовать еще раз!")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Попробовать ещё раз?')
    bot.send_message(chat_id, "Хотите пройти викторину снова?", reply_markup=markup)


# Пройти ещё раз
@bot.message_handler(func=lambda message: message.text.strip() == "Попробовать ещё раз?")
def restart_quiz(message: telebot.types.Message):
    user_id = message.from_user.id
    user_scores[user_id] = 0  # Сбросить счет
    user_question_index[user_id] = 0
    start_quiz(message)  # Начать викторину заново


# Завершение
@bot.message_handler(func=lambda message: message.text == "Завершить викторину")
def end_quiz(message: telebot.types.Message):
    user_id = message.from_user.id
    score = user_scores.get(user_id, 0)

    print(f"User  ID: {user_id}, Score: {score}")  # Отладочное сообщение
# На случай, если не доступны фото
    try:
        if score > 3:
            bot.send_photo(message.chat.id, photo='https://cdn.culture.ru/images/f2d6398e-370c-570b-9d6d-beb18e999f4c',
                           caption="Ты Амурский тигр!")
        else:
            bot.send_photo(message.chat.id,
                           photo='https://avatars.mds.yandex.net/i?id=e58d96e66773ea306dc5418359fe9747_l-5236483-images-thumbs&n=13',
                           caption="Твоё животное – кто-то другой!")
    except Exception as e:
        print(f"Ошибка при отправке фотографии: {e}")

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Попробовать ещё раз?")
    markup.add(item1)
    bot.send_message(message.chat.id, "Что ты хочешь сделать дальше?", reply_markup=markup)


# Запуск бота
bot.polling()
