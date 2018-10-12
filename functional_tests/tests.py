from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class newVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_start_a_list_and_retrieve_it_later(self):
        #User Bob visits our to-do list website
        self.browser.get(self.live_server_url)

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
        self.check_for_row_in_list_table('1: Plan next Tuesday\'s session')
        
        #There is a text box enticing Bob to enter another item, solidifying a potential list addiction
        #   Bob enters "Find way to foreshadow upcoming monsters" to remind him what he still needs for next session
        inputbox = self.browser.find_element_by_id('id_new_list_item')
        inputbox.send_keys('Find way to foreshadow upcoming monsters')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #The page updates and shows both items now
        self.check_for_row_in_list_table('1: Plan next Tuesday\'s session')
        self.check_for_row_in_list_table('2: Find way to foreshadow upcoming monsters')

        #Bob realizes that this is a random site and becomes worried that it won't save his list,
        #   then notices the sit generated a unique url for him, and thinks that's a bit weird,
        #   but good enough for this hypothetical straw user. He also notices some text explaining it
        self.fail('Finish the test!')

        #He visits the url, and sees his list fully there

        #Satisfied, he leaves to plan an awesome game night!
