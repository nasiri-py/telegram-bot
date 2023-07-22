import telebot
import time
from datetime import datetime


bot = telebot.TeleBot("code")


btn1 = telebot.types.InlineKeyboardButton("link", url='https://t.me/telegram')
btn2 = telebot.types.InlineKeyboardButton('info', callback_data='info_call')
markup = telebot.types.InlineKeyboardMarkup(row_width=2)
markup.add(btn1, btn2)

markup_valid = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn = telebot.types.KeyboardButton(text='Send Phone Number', request_contact=True)
markup_valid.add(btn)


@bot.callback_query_handler(func= lambda call:True)
def callback(call):
    if call.data == 'info_call':
        # bot.reply_to(call.id, 'Info')
        bot.answer_callback_query(call.id, 'Info', show_alert=True)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'Hi\nPlease verify your phone number.', reply_markup=markup_valid)
    bot.register_next_step_handler(msg, validation)

verify_status = False
@bot.message_handler(func= lambda call:True)
def validation(message):
    print(message)
    global verify_status
    global msg
    if verify_status:
        bot.register_next_step_handler(msg, calc)
    if message.content_type == 'contact':
        bot.send_chat_action(message.chat.id, action='upload_photo')
        time.sleep(2)
        ph =bot.send_photo(message.chat.id, open('file.jpg', 'rb'), caption='No caption')
        global key_markup
        key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        key_markup.add('fullname', 'age')
        bot.reply_to(ph, 'This message will remove after 15 seconds, Please save it.', reply_markup=markup)
        time.sleep(15)
        msg = bot.reply_to(ph, 'Now what can I do for you?', reply_markup=key_markup)
        bot.delete_message(chat_id=message.chat.id, message_id=ph.message_id)
        verify_status = True
        bot.register_next_step_handler(msg, calc)

    else:
        if not verify_status:
            ms =bot.send_message(message.chat.id, 'Please click on "Send Phone Number" button to verify your account.', reply_markup=markup_valid)
            bot.register_next_step_handler(ms, validation)


def calc(message):
    if message.text == 'fullname':
        msg = bot.send_message(message.chat.id, 'What is your first name?')
        bot.register_next_step_handler(msg, fname)
    elif message.text == 'age':
        msg = bot.send_message(message.chat.id, 'What is your birth year?')
        bot.register_next_step_handler(msg, age)
    else:
        bot.send_message(message.chat.id, 'Please select from choices.')


def fname(message):
    global fn
    fn = message.text
    msg = bot.send_message(message.chat.id, 'What is your last name?')
    bot.register_next_step_handler(msg, lname)

def lname(message):
    ln = message.text
    bot.send_message(message.chat.id, f'You are {fn} {ln}.')

def age(message):
    ag = message.text
    bot.send_message(message.chat.id, f'You are {datetime.today().year -  int(ag)} years old.')

bot.infinity_polling(timeout=120)
