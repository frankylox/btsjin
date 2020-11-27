import telebot
import config
import pandas as pd
from telebot import types

bot = telebot.TeleBot(config.token)

cards = pd.DataFrame(columns=['album', 'version', 'active'])
cards['album'] = config.albums
cards['active'] = 0

cards_withoutver = pd.DataFrame(columns=['album', 'active'])
cards_withoutver['album'] = config.albums_uniq
cards_withoutver['active'] = 0

for i in range(4):
    cards.loc[i + 8, 'version'] = config.versions_of_HER[i]
    cards.loc[i + 12, 'version'] = config.versions_of_TEAR[i]
    cards.loc[i + 16, 'version'] = config.versions_of_ANSWER[i]
    cards.loc[i + 20, 'version'] = i + 1
    cards.loc[i + 24, 'version'] = i + 1
cards.fillna(0)


@bot.message_handler(commands=["start"])
def cd_start(message):
    bot.send_message(message.chat.id, config.greeting)


@bot.message_handler(commands=["addcard"])
def add_card_button(message):
    keyboard = types.InlineKeyboardMarkup()
    button_ORUL = types.InlineKeyboardButton(text='O!RUL8,2?', callback_data='0')
    button_SLA = types.InlineKeyboardButton(text='SKOOL LUV AFFAIR', callback_data='1')
    button_DNW = types.InlineKeyboardButton(text='DARK & WILD', callback_data='2')
    button_HYYH1 = types.InlineKeyboardButton(text='THE MOST BEAUTIFUL MOMENT IN LIFE PT.1', callback_data='3')
    button_HYYH2 = types.InlineKeyboardButton(text='THE MOST BEAUTIFUL MOMENT IN LIFE PT.2', callback_data='4')
    button_YF = types.InlineKeyboardButton(text='THE MOST BEAUTIFUL MOMENT IN LIFE: YOUNG FOREVER', callback_data='5')
    button_WIN = types.InlineKeyboardButton(text='WINGS', callback_data='6')
    button_YNWA = types.InlineKeyboardButton(text='YOU NEVER WALK ALONE', callback_data='7')
    button_LYH = types.InlineKeyboardButton(text='LOVE YOURSELF: HER', callback_data='8')
    button_LYT = types.InlineKeyboardButton(text='LOVE YOURSELF: TEAR', callback_data='9')
    button_LYA = types.InlineKeyboardButton(text='LOVE YOURSELF: ANSWER', callback_data='10')
    button_MOTSPers = types.InlineKeyboardButton(text='MAP OF THE SOUL : PERSONA', callback_data='11')
    button_MOTS7 = types.InlineKeyboardButton(text='MAP OF THE SOUL: 7', callback_data='12')
    keyboard.add(button_ORUL, button_SLA, button_DNW, button_HYYH1, button_HYYH2, button_YF, button_WIN, button_YNWA,
                 button_LYH, button_LYT, button_LYA, button_MOTSPers, button_MOTS7)
    bot.send_message(message.chat.id, "Выбери альбом, карту которого ты хочешь добавить", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def add_incollection(call):
    bot.answer_callback_query(callback_query_id=call.id)
    answer = ''
    sv = 0
    for ch in range(len(config.albums_uniq)):
        if call.data == str(ch):
            answer = config.albums_uniq[ch]
            sv = ch
    bot.send_message(call.message.chat.id, 'Ты выбрал/а альбом ' + answer + '!')
    if cards_withoutver.loc[sv, 'active'] == 1:
        bot.send_message(call.message.chat.id, 'Эта карта уже есть в коллекции :)')
    else:
        cards_withoutver.loc[sv, 'active'] = 1


@bot.message_handler(commands=["mycards"])
def mycards(message):
    bot.send_message(message.chat.id, 'Твоя коллекция:')
    for w in range(len(config.albums_uniq)):
        if cards_withoutver.loc[w, 'active'] == 1:
            bot.send_message(message.chat.id, cards_withoutver.loc[w, 'album'])


if __name__ == '__main__':
    bot.polling(none_stop=True)
