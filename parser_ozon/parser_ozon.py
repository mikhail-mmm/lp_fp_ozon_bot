from parser_ozon.utils_parser import product_filter, price_filter, product_amount_edit

from parser_ozon import xpath_ozon
from parser_ozon import xpath_ya
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from parser_ozon.settings_parser import CHR_PATH, USER_DATA_PATH

import csv
import time


class Parser:

    def __init__(self, chat_id, user_request):
        self.user_request = user_request
        self.chat_id = chat_id
        self.product_carts = []
        self.price_carts = []
        self.product_url = []
        self.parsing_result = []

    def parser_ozon(self):
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
                    self.product_carts.append(product.text)
                    break
            return self.product_carts

        def price_carts_info():
            for i in range(1, 36):
                for xpath in xpath_ozon.XPATH_LIST_NAME:
                    new_xpath = xpath + f'[{i}]' + '/div[3]'
                    try:
                        price = driver.find_element(By.XPATH, new_xpath)
                    except NoSuchElementException:
                        continue
                    self.price_carts.append(price.text)
                    break
            return self.price_carts

        def find_url():
            for i in range(1, 36):
                for xpath in xpath_ozon.XPATH_LIST_NAME:
                    new_xpath = xpath + f'[{i}]' + '/div[2]/div/a'
                    try:
                        url = driver.find_element(By.XPATH, new_xpath)
                        url = url.get_attribute('href')
                    except NoSuchElementException:
                        continue
                    self.product_url.append(str(url))
                    break
            return self.product_url

        while True:
            try:
                options = Options()
                driver = webdriver.Chrome(chrome_options=options, executable_path=CHR_PATH)

                search_request = self.user_request

                driver.get('https://ya.ru')
                time.sleep(1)
                ya_search_box = driver.find_element(By.XPATH, xpath_ya.FIND_BOX_YA)
                ya_search_box.send_keys(f'ozon {search_request}', Keys.RETURN)
                time.sleep(1)

                for i in range(1, 5):
                    unknowed_xpath = xpath_ya.OZON_LINK + f'li[{i}]/div/div[1]/a/h2/span'
                    unknowed_link = driver.find_element(By.XPATH, unknowed_xpath)
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

        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)

        current_url = driver.current_url

        driver.quit()

        options = Options()
        driver = webdriver.Chrome(chrome_options=options, executable_path=CHR_PATH)

        driver.get(current_url)

        time.sleep(1)

        self.product_carts = product_carts_info()
        self.price_carts = price_carts_info()
        self.product_url = find_url()

        product_url = self.product_url
        product_names = product_filter(self.product_carts)[0]
        rating_list = product_filter(self.product_carts)[1]
        reviews_amount = product_filter(self.product_carts)[2]
        prices_with_card = price_filter(self.price_carts)[0]
        prices_without_card = price_filter(self.price_carts)[1]

        page_amount = get_page_amount()[0]
        product_amount = get_page_amount()[1]

        driver.close()

        for i in range(2, (page_amount + 1)):
            self.product_carts = []
            self.price_carts = []

            next_url = current_url + f'?page={i}&tf_state='
            options = Options()
            driver = webdriver.Chrome(chrome_options=options, executable_path=CHR_PATH)
            driver.get(next_url)
            time.sleep(1)

            self.product_carts = product_carts_info()
            self.price_carts = price_carts_info()
            self.product_url = find_url()

            product_url.extend(self.product_url)
            product_names.extend(product_filter(self.product_carts)[0])
            rating_list.extend(product_filter(self.product_carts)[1])
            reviews_amount.extend(product_filter(self.product_carts)[2])
            prices_with_card.extend(price_filter(self.price_carts)[0])
            prices_without_card.extend(price_filter(self.price_carts)[1])

            driver.close()

        for i in range(0, (product_amount - 1)):
            triger = 0
            find_word = 0
            product_data = {}
            if 'для' in product_names[i].lower():
                words = product_names[i].split()
                for word in words:
                    if word.lower() == '3d':
                        find_word += 1
                    elif word.lower() == 'для':
                        triger += 1
                    else:
                        continue
                    if find_word > 0 and triger == 0:
                        product_data['product_name'] = product_names[i]
                        product_data['url'] = product_url[i]
                        product_data['rating'] = rating_list[i]
                        product_data['amount_review'] = reviews_amount[i]
                        product_data['price_with_card'] = prices_with_card[i]
                        product_data['price_without_card'] = prices_without_card[i]
                        self.parsing_result.append(product_data)
            else:
                product_data['product_name'] = product_names[i]
                product_data['url'] = product_url[i]
                product_data['rating'] = rating_list[i]
                product_data['amount_review'] = reviews_amount[i]
                product_data['price_with_card'] = prices_with_card[i]
                product_data['price_without_card'] = prices_without_card[i]
                self.parsing_result.append(product_data)
        return self.parsing_result

    def seve_data(self):
        csv_colums = ['product_name', 'url', 'rating', 'amount_review', 'price_with_card', 'price_without_card']
        save_path = f'{USER_DATA_PATH}user_{self.chat_id}.csv'
        with open(save_path, 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_colums)
            writer.writeheader()
            for el in self.parsing_result:
                writer.writerow(el)
