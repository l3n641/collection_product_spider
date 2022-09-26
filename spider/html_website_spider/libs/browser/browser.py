from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from urllib3.exceptions import MaxRetryError
from urllib.parse import urlparse


class Browser(object):

    def __init__(self, driver):

        self._driver = driver

    def get(self, url):
        try:
            self._driver.get(url)
            return True
        except MaxRetryError as e:
            raise e
        except Exception as e:
            return False

    def click(self, xpath, time_sleep=1, timeout=10):
        self.webdriver_wait_until(timeout, EC.presence_of_element_located((By.XPATH, xpath)))
        element = self._driver.find_element_by_xpath(xpath)

        webdriver.ActionChains(self._driver).move_to_element(element).click(element).perform()

        if time_sleep:
            time.sleep(time_sleep)

    def click_by_script(self, xpath, time_sleep=1, timeout=10, ):
        self.webdriver_wait_until(timeout, EC.presence_of_element_located((By.XPATH, xpath)))
        element = self._driver.find_element_by_xpath(xpath)
        self._driver.execute_script("arguments[0].click();", element)
        if time_sleep:
            time.sleep(time_sleep)

    def get_element_by_xpath(self, xpath, timeout=10, time_sleep=1, ):
        """
        获取指定元素
        :param xpath:
        :param timeout:
        :param time_sleep:
        :return:
        """
        element = self.webdriver_wait_until(timeout, EC.presence_of_element_located((By.XPATH, xpath)))
        if time_sleep:
            time.sleep(time_sleep)
        return element

    def send_keys(self, xpath, value, time_sleep=1, timeout=30, append=True, click=False, click_sleep_time=1):
        element = self.webdriver_wait_until(timeout, EC.presence_of_element_located((By.XPATH, xpath)))
        if click:
            webdriver.ActionChains(self._driver).move_to_element(element).click(element).perform()
            time.sleep(click_sleep_time)

        if not append:
            element.send_keys(Keys.CONTROL + 'a')
            self._driver.implicitly_wait(3)
            element.send_keys(Keys.BACKSPACE)
            element.clear()
        element.send_keys(value)  # send_keys
        if time_sleep:
            time.sleep(time_sleep)

    def close(self):
        self._driver.close()

    def implicitly_wait(self, timeout):
        self._driver.implicitly_wait(timeout)

    def implicitly_wait(self, timeout):
        self._driver.implicitly_wait(timeout)

    def web_driver_wait(self, timeout=10, poll_frequency=1, ignored_exceptions=None):
        return WebDriverWait(self._driver, timeout, poll_frequency, ignored_exceptions)

    def webdriver_wait_until(self, timeout, method, poll_frequency=0.5, ignored_exceptions=None):
        element = WebDriverWait(self._driver, timeout, poll_frequency, ignored_exceptions).until(method)
        return element

    def webdriver_wait_until_not(self, timeout, method, poll_frequency=0.5, ignored_exceptions=None):
        element = WebDriverWait(self._driver, timeout, poll_frequency, ignored_exceptions).until_not(method)
        return element

    def wait_display(self, xpath, timeout=10):
        try:
            return self.webdriver_wait_until(timeout, EC.visibility_of_element_located((By.XPATH, xpath)))
        except (NoSuchElementException, TimeoutException):
            return False

    def wait_invisibility(self, xpath, timeout=10):
        try:
            return self.webdriver_wait_until(timeout, EC.invisibility_of_element_located((By.XPATH, xpath)))
        except (NoSuchElementException, TimeoutException):
            return False

    def is_display(self, xpath):
        try:
            element = self._driver.find_element_by_xpath(xpath)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    def find_elements_by_xpath(self, xpath, timeout=10, time_sleep=1):
        if time_sleep:
            time.sleep(time_sleep)
        try:
            element = self.webdriver_wait_until(timeout, EC.presence_of_element_located((By.XPATH, xpath)))
            return element
        except (NoSuchElementException, TimeoutException):
            return False

    @staticmethod
    def proxy_url_parse_to_dict(url):
        data = urlparse(url.strip())
        if data.hostname and data.port and data.scheme:
            proxy_server = {
                "type": data.scheme.upper(),
                "host": data.hostname,
                "port": data.port,
                "username": data.username,
                "password": data.password,
                "quantity": 0
            }
            return proxy_server
        return False

    @staticmethod
    def proxy_dict_parse_to_url(type, host, port, username=None, password=None):
        if username and password:
            proxy = f'{type.lower()}://{username}:{password}@{host}:{port}'
        else:
            proxy = f'{type.lower()}://{host}:{port}'
        return proxy

    def __getattr__(self, name):
        if hasattr(self._driver, name):
            return getattr(self._driver, name)
