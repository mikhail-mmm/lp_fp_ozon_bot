from instruments import product_info_edit, price_info_edit, product_amount_edit

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from settings import CHR_PATH, FILE_PATH

import time
import xpath_ozon

product_carts = []
price_carts = []

def get_page_amount():
    for xpath in xpath_ozon.XPATH_LIST_AMOUNT_PRODUCT:
        try:
            product_amount = driver.find_element(By.XPATH, xpath)
            product_amount = product_amount_edit(product_amount.text)
            if product_amount % 35 != 0:
                page_amount = product_amount // 35 + 1
            else:
                page_amount = product_amount // 35
            break
        except NoSuchElementException:
                page_amount = None
                continue
    return page_amount, product_amount

def product_carts_info():
    for i in range(1, 36):
        for xpath in xpath_ozon.XPATH_LIST_NAME:
            new_xpath = xpath + f'[{i}]' + '/div[2]'
            try:
                product = driver.find_element(By.XPATH, new_xpath)
            except NoSuchElementException:
                continue
            product_carts.append(product.text)
            break
    return product_carts

def price_carts_info():
    for i in range(1, 36):
        for xpath in xpath_ozon.XPATH_LIST_NAME:
            new_xpath = xpath + f'[{i}]' + '/div[3]'
            try:
                price = driver.find_element(By.XPATH, new_xpath)
            except NoSuchElementException:
                continue
            price_carts.append(price.text)
            break
    return price_carts


while True:
    try:
        options = Options()
        driver = webdriver.Chrome(chrome_options=options, executable_path="./chromedriver/chromedriver")

        search_request = '3D принтер'

        driver.get('https://ya.ru')
        time.sleep(1)
        ya_search_box = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div[2]/div/input')
        ya_search_box.send_keys(f'ozon {search_request}', Keys.RETURN)
        window_ya = driver.window_handles[0]
        time.sleep(1)

        for i in range(1, 5):
            unknowed_link = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[2]/div[1]/div[1]/ul/li[{i}]/div/div[1]/a/h2/span')
            if 'OZON' not in unknowed_link.text:
                continue
            else:
                ozon_link = unknowed_link
                break
        break
    except NoSuchElementException:
        continue

ozon_link.click()
time.sleep(1)

# Без этой магии selenium не берет текущий url
driver.switch_to.window(driver.window_handles[0])
driver.switch_to.window(driver.window_handles[1])
time.sleep(1)

current_url = driver.current_url

driver.quit()

options = Options()
driver = webdriver.Chrome(chrome_options=options, executable_path="./chromedriver/chromedriver")

driver.get(current_url)

time.sleep(1)

product_carts = product_carts_info()
price_carts = price_carts_info()

product_names = product_info_edit(product_carts)[0]
rating_list = product_info_edit(product_carts)[1]
reviews_amount = product_info_edit(product_carts)[2]
prices_with_card = price_info_edit(price_carts)[0]
prices_without_card = price_info_edit(price_carts)[1]

page_amount = get_page_amount()[0]
product_amount = get_page_amount()[1]

driver.close()

for j in range(2, (page_amount + 1)):
    product_carts = []
    price_carts = []

    next_url = current_url + f'?page={j}'
    options = Options()
    driver = webdriver.Chrome(chrome_options=options, executable_path=CHR_PATH)
    driver.get(next_url)
    time.sleep(1)

    product_carts = product_carts_info()
    price_carts = price_carts_info()

    product_names.extend(product_info_edit(product_carts)[0])
    rating_list.extend(product_info_edit(product_carts)[1])
    reviews_amount.extend(product_info_edit(product_carts)[2])
    prices_with_card.extend(price_info_edit(price_carts)[0])
    prices_without_card.extend(price_info_edit(price_carts)[1])

    driver.close()

# Временное сохранение данных
with open(FILE_PATH, 'w', encoding='utf-8') as f:
    for i in range(0, product_amount):
        f.write(product_names[i] + '    ' + prices_with_card[i] + '    ' + prices_without_card[i] + '   ' + rating_list[i] + '   ' + reviews_amount[i] + '\n')
