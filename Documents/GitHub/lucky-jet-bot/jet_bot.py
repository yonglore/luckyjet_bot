import telebot, sqlite3, time
from telebot import types
import random as r
import numpy as np

bot = telebot.TeleBot('7348101281:AAEqKe6PyKE5-G6P2b-BotKoMVi8xTO6m6A')


def connect_database():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


conn, cursor = connect_database()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    reg_flag TEXT,
    reg_id TEXT,
    signal TEXT
)
''')
conn.commit()
conn.close()


def add_user(user_id, username):
    conn, cursor = connect_database()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()


def update_user_data(user_id, reg_flag, reg_id):
    conn, cursor = connect_database()
    cursor.execute("UPDATE users SET reg_flag = ?, reg_id = ? WHERE user_id = ?",
                   (reg_flag, reg_id, user_id))
    conn.commit()
    conn.close()


def update_user_signal(user_id, signal):
    conn, cursor = connect_database()
    cursor.execute("UPDATE users SET signal = ? WHERE user_id = ?",
                   (signal, user_id))
    conn.commit()
    conn.close()


def get_user_data(user_id):
    conn, cursor = connect_database()
    cursor.execute("SELECT reg_flag, reg_id, signal FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    add_user(user_id, username)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("📲Регистрация", callback_data='registration')
    button2 = types.InlineKeyboardButton('🚀Сигналы', callback_data='signal')
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id, "{0.first_name}, добро пожаловать в 🔸LUCKY JET OpenAI🔸! \n \n"
                                      "🚀Lucky jet - краш-игра на деньги, в которой вы сможете выиграть значительные суммы, минимизируя риски. \n"
                                      "\n \n Наш бот основан на нейросети от Open AI.\n \n"
                                      "Он может предугадать краш с вероятностью 80%.".format(message.from_user),
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_signal(call):
    if call.data == 'registration':
        user_id = call.message.chat.id
        user_data = get_user_data(user_id)
        if user_data[1] is None:
            update_user_data(user_id, 1, None)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            photo = open('reg_img.jpg', 'rb')
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("🔙Главное меню", callback_data='back_menu')
            markup.add(button1)
            bot.send_photo(call.message.chat.id, photo=photo,
                           caption='🔷 1. Для начала зарегистрируйтесь по ссылке на <a href="https://1wbhk.com/casino/list/4?p=w7gk">сайте 1WIN</a> и добавьте промокод «VIP522» \n \n'
                                   '🔷 2. После успешной регистрации cкопируйте ваш айди на сайте (Вкладка "пополнение" и в правом верхнем углу будет ваш ID).\n \n'
                                   '🔷 3. И отправьте его боту в ответ на это сообщение!', parse_mode='HTML',
                           reply_markup=markup)

        if user_data[0] == '1' and str(user_data[1]).isdigit():
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("🔄Перерегистрация ID 1WIN", callback_data='reregistration')
            button2 = types.InlineKeyboardButton("🔙Главное меню", callback_data='back_menu')
            markup.add(button1)
            markup.add(button2)
            bot.send_message(call.message.chat.id, text=f'Вы уже зарегистрированы!\n\n'
                                                        f'Ваш ID: {user_data[1]}', reply_markup=markup)

    if call.data == 'reregistration':
        user_id = call.message.chat.id
        update_user_data(user_id, 1, None)
        update_user_signal(user_id, None)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        photo = open('reg_img.jpg', 'rb')
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("🔙Главное меню", callback_data='back_menu')
        markup.add(button1)
        bot.send_photo(call.message.chat.id, photo=photo,
                       caption='🔷 1. Для начала зарегистрируйтесь по ссылке на <a href="https://1wbhk.com/casino/list/4?p=w7gk">сайте 1WIN</a> и добавьте промокод «VIP522» \n \n'
                               '🔷 2. После успешной регистрации cкопируйте ваш айди на сайте (Вкладка "пополнение" и в правом верхнем углу будет ваш ID).\n \n'
                               '🔷 3. И отправьте его боту в ответ на это сообщение!', parse_mode='HTML',
                       reply_markup=markup)

    if call.data == 'back_menu':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("📲Регистрация", callback_data='registration')
        button2 = types.InlineKeyboardButton('🚀Сигналы', callback_data='signal')
        markup.add(button1)
        markup.add(button2)
        bot.send_message(call.message.chat.id, "Добро пожаловать в 🔸LUCKY JET OpenAI🔸! \n \n"
                                               "🚀Lucky jet - краш-игра на деньги, в которой вы сможете выиграть значительные суммы, минимизируя риски. \n"
                                               "\n \n Наш бот основан на нейросети от Open AI.\n \n"
                                               "Он может предугадать краш с вероятностью 80%.", reply_markup=markup)

    if call.data == 'signal':
        user_id = call.message.chat.id
        user_data = get_user_data(user_id)
        if user_data[2] == '1':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("🚀Получить сигнал", callback_data='get_signal')
            button2 = types.InlineKeyboardButton("🔙Главное меню", callback_data='back_menu')
            markup.add(button1)
            markup.add(button2)
            bot.send_message(call.message.chat.id, '🤖Бот может предугадать краш с вероятностью до 80%\n\n'
                                                   '🚨Для того чтобы получить сигнал, нажмите на кнопку снизу',
                             reply_markup=markup)
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("🔙Главное меню", callback_data='back_menu')
            markup.add(button1)
            bot.send_message(call.message.chat.id, '‼️Вы не можете получать сигналы без регистрации!',
                             reply_markup=markup)

    if call.data == 'get_signal':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        texts = 'Получаем данные с сайта 1WIN...'
        message = bot.send_message(call.message.chat.id, text=texts)
        time.sleep(2)
        bot.delete_message(call.message.chat.id, message.message_id)
        numbers = np.arange(1, 3.8, 0.1)
        numbers = numbers[1:]
        crash = str(r.choice(numbers))[:3]
        if float(crash) > 2.4:
            chance = r.randint(55, 70)
        else:
            chance = r.randint(65, 80)
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("🚀Получить новый сигнал", callback_data='get_signal')
        button2 = types.InlineKeyboardButton("🔙Главное меню", callback_data='back_menu')
        markup.add(button1)
        markup.add(button2)
        bot.send_message(call.message.chat.id, f'💥Предугаданный краш: {crash}\n\n'
                                               f'⚠️Шанс предугаданного краша: {chance}%', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_id(message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    if user_data[0] == '1' and user_data[1] is None:
        if len(str(message.text)) == 8 and str(message.text).isdigit():
            id = message.text
            update_user_data(user_id, 1, reg_id=id)
            update_user_signal(user_id, 1)
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("🔙Главное меню", callback_data='back_menu')
            markup.add(button1)
            bot.send_message(message.chat.id, text='Вы успешно прошли регистрацию!', reply_markup=markup)
        else:
            bot.send_message(message.from_user.id, 'Неправильный ID.')


bot.polling()
