import os
from parser_ozon.settings_parser import USER_DATA_PATH
from telegram import ParseMode
from utils_bot import main_keyboard, read_user_file

message_help = """Основные команды бота:
<b>/start</b>: Запуск Бота
<b>/help</b>: Вывод справки
<b>/clear_data</b>: Очистить сохраненные данные
-----------------------------------------------

Также можете воспользоваться специальной клавиатурой внизу экрана.
<b>Поиск продукта на OZON</b>, <b>Показать найденные товары</b>,
<b>Очистить данные по товарам</b>:
"""


def greet_user(update, context):
    print('Бот стартовал!')
    update.message.reply_text(f'''
Привет! Этот телеграмм бот поможет тебе найти товары на озоне и отфильтровать их по цене отзывам и т.д.\n
{message_help}''', reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    print(update.message.chat['id'])


def help_message(update, context):
    update.message.reply_text(message_help, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)


def answer_text(update, context):
    update.message.reply_text('Воспользуйся командами из /help, или выбери нужный пункт на клавиатуре внизу экрана.')


def last_request(update, context):
    try:
        # filter = context.user_data["find_product"]["filters"]
        filter = 'По цене и рейтингу'
        chat_id = str(update.message.chat['id'])
        file_name = f'{USER_DATA_PATH}user_{chat_id}.csv'
        if os.path.isfile(file_name) is False:
            update.message.reply_text('Сбор данных еще не закончен...', reply_markup=main_keyboard())
        else:
            user_data = read_user_file(file_name, filter)
            for el in user_data:
                update.message.reply_text(el, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    except KeyError:
        update.message.reply_text('Вы еще не сделали ни одного запроса', reply_markup=main_keyboard())


def clear_data(update, context):
    update.message.reply_text('Функция пока недоступна.', reply_markup=main_keyboard())
