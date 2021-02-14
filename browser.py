from selenium import webdriver


class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')

    def go(self, url):
        self.driver.get(url)


if __name__ == '__main__':
    Browser()
