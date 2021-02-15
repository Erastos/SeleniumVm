from selenium import webdriver


class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')

    def go(self, url):
        self.driver.get(url)

    def get_elements_by_tag(self, tag):
        result = self.driver.find_elements_by_tag_name(tag)
        return result

    def get_all_links(self, link_text):
        result = self.driver.find_elements_by_partial_link_text(link_text)
        return list(map(lambda x: x.text, result))


if __name__ == '__main__':
    browser = Browser()
    browser.go("https://news.ycombinator.com")
    print(browser.get_all_links("SolarWinds"))
