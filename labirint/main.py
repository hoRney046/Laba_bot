import random

import telebot

from mg import get_map_cell

bot = telebot.TeleBot('7055753206:AAFbTFlhtgQy0Oa-QKLzApb-A3WDLgFTdQo')
cols, rows = 8, 8
ballans = 500
skins = ["👩", "👨", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "👽", "🐵", "🐺", "🐱", "🐯", "🦒", "🦊", "🦝", "🐭", "🐹"]
ourskins = []

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('Влево', callback_data='left'),
             telebot.types.InlineKeyboardButton('Вверх', callback_data='up'),
             telebot.types.InlineKeyboardButton('Вниз', callback_data='down'),
             telebot.types.InlineKeyboardButton('Вправо', callback_data='right'))

maps = {}


def get_map_str(map_cell, player):
    map_str = ""
    for y in range(rows * 2 - 1):
        for x in range(cols * 2 - 1):
            if map_cell[x + y * (cols * 2 - 1)]:
                map_str += "⬛"
            elif (x, y) == player:
                map_str += c
            else:
                map_str += "⬜"
        map_str += "\n"

    return map_str


@bot.message_handler(commands=['play'])
def play_message(message):
    map_cell = get_map_cell(cols, rows)

    user_data = {
        'map': map_cell,
        'x': 0,
        'y': 0
    }

    maps[message.chat.id] = user_data

    bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    user_data = maps[query.message.chat.id]
    new_x, new_y = user_data['x'], user_data['y']

    if query.data == 'left':
        new_x -= 1
    if query.data == 'right':
        new_x += 1
    if query.data == 'up':
        new_y -= 1
    if query.data == 'down':
        new_y += 1

    if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
        return None
    if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
        return None

    user_data['x'], user_data['y'] = new_x, new_y

    if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
        bot.edit_message_text(chat_id=query.message.chat.id,
                              message_id=query.message.id,
                              text="Вы выиграли")
        ballans2(ballans)
        return None
    bot.edit_message_text(chat_id=query.message.chat.id,
                          message_id=query.message.id,
                          text=get_map_str(user_data['map'], (new_x, new_y)),
                          reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Добро пожаловать в игру 'Бегущий в лабиринте'.\n"
                                      "Обучение:\n"
                                      "У тебя на балансе есть подарочные 500 point.\n"
                                      "Заходи и покупай себе скины - /lottery.\n"
                                      "Дальше зайди в инвентарь - /skin.\n"
                                      "Выбирай скин 1-5 - например /1\n"
                                      "И начиный играть - /play")


@bot.message_handler(commands=['lottery'])
def lottery(message):
    if ballans > 0:
        k = random.choice(skins)
        ourskins.append(k)
        skins.remove(k)
        ballans1(ballans)
        bot.send_message(message.chat.id, f"Ваш скин{k}")
    elif len(ourskins) > 5:
        bot.send_message(message.chat.id, "У вас полный инвентарь")
    else:
        bot.send_message(message.chat.id, "Нету денег, иди играй")


@bot.message_handler(commands=['balans'])
def balans(message):
    bot.send_message(message.chat.id, f"Ваш баланс: {ballans} point")


def ballans1(b):
    global ballans
    ballans -= 100
    return ballans


def ballans2(b):
    global ballans
    ballans += 100
    return ballans


@bot.message_handler(commands=['skin'])
def skin(message):
    bot.send_message(message.chat.id, f"Ваши скины: {ourskins[:5]}")


@bot.message_handler(commands=['1'])
def one(message):
    bot.send_message(message.chat.id, f"Вы выбрали скин №1: {ourskins[0]}")
    global c
    c = ourskins[0]


@bot.message_handler(commands=['2'])
def one(message):
    bot.send_message(message.chat.id, f"Вы выбрали скин №2: {ourskins[1]}")
    global c
    c = ourskins[1]


@bot.message_handler(commands=['3'])
def one(message):
    bot.send_message(message.chat.id, f"Вы выбрали скин №3: {ourskins[2]}")
    global c
    c = ourskins[2]


@bot.message_handler(commands=['4'])
def one(message):
    bot.send_message(message.chat.id, f"Вы выбрали скин №4: {ourskins[3]}")
    global c
    c = ourskins[3]


@bot.message_handler(commands=['5'])
def one(message):
    bot.send_message(message.chat.id, f"Вы выбрали скин №5: {ourskins[4]}")
    global c
    c = ourskins[4]


@bot.message_handler(commands=['5'])
def one(message):
    bot.send_message(message.chat.id, f"Вы выбрали скин №5: {ourskins[4]}")
    global c
    c = ourskins[4]


@bot.message_handler(commands=['info'])
def one(message):
    bot.send_message(message.chat.id,
                     f"Команды: \n"
                     f" /start - обученние\n /play - начать игру\n /lottery - получить скины \n"
                     f" /skin - скины\n /1 - выбор скина\n"
                     f"/balans - баланс\n /sell - продать все скины")


@bot.message_handler(commands=['sell'])
def one(message):
    if len(ourskins) > 0:
        ballans2(ballans)
        ourskins.clear()
        bot.send_message(message.chat.id,
                         f"Ты продал все скины тебе на баланс зачислено 100 point")
    else:
        bot.send_message(message.chat.id,
                         f"У тебя не скинов")


bot.polling(none_stop=False, interval=0)
