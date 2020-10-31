import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewUserTest(unittest.TestCase):
    """
    Тестируем нового пользователя
    """
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Можно начать список и получить его позже"""
        # Эдит слышала про новое крутое приложение
        # со списком неотложных дел и решает оценить
        # его домашнюю страницу
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1. Купить павлиньи перья' for row in rows)
        )
        # Тестовое поле по прежнему приглашает ее добавить еще один элемент
        # Она вводит "Сделать мушку из павлиньих перьев"
        self.fail('Закончить тест!')
        # Страница снова обновляется и теперь показывает оба элемента списка

        # Эдит интересно, запомнит ли сайт ее списко. Далее она видит,
        # что сайт сгенерировал для нее уникальный URL-адрес.
        # Об этом выводится небольшой текст с объяснениями.

        # Она посещает этот URL-адрес и ее список по-прежнему там.
        # Удовлетворенная она снова ложится спать.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
