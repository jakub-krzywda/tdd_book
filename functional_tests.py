from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Mathew heard about new to-do list site
        # He goes to check its homepage
        self.browser.get('http://localhost:8000')

        # He notices To-Do is in the header, so he assumes it's the
        # right page
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        # He types "Raise taxes"
        inputbox.send_keys('Raise taxes')
        # When he hits enter, the page updates and lists:
        # "1: Raise taxes" as an item in to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Raise taxes' for row in rows))
        # There is still a text box inviting to enter another to-do list item. He enters
        # "Lie about raising taxes". He hits enter and now page lists both items.
        self.fail('Finish the test!')
        # Mateusz wonders if site will remember his to-do list. He notices that site generated
        # unique url for him. There is some explanatory text to that effect

        # He visits that url - his to-do list is still there


if __name__ == "__main__":
    unittest.main()
