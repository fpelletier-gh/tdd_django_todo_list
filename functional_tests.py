from selenium import webdriver
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
        self.fail("Finish the test!")
        # He is invited to enter a todo item

        # He enter "Groceries" in an input

        # When he hit enter, the page updates and the page show a list
        # "1: Groceries" is displayed

        # There is still an input to enter a new item
        # He enter a new item "Wash the dishes"

        # The page updates and show the updated list with both items

        # The user see look to see that a unique url was generated for him

        # He visit that url and his todo list is still there


if __name__ == "__main__":
    unittest.main()
