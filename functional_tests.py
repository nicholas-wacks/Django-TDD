from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class newVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_start_a_list_and_retrieve_it_later(self):
        #User Bob visits our to-do list website
        self.browser.get('http://localhost:8080')

        #Bob notices page title and header mention to-do lists, so is 100% in the right place
        #   Poor, naive Bob
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #Bob is invited to make a to-do item right away. First one's free
        inputbox = self.browser.find_element_by_id('id_new_list_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #Bob types "Plan next Tuesday's session" into the text box
        #   Bob is a huge nerd and leads a bi-weekly D&D group. That nerd.
        inputbox.send_keys('Plan next Tuesday\'s session')

        #When Bob hits enter, the page updates and now shows a to-do list with
        #   "#1: Plan next Tuesday's session" as the only item
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '#1: Plan next Tuesday\'s session' for row in rows),
            "New to-do item did not appear in table"
        )

        #There is a text box enticing Bob to enter another item, solidifying a potential list addiction
        #   Bob enters "Find way to foreshadow upcoming monsters" to remind him what he still needs for next session
        self.fail('Finish the test!')

        #The page updates and shows both items now

        #Bob realizes that this is a random site and becomes worried that it won't save his list,
        #   then notices the sit generated a unique url for him, and thinks that's a bit weird,
        #   but good enough for this hypothetical straw user. He also notices some text explaining it

        #He visits the url, and sees his list fully there

        #Satisfied, he leaves to plan an awesome game night!

if __name__ == '__main__':
    unittest.main(warnings='ignore')