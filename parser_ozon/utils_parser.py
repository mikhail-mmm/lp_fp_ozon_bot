def price_edit(price):
    price_new = price.replace('\u2009', '')
    price_new = price_new.replace(' ', '')
    price_new = price_new[:-1]
    return price_new

def product_amount_edit(product_amount):
    product_amount_new = ''
    for simbol in product_amount:
        if simbol in '1234567890':
            product_amount_new += simbol
    return int(product_amount_new)

def product_filter(product_carts):
    product_names = []
    rating_list = []
    reviews_amount = []

    for product_cart in product_carts:
        characteristics = product_cart.split('\n')
        if 'бонус' in characteristics[0]:
            product_name = characteristics[1]
        else:
            product_name = characteristics[0]
        for characteristic in characteristics:
            if characteristic[0] == ' ':
                if 'бонус' not in characteristic:
                    presence_reviews = True
                    review_and_rating = characteristic.split()
                    rating_list.append(review_and_rating[0])
                    reviews_amount.append(review_and_rating[1])
            else:
                presence_reviews = False
        if presence_reviews == False:
            reviews_amount.append('0')
            rating_list.append('0')

        product_names.append(product_name)
    return product_names, rating_list, reviews_amount

def price_filter(price_carts):
    
    prices_with_card = []
    prices_without_card = []

    for price_cart in price_carts:
        prices = price_cart.split('\n')
        if prices[1] == 'c Ozon Картой':
            prices_with_card.append(price_edit(prices[0]))
            prices_without_card.append(price_edit(prices[2]))
        else:
            prices_without_card.append(price_edit(prices[0]))
            prices_with_card.append('None')
    
    return prices_with_card, prices_without_card
        