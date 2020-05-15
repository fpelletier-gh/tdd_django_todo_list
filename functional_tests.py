from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # The user enter the url for toto online application
        self.browser.get("http://localhost:8000")

        # He look at the title and header and it mention to-do
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1")
        self.assertIn("To-Do", header_text.text)
        # He is invited to enter a todo item
        inputbox = self.browser.find_element_by_id("new-item-input")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # He enter "Groceries" in an input
        inputbox.send_keys("Groceries")

        # When he hit enter, the page updates and the page show a list
        # "1: Groceries" is displayed
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id("list-table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertTrue(
            any(row.text == "1: Groceries" for row in rows),
            "New todo item did not appear in table",
        )

        # There is still an input to enter a new item
        # He enter a new item "Wash the dishes"
        self.fail("Finish the test!")

        # The page updates and show the updated list with both items

        # The user see look to see that a unique url was generated for him

        # He visit that url and his todo list is still there


if __name__ == "__main__":
    unittest.main()
