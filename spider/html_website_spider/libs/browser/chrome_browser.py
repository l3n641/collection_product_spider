import time

from selenium import webdriver
from .browser import Browser
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class ChromeBrowser(Browser):

    def __init__(self, executable_path, proxy_server=None, debugger_address=None):
        chrome_options = self.get_chrome_option(proxy_server, debugger_address)
        service = self.get_chrome_server(executable_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        super(ChromeBrowser, self).__init__(driver)

    @staticmethod
    def get_chrome_server(executable_path):
        service = Service(executable_path=executable_path, )
        return service

    @classmethod
    def get_chrome_option(cls, proxy_server=None, debugger_address=None):
        chrome_options = Options()

        if debugger_address:
            chrome_options.add_experimental_option("debuggerAddress", debugger_address)

        else:
            prefs = {"profile.managed_default_content_settings.images": 2}

            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option("detach", True)
            # chrome_options.add_experimental_option("prefs", prefs)

        if proxy_server:
            proxy_url = cls.proxy_dict_parse_to_url(proxy_server.get("type"), proxy_server.get("host"),
                                                    proxy_server.get("port"), proxy_server.get("username"),
                                                    proxy_server.get("password"))
            chrome_options.add_argument(f"proxy-server={proxy_url}")
        return chrome_options


def get_product_url(driver):
    urls = []
    elements = driver.find_elements(By.XPATH, '//div[@class="tile-media"]/a[@href!="#"]')
    for element in elements:
        url = element.get_attribute("href")
        urls.append(url)
    return urls


def scroll(setup=1000, time_sleep=2):
    next_position = 2000

    while next_position < 15000:
        driver.execute_script(f"window.scrollTo(0,{next_position});")
        next_position = next_position + setup
        time.sleep(time_sleep)


if __name__ == "__main__":
    from selenium.webdriver.common.by import By

    driver = ChromeBrowser("F:\code\collection_product_spider\chromedriver.exe")
    response = driver.get("https://www.ae.com/us/en/c/women/dresses-skirts/cat1320034?pagetype=plp")
    scroll()
    urls = get_product_url(driver)
    driver.quit()
