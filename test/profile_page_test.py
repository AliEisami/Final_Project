import logging
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from infra.browser_wrapper import BrowserWrapper
from infra.config_provider import ConfigProvider
from infra.logger import Logger
from logic.first_page import FirstPage
from logic.home_page import HomePage
from logic.login_page import LoginPage
from logic.profile_page import ProfilePage


class ProfilePageTest(unittest.TestCase):

    def setUp(self):
        # Initialize the browser and load configuration
        self.browser = BrowserWrapper()
        self.config = ConfigProvider.load_from_file()

        # Start the browser session and navigate to the specified URL
        self.driver = self.browser.get_driver(self.config['url'])

        # Perform login
        FirstPage(self.driver).login_button_click()
        LoginPage(self.driver).login_flow(self.config['email'], self.config['password'])

        # Initialize HomePage and ProfilePage
        self.home_page = HomePage(self.driver)
        self.profile_page = ProfilePage(self.driver)

    def tearDown(self):
        # Revert the username change after test execution
        self.profile_page.change_back_username(self.config['username'])

        # Quit the WebDriver session
        self.driver.quit()

    def test_change_valid_username(self):
        # Test case for changing the username to a valid one
        logging.info("Valid Username Change Test")
        self.home_page.header_account_button_click()
        self.home_page.profile_and_visibility_button_click()
        self.profile_page.fill_random_username_input(5, 20, "lowercase")
        self.profile_page.profile_change_save_button_click()

        # Wait until the username input field text changes from the original username
        WebDriverWait(self.driver, 5).until(
            lambda driver:
            self.driver.find_element(By.XPATH, self.profile_page.USERNAME_INPUT).text != self.config['username'])

        # Assert that the username has been changed successfully
        self.assertNotEqual(self.driver.find_element(By.XPATH,
                            self.profile_page.USERNAME_INPUT), self.config['username'])

    def test_change_invalid_username(self):
        # Test case for attempting to change the username to an invalid one
        logging.info("Invalid Username Change Test")
        self.home_page.header_account_button_click()
        self.home_page.profile_and_visibility_button_click()
        self.profile_page.fill_random_username_input(5, 20, "uppercase")
        self.profile_page.profile_change_save_button_click()

        # Wait until the error message is displayed and Assert that the error message is displayed
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, self.profile_page.ERROR_MESSAGE)))
        self.assertTrue(self.driver.find_element(By.XPATH, self.profile_page.ERROR_MESSAGE).is_displayed())
