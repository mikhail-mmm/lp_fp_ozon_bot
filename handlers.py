from telegram import ParseMode
from utils_bot import main_keyboard

message_help = """Основные команды бота:
<b>/start</b>: Запуск Бота
<b>/help</b>: Вывод справки
<b>/clear_data</b>: Очистить сохраненные данные
-----------------------------------------------
<b>Поиск продукта на OZON</b>, <b>Показать найденные товары</b>,
<b>Очистить данные по товарам</b>:
Воспользуйтесь клавиатурой
"""

def greet_user(update, context):
    print('Бот стартовал!')
    update.message.reply_text(f'''
    Привет! Этот телеграмм бот поможет тебе найти товары на озоне и отфильтровать их по цене отзывам и т.д.
    {message_help}
Также можете воспользоваться специальной клавиатурой внизу экрана.
    ''', reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    print(update.message.chat['id'])

def help_message(update, context):
    update.message.reply_text(message_help, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)

def answer_text(update, context):
    update.message.reply_text('Воспользуйся командами из /help, или выбери нужный пункт на клавиатуре внизу экрана.')
