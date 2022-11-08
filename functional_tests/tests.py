from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, item_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(item_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Mathew heard about new to-do list site
        # He goes to check its homepage
        self.browser.get(self.live_server_url)

        # He notices To-Do is in the header, so he assumes it's the
        # right page
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        # He types "Raise taxes"
        # When he hits enter, the page updates and lists:
        inputbox.send_keys('Raise taxes')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # "1: Raise taxes" as an item in to-do list
        self.check_for_row_in_list_table('1: Raise taxes')
        # There is still a text box inviting to enter another to-do list item. He enters
        # "Lie about raising taxes". He hits enter and now page lists both items.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('Lie about raising taxes')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Raise taxes')
        self.check_for_row_in_list_table('2: Lie about raising taxes')

        self.fail('Finish the test!')
        # Mateusz wonders if site will remember his to-do list. He notices that site generated
        # unique url for him. There is some explanatory text to that effect

        # He visits that url - his to-do list is still there
