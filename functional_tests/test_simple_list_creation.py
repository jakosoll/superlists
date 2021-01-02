import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    """тест нового посетитееля"""

    def test_can_start_a_list_for_one_user(self):
        """Можно начать список и получить его позже"""
        # Эдит слышала про новое крутое приложение
        # со списком неотложных дел и решает оценить
        # его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка сайта говорят
        # о списках дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ей стразу же предлагается ввести элемент списка
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # Она набирает в текстовом поле "Купить павлиньи перья"
        # в качестве элемента списка
        input_box.send_keys('Купить павлиньи перья')

        # Она нажимает "enter" и страница обновляется.
        # Теперь страница содержит "1. Купить павлиньи перья" в качестве элемента списка
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Тестовое поле по прежнему приглашает ее добавить еще один элемент
        input_box = self.browser.find_element_by_id('id_new_item')
        # Она вводит "Сделать мушку из павлиньих перьев"
        input_box.send_keys('Сделать мушку из павлиньих перьев')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # Страница снова обновляется и теперь показывает оба элемента списка
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # Удовлетворенная она снова ложится спать.

        # Эдит интересно, запомнит ли сайт ее списко. Далее она видит,
        # что сайт сгенерировал для нее уникальный URL-адрес.
        # Об этом выводится небольшой текст с объяснениями.

        # Она посещает этот URL-адрес и ее список по-прежнему там.

    def test_multiple_users_can_start_list_at_different_urls(self):
        """Тест: многочисленные пользователи могут начать списки по разным url"""
        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Купить павлиньи перья')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Она замечает, что ее список имеет уникальный URL-адрес
        edit_list_url = self.browser.current_url
        self.assertRegex(edit_list_url, '/lists/.+')

        # Теперь приходит новый пользователь, Френсис.

        ## Мы используем новый сеанс браузера, чтобы инфа Эдит не повлияла
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Френсис посещает домашнюю страницу. Нет никаких признаков Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Френсис начинает новый список
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Купить молоко')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Френсис получает уникальный адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edit_list_url)

        # Френсис еще раз убеждается, что нет следов списка Эдит
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

        # Удовлетворенные они оба ложатся спать
