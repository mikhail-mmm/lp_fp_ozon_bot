from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Поиск продукта на OZON'],
        ['Показать найденные товары', "Очистить данные по товарам"],
        ['Справка']
    ])
