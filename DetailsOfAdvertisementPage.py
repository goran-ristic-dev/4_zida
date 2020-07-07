from selenium.webdriver.common.by import By


class AdvertisementDetails:
    def __init__(self, browser):
        # self.url = url
        self.browser = browser
        # basic data locators
        self.title_class = 'font-weight-bold.mt-2.title-placeholder.ng-star-inserted'
        self.location_xpath = '//body//h3//span//span[1]'
        self.price_class = 'pr-2'
        self.characteristic_names_elements_xpath = '//div[@class="info-item ng-star-inserted"]//span[1]'
        self.characteristic_value_elements_xpath = '//div[@class="info-item ng-star-inserted"]//span[2]'

    def scrape_advertisement_data(self, url) -> dict:
        """

        """
        self.browser.get(url)
        self.browser.implicitly_wait(30)
        # scrape basic data
        # scrape advertisement title
        title = self.browser.find_element(By.CLASS_NAME, self.title_class).text
        # scrape advertisement location
        location = self.browser.find_element(By.XPATH, self.location_xpath).text
        # scrape advertisement price
        price = self.browser.find_element(By.CLASS_NAME, self.price_class).text.replace('.', '').replace('€', '')
        scraped_items = ['00 URL', '01 Naslov', '02 Lokacija', '03 Cena']
        scraped_values = [url, title, location, price]
        scraped_data: dict = dict(zip(scraped_items, scraped_values))
        # scrape additional data
        characteristic_names_elements = self.browser.find_elements(By.XPATH, self.characteristic_names_elements_xpath)
        characteristic_value_elements = self.browser.find_elements(By.XPATH, self.characteristic_value_elements_xpath)

        characteristic_names = [element.text for element in characteristic_names_elements if not
                                element.text.startswith('/')]
        characteristic_values = [element.text for element in characteristic_value_elements if not
                                 element.text.startswith('sprat')]
        numerated_characteristic_names = [('1' + str(num) + ' ' + value) for num, value in
                                          enumerate(characteristic_names)]
        scraped_additional_data: dict = dict(zip(numerated_characteristic_names, characteristic_values))
        print('Data extracted from page.')
        total_dict: dict = {**scraped_data, **scraped_additional_data}

        return total_dict
