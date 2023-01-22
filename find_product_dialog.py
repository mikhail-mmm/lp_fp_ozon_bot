import time

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from parser_ozon.parser_ozon import Parser_ozon
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
    context.user_data["find_product"] = {"request": user_request}
    update.message.reply_text(
        """Выполняется сбор информации. Ожидайте...
Может занять несколько минут"""
    )
    print("Parsing process...")
    parser = Parser_ozon(user_request)
    parser.parser()
    print('Parsing completed')
    update.message.reply_text(parser.result_parsing['product_name'][1])
    reply_keyboard = [
        ['По цене', 'По цене и рейтингу'],
        ['По рейтингу и кол-ву отзывов']
    ]
    update.message.reply_text(
        'Сбор данных завершен! Выберите фильтр',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "filters"

def find_product_filters(update, context):
    context.user_data["find_product"]["filters"] = update.message.text
    update.message.reply_text(
        "Применяем фильтр..."
    )
    print('Filtering')
    time.sleep(5)
    update.message.reply_text(
        format_output()
    )
    reply_keyboard = [["Далее"]]
    update.message.reply_text(
        """Посмотрите полученные данные.
Для продолжения нажмите Далее""",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "choise"

def find_product_choise(update, context):
    update.message.reply_text(
        """Выберите товары которые хотите добавить в избранное
Формат ввода: Номер|Пробел|Номер
Пример: 1 3 4 9""",
        reply_markup=ReplyKeyboardRemove()
    )
    return "alarm"

def find_product_alarm(update, context):
    context.user_data["find_product"]["favorite_product"] = update.message.text
    update.message.reply_text("Выполнено")
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
{user_data["find_product"]["filters"]},
{user_data["find_product"]["favorite_product"]}"""
    return text_message