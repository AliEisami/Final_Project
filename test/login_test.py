import logging
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from infra.browser_wrapper import BrowserWrapper
from infra.config_provider import ConfigProvider
from infra.logger import Logger
from logic.first_page import FirstPage
from logic.login_page import LoginPage


class LoginTest(unittest.TestCase):

    def setUp(self):
        # Initialize the browser and load configuration
        self.browser = BrowserWrapper()
        self.config = ConfigProvider.load_from_file()

        # Start the browser session and navigate to the specified URL
        self.driver = self.browser.get_driver(self.config['url'])

    def tearDown(self):
        # Quit the WebDriver session after test execution
        self.driver.quit()

    def test_login_successful(self):
        # Test case for successful login
        logging.info("Successful Login Test")
        first_page = FirstPage(self.driver)
        first_page.login_button_click()     # click the Login button
        login_page = LoginPage(self.driver)
        login_page.fill_login_email_input(self.config['email'])     # Enter email
        login_page.continue_button_click()      # click the continue button
        login_page.fill_login_password_input(self.config['password'])       # Enter password
        login_page.continue_button_click()      # click the continue button

        # Wait up to 5 seconds until the URL matches the expected pattern
        WebDriverWait(self.driver, 5).until(EC.url_matches(f"https://trello.com/u/{self.config['username']}/boards"))
        # Assert that the current URL matches the expected user URL
        self.assertEqual(self.driver.current_url, f"https://trello.com/u/{self.config['username']}/boards")

    def test_login_unsuccessful(self):
        # Test case for unsuccessful login
        logging.info("UnSuccessful Login Test")
        first_page = FirstPage(self.driver)
        first_page.login_button_click()
        login_page = LoginPage(self.driver)
        login_page.fill_login_email_input(self.config['email'])
        login_page.continue_button_click()
        login_page.fill_login_password_input(self.config['wrong_password'])
        login_page.continue_button_click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, login_page.LOGIN_ERROR)))
        self.assertTrue(self.driver.find_element(By.XPATH, login_page.LOGIN_ERROR).is_displayed())
