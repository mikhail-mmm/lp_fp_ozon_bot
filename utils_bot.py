from telegram import ReplyKeyboardMarkup

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Поиск продукта на OZON'],
        ['Показать последний результат', 'Очистить данные по товарам'],
        ['Справка']
    ])
