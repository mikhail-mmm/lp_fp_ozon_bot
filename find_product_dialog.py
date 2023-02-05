import time

from start_parsing import start_parser
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from utils_bot import main_keyboard


def find_product_start(update, context):
    update.message.reply_text(
        """Введите наименование искомого товара
В запросе можно уточнить категорию,
например, 'Xiaomi' -> 'Смартфон Xiaomi')""",
        reply_markup=ReplyKeyboardRemove()
    )
    return "request"


def find_product_request(update, context):
    user_request = update.message.text
    chat_id = str(update.message.chat['id'])
    context.user_data["find_product"] = {"request": user_request}
    start_parser.send(chat_id, user_request)
    print("Parsing process...")
    reply_keyboard = [
        ['По цене', 'По цене и рейтингу'],
        ['По рейтингу и кол-ву отзывов']
    ]
    update.message.reply_text(
        'Пока идет сбор данных. Выберите фильтр',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "filters"


def find_product_filters(update, context):
    context.user_data["find_product"]["filters"] = update.message.text
    update.message.reply_text(
        "Фильтр выбран!"
    )
    time.sleep(2)
    reply_keyboard = [["Далее"]]
    update.message.reply_text(
        """Сбор данных может занять несколько минут.
Для продолжения нажмите Далее""",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "close"


def find_product_close(update, context):
    update.message.reply_text(
        """Для просмотра результата Вашего запроса
нажмите клавишу 'Показать последний результат'.""",
        reply_markup=main_keyboard()
    )
    user_data = format_data(context.user_data)
    update.message.reply_text(
        user_data,
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END


def find_product_dontknow(update, context):
    update.message.reply_text('Неправильный формат ввода')


def format_output(data='Данные'):
    return data


def format_data(user_data):
    text_message = f"""
{user_data["find_product"]["request"]},
{user_data["find_product"]["filters"]}.
"""
    return text_message
