from selenium import webdriver


class Browser:
    def __init__(self):
        self.driver = webdriver.chrome()
        driver.get("http://www.google.com")