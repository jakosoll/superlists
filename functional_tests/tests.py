import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

WAIT_TIME = 5


class NewUserTest(LiveServerTestCase):
    """
    Тестируем нового пользователя
    """
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """Ожидать строки в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (WebDriverException, AssertionError) as e:
                if time.time() - start_time > WAIT_TIME:
                    raise e
                time.sleep(0.5)

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

    def test_layout_and_styling(self):
        """тест макета и стилевого оформления"""
        # Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Она замечает, что поле ввода аккуратно отцентрировано
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
        # Она начинает новый список и видит, что поле там тоже аккуратно отценровано
        input_box.send_keys('test')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: test')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
