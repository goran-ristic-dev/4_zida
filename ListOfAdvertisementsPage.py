from selenium.webdriver.common.by import By
from tqdm import tqdm


class AdvertisementsListsPage:

    def __init__(self, browser: object, url: str):
        """

        :type url: str
        """
        self.url = url
        self.browser = browser

        # Locators
        self.advertisement_url_elements_css = 'a.z4-classified-title-and-price'  # advertisement locator
        self.pagination_css = 'a.page-link.ng-star-inserted'  # pagination locator a.page-link.ng-star-inserted

    def __str__(self):
        return f"Url: {self.url},\n locators:\n {self.advertisement_url_elements_css},\n {self.pagination_css} "

    def get_number_of_pages(self):
        self.browser.get(self.url)
        self.browser.implicitly_wait(40)
        try:
            pagination = self.browser.find_elements(By.CSS_SELECTOR, self.pagination_css)
            page_numbers = [element.text for element in pagination if element.text.isdigit()]
            last_page_number = int(page_numbers[-1])
            first_page_number = int(page_numbers[0])
            return first_page_number, last_page_number
        except Exception as exc:
            print(exc)

    def get_urls_from_page(self):
        self.browser.implicitly_wait(30)
        advertisement_url_elements = self.browser.find_elements(By.CSS_SELECTOR, self.advertisement_url_elements_css)
        url_list = [element.get_attribute('href') for element in advertisement_url_elements]
        return url_list

    def extract_urls(self):
        self.browser.implicitly_wait(30)
        print('Starting extraction...')
        # start_page, stop_page
        start_page, stop_page = self.get_number_of_pages()
        list_of_urls = self.get_urls_from_page()
        print('\n...looping trough advertisement pages...')

        for i in tqdm(range(start_page, stop_page)):
            # print('Extracting urls from page:', str(i + 1))
            self.browser.get(self.url + '&strana=' + str(i + 1))
            list_of_urls += self.get_urls_from_page()
        return list_of_urls
