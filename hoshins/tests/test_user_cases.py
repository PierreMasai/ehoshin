from eHoshin.tests.utils import TeamTestCase
from selenium.common.exceptions import NoSuchElementException


class HoshinObjectsTestCase(TeamTestCase):
    fixtures = ['team_with_hoshin.json']

    def test_hoshin_CRUD(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_ta()
        self.wait_for_elt('//*[@id="itemList"]')

        hoshin_name_xpath = '//*[@id="hoshins_list"]/div/div[2]/div/a/button/span[2]'

        # Create a hoshin
        hoshin_name_field = self.selenium.find_element_by_xpath(
            '//*[@id="hoshins_list"]/div/div[2]/div/span/div[2]/input')
        hoshin_name_field.send_keys('test')
        self.selenium.find_element_by_xpath('//*[@id="hoshins_list"]/div/div[2]/div/span/div[2]/a').click()
        hoshin_name = self.wait_for_elt(hoshin_name_xpath)
        self.assertEqual('test', hoshin_name.text)

        # Modify a hoshin
        self.selenium.find_element_by_xpath('//*[@id="hoshins_list"]/div/div[2]/div/div/button').click()
        self.wait_for_elt('//*[@id="hoshins_list"]/div/div[2]/div/div/ul')
        self.selenium.find_element_by_xpath('//*[@id="hoshins_list"]/div/div[2]/div/div/ul/li[2]/a').click()
        hoshin_name_field = self.selenium.find_element_by_xpath(
            '//*[@id="hoshins_list"]/div/div[2]/div/span/div[2]/input')
        hoshin_name_field.send_keys('2')
        self.selenium.find_element_by_xpath('//*[@id="hoshins_list"]/div/div[2]/div/span/div[2]/a').click()
        hoshin_name = self.wait_for_elt(hoshin_name_xpath)
        self.assertEqual('test2', hoshin_name.text)

        # Delete a hoshin
        self.selenium.find_element_by_xpath('//*[@id="hoshins_list"]/div/div[2]/div/div/button').click()
        self.wait_for_elt('//*[@id="hoshins_list"]/div/div[2]/div/div/ul')
        self.selenium.find_element_by_xpath('//*[@id="hoshins_list"]/div/div[2]/div/div/ul/li[1]/a').click()

        self.assertRaises(NoSuchElementException, self.selenium.find_element_by_xpath, hoshin_name_xpath)

    def test_item_CRUD(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_ta()
        self.wait_for_elt('//*[@id="itemList"]')

        item_name_xpath = '//*[@id="itemList"]/div/div[2]/div/div[1]/a/h3/span[3]'

        # Create an item
        fields = [
            '//*[@id="itemList"]/div/div[2]/div/div[3]/input',
            '//*[@id="itemList"]/div/div[2]/div/div[4]/span/input[2]',
            '//*[@id="itemList"]/div/div[2]/div/div[5]/textarea'
        ]

        for field_xpath in fields:
            field = self.selenium.find_element_by_xpath(field_xpath)
            field.send_keys('test')

        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[2]/div/div[7]/div/button').click()
        item_name = self.wait_for_elt(item_name_xpath)
        self.assertEqual('test', item_name.text)

        # Modify an item
        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[2]/div/div[2]/a').click()
        self.wait_for_elt('//*[@id="itemList"]/div/div[2]/div/div[2]/ul')
        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[2]/div/div[2]/ul/li[2]/a').click()
        item_name_field = self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[2]/div/div[3]/input')
        item_name_field.send_keys('2')
        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[2]/div/div[7]/div/button').click()
        item_name = self.wait_for_elt(item_name_xpath)
        self.assertEqual('test2', item_name.text)

        # Delete an item
        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[2]/div/div[2]/a').click()
        self.wait_for_elt('//*[@id="itemList"]/div/div[2]/div/div[2]/ul')
        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[2]/div/div[2]/ul/li[1]/a').click()

        self.assertRaises(NoSuchElementException, self.selenium.find_element_by_xpath, item_name_xpath)

    def test_concrete_action_CRUD(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam/1/1'))
        self.connect_ta()
        self.wait_for_elt('//*[@id="commentList"]')
        self.selenium.find_element_by_xpath('//*[@id="header_item"]/div/div/div/a[2]').click()
        self.wait_for_elt('//*[@id="priorityList"]')

        ca_name_xpath = '//*[@id="priorityList"]/div/div[1]/div/div[1]/a/table/tbody/tr/td[2]'

        # Create a ca
        ca_field = self.selenium.find_element_by_xpath('//*[@id="priorityList"]/div/div/div/div[3]/textarea')
        ca_field.send_keys('test')
        self.selenium.find_element_by_xpath('//*[@id="priorityList"]/div/div/div/div[4]/div/button').click()
        ca_name = self.wait_for_elt(ca_name_xpath)
        self.assertEqual('test', ca_name.text)

        # Modify a ca
        self.selenium.find_element_by_xpath('//*[@id="priorityList"]/div/div[1]/div/div[2]/a').click()
        self.wait_for_elt('//*[@id="priorityList"]/div/div[1]/div/div[2]/ul')
        self.selenium.find_element_by_xpath('//*[@id="priorityList"]/div/div[1]/div/div[2]/ul/li[2]/a').click()
        item_name_field = self.selenium.find_element_by_xpath('//*[@id="priorityList"]/div/div[1]/div/div[3]/textarea')
        item_name_field.send_keys('2')
        self.selenium.find_element_by_xpath('//*[@id="priorityList"]/div/div[1]/div/div[4]/div/button').click()
        ca_name = self.wait_for_elt(ca_name_xpath)
        self.assertEqual('test2', ca_name.text)

        # Delete a ca
        self.selenium.find_element_by_xpath('//*[@id="priorityList"]/div/div[1]/div/div[2]/a').click()
        self.wait_for_elt('//*[@id="priorityList"]/div/div[1]/div/div[2]/ul')
        self.selenium.find_element_by_xpath('//*[@id="priorityList"]/div/div[1]/div/div[2]/ul/li[1]/a').click()

        self.assertRaises(NoSuchElementException, self.selenium.find_element_by_xpath, ca_name_xpath)
