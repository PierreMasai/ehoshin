from eHoshin.tests.utils import multi, TeamTestCase
from selenium.common.exceptions import NoSuchElementException
import requests
import time


class EmptyTeamTestCase(TeamTestCase):
    fixtures = ['default_team.json']

    @multi()
    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEquals(self.selenium.title, 'eHoshin')

    @multi()
    def test_creation_team_then_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        field = self.selenium.find_element_by_xpath('/html/body/section/div/form/div/input')
        field.send_keys("test")

        self.click_and_wait('/html/body/section/div/form/div/span/button')

        self.connect_ta()
        self.assertIn("test", self.selenium.current_url)

    def test_creation_team_then_signup(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        field = self.selenium.find_element_by_xpath('/html/body/section/div/form/div/input')
        field.send_keys("test")

        self.click_and_wait('/html/body/section/div/form/div/span/button')
        self.assertIn("Login", self.selenium.title)

        self.click_and_wait('/html/body/section/div/div/div/div/form/p/a')
        self.signup_user('tu', 'tu', 'Tu', 'tu')
        self.assertIn("test", self.selenium.current_url)
        self.assertNotIn("join", self.selenium.current_url)

    @multi()
    def test_team_access(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.assertIn("login", self.selenium.current_url)

    @multi()
    def test_team_list_click(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.click_and_wait('//*[@id="teamList"]/a')
        self.assertIn("login", self.selenium.current_url)

    @multi()
    def test_noHoshin_moderator(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_ta()
        self.assertIn("publicTeam", self.selenium.current_url)

        admin_text = self.wait_for_elt('//*[@id="noHoshinTextMo"]')
        normal_text = self.selenium.find_element_by_id('noHoshinTextNo')

        self.assertTrue(admin_text.is_displayed())
        self.assertFalse(normal_text.is_displayed())

    @multi()
    def test_noHoshin_normal_user(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_admin()
        self.assertIn("publicTeam", self.selenium.current_url)
        normal_text = self.wait_for_elt('//*[@id="noHoshinTextNo"]')
        admin_text = self.selenium.find_element_by_id('noHoshinTextMo')
        hoshin_list = self.selenium.find_element_by_xpath('/html/body/section/div[1]')

        self.assertFalse(admin_text.is_displayed())
        self.assertTrue(normal_text.is_displayed())
        self.assertFalse(hoshin_list.is_displayed())

    @multi()
    def test_select_team(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login'))
        self.connect_ta()

        self.assertEquals(self.selenium.title, 'eHoshin')
        self.selenium.find_element_by_xpath('//*[@id="teamDropdown"]/a').click()
        self.wait_for_elt('//*[@id="teamDropdown"]/ul')
        self.click_and_wait('//*[@id="teamDropdown"]/ul/li[2]/a')

    @multi()
    def test_hoshin_direct_access(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam/1'))
        self.assertIn("Login", self.selenium.title)


class FullTeamTestCase(TeamTestCase):
    fixtures = ['team_with_hoshin.json']

    def get_indicators(self):
        indicator = '//*[@id="hoshinIndicators"]/table/tbody/tr[%d]/td[2]'
        time.sleep(1)
        indicators = []
        for i in [1, 3, 5, 6]:
            indicators.append(self.selenium.find_element_by_xpath(indicator % i))

        return [int(indic.text) for indic in indicators]

    @multi()
    def test_Hoshin_moderator(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_ta()
        self.assertIn("publicTeam", self.selenium.current_url)

        item_list = self.wait_for_elt('//*[@id="itemList"]')
        admin_text = self.selenium.find_element_by_id('noHoshinTextMo')
        normal_text = self.selenium.find_element_by_id('noHoshinTextNo')

        self.assertTrue(item_list.is_displayed())
        self.assertFalse(admin_text.is_displayed())
        self.assertFalse(normal_text.is_displayed())

        self.assertIn('Create a new theme', self.selenium.page_source)
        self.assertTrue(self.selenium.find_element_by_xpath('//*[@id="hoshins_list"]/div/div[2]/div/span/div[2]/input'))

    @multi()
    def test_Hoshin_normal_user(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_admin()
        self.assertIn("publicTeam", self.selenium.current_url)

        item_list = self.wait_for_elt('//*[@id="itemList"]')
        admin_text = self.selenium.find_element_by_id('noHoshinTextMo')
        normal_text = self.selenium.find_element_by_id('noHoshinTextNo')

        self.assertTrue(item_list.is_displayed())
        self.assertFalse(admin_text.is_displayed())
        self.assertFalse(normal_text.is_displayed())

        self.assertNotIn('Create a new theme', self.selenium.page_source)

    def test_leader_become_moderator_at_team_signup(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signup?next=/join/publicTeam'))
        self.signup_user('tu', 'tu', 'Tu', 'tu')

        self.wait_for_elt('//*[@id="itemList"]/div/div[2]/div/div[1]/h3')

    def test_get_comment_list(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login?next=/join/publicTeam'))
        self.connect_ta()
        self.wait_for_elt('//*[@id="itemList"]')

        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div/div/div/a').click()
        self.wait_for_elt('//*[@id="header_item"]/div/div/table')

    def test_get_comment_once(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login?next=/join/publicTeam'))
        self.connect_ta()
        self.wait_for_elt('//*[@id="itemList"]')

        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div/div/div/a').click()
        self.wait_for_elt('//*[@id="header_item"]/div/div/table')

        # Write a comment
        comment_box = self.wait_for_elt('//*[@id="commentList"]/div/div/div/div[4]/textarea')
        comment_box.send_keys('write comment...')
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div/div/div[5]/div/button').click()
        self.wait_for_elt('//*[@id="commentList"]/div/div[1]/div/div[1]/p')

        _, nb_comments, nb_commentators, _ = self.get_indicators()
        self.assertEqual(1, nb_comments)
        self.assertEqual(1, nb_commentators)

        # Delete comment
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div[1]/div/div[2]/a').click()
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div[1]/div/div[2]/ul/li[1]/a').click()

        _, nb_comments, nb_commentators, _ = self.get_indicators()
        self.assertEqual(0, nb_comments)
        self.assertEqual(0, nb_commentators)

    def test_get_comment_twice(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login?next=/join/publicTeam'))
        self.connect_ta()
        self.wait_for_elt('//*[@id="itemList"]')

        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div/div/div/a').click()
        self.wait_for_elt('//*[@id="header_item"]/div/div/table')

        # Write a comment
        comment_box = self.wait_for_elt('//*[@id="commentList"]/div/div/div/div[4]/textarea')
        comment_box.send_keys('write comment...')
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div/div/div[5]/div/button').click()
        self.wait_for_elt('//*[@id="commentList"]/div/div[1]/div/div[1]/p')

        # Write a second comment
        comment_box = self.wait_for_elt('//*[@id="commentList"]/div/div[2]/div/div[4]/textarea')
        comment_box.send_keys('second comment...')
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div[2]/div/div[5]/div/button').click()
        self.wait_for_elt('//*[@id="commentList"]/div/div[1]/div/div[1]/p')

        _, nb_comments, nb_commentators, nb_chatty_commentators = self.get_indicators()
        self.assertEqual(0, nb_commentators)
        self.assertEqual(1, nb_chatty_commentators)
        self.assertEqual(2, nb_comments)

        # Delete comment
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div[1]/div/div[2]/a').click()
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div[1]/div/div[2]/ul/li[1]/a').click()

        _, nb_comments, nb_commentators, nb_chatty_commentators = self.get_indicators()
        self.assertEqual(1, nb_commentators)
        self.assertEqual(0, nb_chatty_commentators)
        self.assertEqual(1, nb_comments)

        # Delete comment
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div[1]/div/div[2]/a').click()
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div[1]/div/div[2]/ul/li[1]/a').click()

        _, nb_comments, nb_commentators, nb_chatty_commentators = self.get_indicators()
        self.assertEqual(0, nb_commentators)
        self.assertEqual(0, nb_chatty_commentators)
        self.assertEqual(0, nb_comments)

    def test_delete_item_commented(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login?next=/join/publicTeam'))
        self.connect_ta()
        self.wait_for_elt('//*[@id="itemList"]')

        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div/div/div/a').click()
        self.wait_for_elt('//*[@id="header_item"]/div/div/table')

        # Write a comment
        comment_box = self.wait_for_elt('//*[@id="commentList"]/div/div/div/div[4]/textarea')
        comment_box.send_keys('write comment...')
        self.selenium.find_element_by_xpath('//*[@id="commentList"]/div/div/div/div[5]/div/button').click()
        self.wait_for_elt('//*[@id="commentList"]/div/div[1]/div/div[1]/p')

        nb_theme, nb_comments, nb_commentators, _ = self.get_indicators()
        self.assertEqual(1, nb_theme)
        self.assertEqual(1, nb_commentators)
        self.assertEqual(1, nb_comments)

        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.wait_for_elt('//*[@id="itemList"]')
        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[1]/div/div[2]/a').click()
        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[1]/div/div[2]/ul/li[1]/a').click()

        nb_theme, nb_comments, nb_commentators, _ = self.get_indicators()
        self.assertEqual(0, nb_theme)
        self.assertEqual(0, nb_commentators)
        self.assertEqual(0, nb_comments)

    def test_no_concrete_action(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login?next=/join/publicTeam'))
        self.connect_ta()
        self.wait_for_elt('//*[@id="itemList"]')

        # Go to the comment list when no concrete action
        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div/div/div/a').click()
        self.wait_for_elt('//*[@id="commentList"]')

        self.selenium.find_element_by_xpath('//*[@id="header_item"]/div/div/div/a[2]').click()
        self.wait_for_elt('//*[@id="priorityList"]')

        self.selenium.find_element_by_xpath('//*[@id="header_item"]/div/div/div/a[3]').click()
        self.wait_for_elt('//*[@id="commentList"]')


class ExcelsTestCase(TeamTestCase):
    fixtures = ['team_with_hoshin.json']

    def assertExcelFile(self, url):
        cookies = {}
        for s_cookie in self.selenium.get_cookies():
            cookies[s_cookie["name"]] = s_cookie["value"]

        # request the excel using the cookies:
        url = '%s%s' % (self.live_server_url, url)
        response = requests.get(url, cookies=cookies)
        self.assertEqual(response.headers["content-type"], "application/excel")

    def test_hoshin_abstract(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_ta()
        self.assertExcelFile('/publicTeam/api/hoshins/1?type=application/excel')

    def test_items_leader_abstract(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_ta()
        leader_button_xpath = '/html/body/section/div[1]/div[1]/a'

        self.assertRaises(NoSuchElementException, self.selenium.find_element_by_xpath, leader_button_xpath)

        # Become leader
        self.wait_for_elt('//*[@id="itemList"]')
        # Create an item
        fields = [
            '//*[@id="itemList"]/div/div[2]/div/div[3]/input',
            '//*[@id="itemList"]/div/div[2]/div/div[4]/span/input[2]',
            '//*[@id="itemList"]/div/div[2]/div/div[5]/textarea'
        ]

        for field_xpath in fields:
            field = self.selenium.find_element_by_xpath(field_xpath)
            field.send_keys('T A')

        self.selenium.find_element_by_xpath('//*[@id="itemList"]/div/div[2]/div/div[7]/div/button').click()

        # The button must exists now
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.wait_for_elt(leader_button_xpath)

        # request it
        self.assertExcelFile('/publicTeam/api/leader_synthesis/1')

    def test_items_stats(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_ta()
        self.assertExcelFile('/publicTeam/api/leader_synthesis/1?items=all')
        self.assertExcelFile('/publicTeam/api/hoshin_synthesis/1')


class LeadersTestCase(TeamTestCase):
    fixtures = ['team_with_hoshin.json']

    def test_see_dashboard(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_ta()

        self.selenium.find_element_by_xpath('//*[@id="teamDropdown"]/a').click()
        self.wait_for_elt('//*[@id="teamDropdown"]/ul')
        self.click_and_wait('//*[@id="teamDropdown"]/ul/li[3]/a')

    def test_user_gestion(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam'))
        self.connect_ta()
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam/settings/users'))
        self.wait_for_elt('//*[@id="userList"]/tbody/tr[3]')

        not_moderator_path = '#userList > tbody > tr:nth-child(3) > td:nth-child(2) > div.off'
        self.assertTrue(self.selenium.find_element_by_css_selector(not_moderator_path).is_displayed())

        # Set the user moderator
        self.selenium.find_element_by_xpath('//*[@id="userList"]/tbody/tr[3]/td[2]/div/div/label[2]').click()
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam/settings/users'))
        self.wait_for_elt('//*[@id="userList"]/tbody/tr[3]')
        self.assertRaises(NoSuchElementException, self.selenium.find_element_by_css_selector, not_moderator_path)

        # Remove the user from the team
        self.selenium.find_element_by_xpath('//*[@id="userList"]/tbody/tr[3]/td[3]/a').click()
        self.selenium.get('%s%s' % (self.live_server_url, '/publicTeam/settings/users'))
        self.wait_for_elt('//*[@id="userList"]/tbody/tr[2]')
        self.assertRaises(NoSuchElementException,
                          self.selenium.find_element_by_xpath, '//*[@id="userList"]/tbody/tr[3]')

        # Re add the user to the team
        input_field = self.selenium.find_element_by_xpath('//*[@id="add-user"]/form/div/span[1]/input[2]')
        input_field.send_keys('admin')
        self.selenium.find_element_by_xpath('//*[@id="add-user"]/form/div/span[2]/button').click()
        self.wait_for_elt('//*[@id="userList"]/tbody/tr[3]')
