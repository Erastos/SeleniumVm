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
        xPathExpression = f"//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{link_text.lower()}')]"
        result = self.driver.find_elements_by_xpath(xPathExpression)
        text = map(lambda x: x.text, result)
        urls = map(lambda x: x.get_attribute('href'), result)
        link_info = {name:url for name, url in zip(text, urls)}
        return link_info

    def close(self):
        return self.driver.close()


if __name__ == '__main__':
    browser = Browser()
    browser.go("https://news.ycombinator.com")
    print(browser.get_all_links("A new"))
    browser.close()
