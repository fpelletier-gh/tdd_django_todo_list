from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("list-table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.2)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_for_one_user(self):
        # The user enter the url for toto online application
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table("1: Groceries")

        # There is still an input to enter a new item
        # He enter a new item "Wash the dishes"
        inputbox = self.browser.find_element_by_id("new-item-input")
        inputbox.send_keys("Wash the dishes")
        inputbox.send_keys(Keys.ENTER)

        # The page updates and show the updated list with both items
        self.wait_for_row_in_list_table("1: Groceries")
        self.wait_for_row_in_list_table("2: Wash the dishes")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element_by_id("new-item-input")
        inputbox.send_keys("Groceries")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Groceries")

        # The user see look to see that a unique url was generated for him
        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, "/lists/.+")

        # He visit that url and his todo list is still there

        # A new user, user2 comes to the site
        ## We use a new browser session to make sure that no information of
        ## the first user is comming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        # User2 visit the home page there is no sign of the first user list
        inputbox = self.browser.find_element_by_id("new-item-input")
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Groceries", page_text)
        self.assertNotIn("Wash the dishes", page_text)

        # User2 start a new list by entering a new item
        inputbox = self.browser.find_element_by_id("new-item-input")
        inputbox.send_keys("Milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Milk")

        # User2 get it's own unique url
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, "/lists/.+")
        self.assertNotEqual(first_user_list_url, second_user_list_url)

        # There is still no trace of the first user list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Groceries", page_text)
        self.assertIn("1: Milk", page_text)

        self.fail("Finish the test!")
