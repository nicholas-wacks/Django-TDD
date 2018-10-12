from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class newVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
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
        self.wait_for_row_in_list_table('1: Plan next Tuesday\'s session')
        
        #There is a text box enticing Bob to enter another item, solidifying a potential list addiction
        #   Bob enters "Find way to foreshadow upcoming monsters" to remind him what he still needs for next session
        inputbox = self.browser.find_element_by_id('id_new_list_item')
        inputbox.send_keys('Find way to foreshadow upcoming monsters')
        inputbox.send_keys(Keys.ENTER)

        #The page updates and shows both items now
        self.wait_for_row_in_list_table('1: Plan next Tuesday\'s session')
        self.wait_for_row_in_list_table('2: Find way to foreshadow upcoming monsters')

        #Satisfied, he leaves to plan an awesome game night!

    def test_multiple_users_can_have_unique_lists(self):
        #Bob makes a new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_list_item')
        inputbox.send_keys('Plan next Tuesday\'s session')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Plan next Tuesday\'s session')

        #Bob realizes that this is a random site and becomes worried that it won't save his list,
        #   then notices the sit generated a unique url for him, and thinks that's a bit weird,
        #   but good enough for this hypothetical straw user. He also notices some text explaining it
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, '/lists/.+')

        #Satisfied for now, bob leaves the site
        self.browser.quit()

        #A new user, Carol, visits the site
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        #Carol sees an empty list, and no sign of Bob's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Plan next Tuesday\'s session', page_text)
        
        #Carol begins making a new list by entering a new item
        #   Carol is less of a huge nerd
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #Carol gets her own unique URL
        carol_list_url = self.browser.current_url
        self.assertRegex(carol_list_url, '/lists/.+')
        self.assertNotEqual(carol_list_url, bob_list_url)

        #Still no trace of Bob's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Plan next Tuesday\'s session', page_text)
        self.assertIn('Buy milk', page_text)

        #Satisfied with her milky decision, she leaves the site, likely without bookmarking her unique URL, 
        #   leaving this list to drift into the ether, untouched until the day the production servers
        #   catch fire and the project is considered lost