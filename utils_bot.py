import pandas as pd
from telegram import ReplyKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Поиск продукта на OZON'],
        ['Показать последний результат', 'Очистить данные по товарам'],
        ['Справка']
    ])


def read_user_file(file_name, filter):
    data = pd.read_csv(open(file_name, 'r'), sep=',')
    result = []

    if filter == 'По цене':
        new_data = data.sort_values('price_without_card', ascending=False)
        new_data = new_data.drop_duplicates('price_without_card')
    elif filter == 'По цене и рейтингу':
        new_data = data.sort_values(by=['rating', 'price_without_card'], ascending=[False, True])
        new_data = new_data.drop_duplicates('price_without_card')
        new_data = new_data[new_data['price_without_card'] > 5000]
        new_data = new_data[new_data['amount_review'] > 5]
    else:
        new_data = data.sort_values(by=['rating', 'amount_review'], ascending=[False, False])
        new_data = new_data.drop_duplicates('price_without_card')
        new_data = new_data[new_data['amount_review'] > 5]

    for i in range(5):
        product_name = str(new_data['product_name'].loc[new_data.index[i]])
        url = str(new_data['url'].loc[new_data.index[i]])
        rating = str(new_data['rating'].loc[new_data.index[i]])
        amount_review = str(new_data['amount_review'].loc[new_data.index[i]])
        price_with_card = str(new_data['price_with_card'].loc[new_data.index[i]])
        price_without_card = str(new_data['price_without_card'].loc[new_data.index[i]])

        answer = f'''
<b>{product_name}</b>
{url}
<i>Рейтинг:</i> <b>{rating}</b>
<i>Кол-во отзывов:</i> <b>{amount_review}</b>
{price_with_card} руб.
<b>{price_without_card} руб.</b>'''

        result.append(answer)
    return result
