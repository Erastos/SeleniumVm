from selenium import webdriver


class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get("http://www.google.com")


if __name__ == '__main__':
    Browser()
