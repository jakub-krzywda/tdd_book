from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time
from django.test import LiveServerTestCase

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
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
        self.wait_for_row_in_list_table('1: Raise taxes')
        # There is still a text box inviting to enter another to-do list item. He enters
        # "Lie about raising taxes". He hits enter and now page lists both items.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('Lie about raising taxes')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Raise taxes')
        self.wait_for_row_in_list_table('2: Lie about raising taxes')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Mateusz starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Raise taxes')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Raise taxes')
        pinoccios_list_url = self.browser.current_url
        self.assertRegex(pinoccios_list_url, '/lists/.+')
        # Mateusz wonders if site will remember his to-do list. He notices that site generated
        # unique url for him. There is some explanatory text to that effect

        # He visits that url - his to-do list is still there

        # Now a new user, Jaroslaw, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Mateusz's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Jaroslaw visits the home page. There is no sign of Mateusz's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Raise taxes', page_text)
        self.assertNotIn('Lie about raising taxes', page_text)

        # Jaroslaw starts a new list by entering a new item. He is less interesting than Mateusz
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Fuck around')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Fuck around')

        # Jaroslaw gets his own unique URL
        jaroslaw_list_url = self.browser.current_url
        self.assertRegex(jaroslaw_list_url, '/lists/.+')
        self.assertNotEqual(pinoccios_list_url, jaroslaw_list_url)

        # Again there is no sign of Mateusz's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Raise taxes', page_text)
        self.assertIn('Fuck around', page_text)

        # Satisfied, they both go back to sleep