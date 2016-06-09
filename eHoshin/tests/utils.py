import functools
from django.test import LiveServerTestCase
from selenium import webdriver
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import \
    staleness_of
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException



def multi(pool_name='drivers', target_attr='selenium'):
    """
    Run tests with `target_attr` set to each instance in the `WebDriverPool`
    named `pool_name`.

    For example, in you setUpClass method of your LiveServerTestCase:

        # Importing the necessaries:
        from selenium import webdriver

        ### In your TestCase:

        # Be sure to add a place holder attribute for the driver variable
        selenium = None

        # Set up drivers
        @classmethod
        def setUpClass(cls):
            cls.drivers = WebDriverList(
                webdriver.Chrome(),
                webdriver.Firefox(),
                webdriver.Opera(),
                webdriver.PhantomJS,
            )
            super(MySeleniumTests, cls).setUpClass()

        # Tear down drivers
        @classmethod
        def tearDownClass(cls):
            cls.drivers.quit()
            super(MySeleniumTests, cls).tearDownClass()

        # Use drivers
        @test_drivers()
        def test_login(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/'))
            self.assertEquals(self.selenium.title, 'Awesome Site')

    This will run `test_login` with each of the specified drivers as the
    attribute named "selenium"

    """
    def wrapped(test_func):
        @functools.wraps(test_func)
        def decorated(test_case, *args, **kwargs):
            test_class = test_case.__class__
            web_driver_pool = getattr(test_class, pool_name)
            for web_driver in web_driver_pool:
                setattr(test_case, target_attr, web_driver)
                test_func(test_case, *args, **kwargs)
        return decorated
    return wrapped


class WebDriverList(list):
    """
    A sequence that has a `.quit` method that will run on each item in the list.
    Used to easily "quit" a list of WebDrivers.
    """

    def __init__(self, *drivers):
        super(WebDriverList, self).__init__(drivers)

    def quit(self):
        for driver in self:
            driver.quit()


class MultiBrowserTestCase(LiveServerTestCase):
    selenium = None

    # Set up drivers
    @classmethod
    def setUpClass(cls):
        cls.drivers = WebDriverList(
            webdriver.Firefox(),
        #    webdriver.Chrome(),
        )
        MultiBrowserTestCase.selenium = cls.drivers[0]
        super(MultiBrowserTestCase, cls).setUpClass()

    # Tear down drivers
    @classmethod
    def tearDownClass(cls):
        cls.drivers.quit()
        super(MultiBrowserTestCase, cls).tearDownClass()

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.selenium.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.selenium, timeout).until(
            staleness_of(old_page)
        )

    def wait_for_elt(self, xpath_elt, timeout=10):
        try:
            WebDriverWait(self.selenium, timeout).until(
                    lambda d: d.find_element_by_xpath(xpath_elt).is_displayed())
        except TimeoutException:
            raise AssertionError('Element defined by the xpath "' + xpath_elt + '" not found.')
        except StaleElementReferenceException:
            self.selenium.implicitly_wait(1)
            return self.wait_for_elt(xpath_elt, timeout-1)

        return self.selenium.find_element_by_xpath(xpath_elt)

    def click_and_wait(self, xpath):
        button = self.selenium.find_element_by_xpath(xpath)

        with self.wait_for_page_load(timeout=1):
            button.click()


class TeamTestCase(MultiBrowserTestCase):
    def connect_admin(self):
        self.connect_user('admin', 'admin')

    def connect_ta(self):
        self.connect_user('ta', 'ta')

    def connect_user(self, name, pwd):
        self.assertIn("Login", self.selenium.title)
        username = self.selenium.find_element_by_xpath('/html/body/section/div/div/div/div/form/input[2]')
        username.send_keys(name)

        password = self.selenium.find_element_by_xpath('/html/body/section/div/div/div/div/form/input[3]')
        password.send_keys(pwd)

        self.click_and_wait('/html/body/section/div/div/div/div/form/button')

    def signup_user(self, name, pwd, f_name, l_name):
        self.assertIn("signup", self.selenium.current_url)

        field = self.selenium.find_element_by_xpath('//*[@id="id_user-username"]')
        field.send_keys(name)

        field = self.selenium.find_element_by_xpath('//*[@id="id_user-password"]')
        field.send_keys(pwd)

        field = self.selenium.find_element_by_xpath('//*[@id="id_user-first_name"]')
        field.send_keys(f_name)

        field = self.selenium.find_element_by_xpath('//*[@id="id_user-last_name"]')
        field.send_keys(l_name)

        self.click_and_wait('/html/body/section/div/form/div[5]/div/button')