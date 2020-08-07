import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from GuiCollection import GuiCollection
from ListOfAdvertisementsPage import AdvertisementsListsPage
from DetailsOfAdvertisementPage import AdvertisementDetails
from ExportData import DataProcessing
from tqdm import tqdm


class RunScraper:

    def __init__(self):
        self.default_url = 'https://www.4zida.rs/prodaja-stanova/novi-beograd-beograd?jeftinije_od=140000&struktura' \
                           '=dvoiposoban&struktura=trosoban&struktura=troiposoban&struktura=cetvorosoban&struktura' \
                           '=cetvoroiposoban '
        self.browser_path = 'C:/Users/g.ristic/PycharmProjects/4_zida/chromedriver.exe'

    def configure_and_start_browser(self, browser_options: list):
        """

        :param browser_options:
        :return: object: driver object
        """
        browser_configuration_list = browser_options
        browser_options = Options()
        for option in browser_configuration_list:
            browser_options.add_argument(option)
        return webdriver.Chrome(
            executable_path=self.browser_path, options=browser_options
        )

    @classmethod
    def teardownclass(cls, browser: object) -> None:
        """
        :param browser:
        """
        browser.close()
        browser.quit()


def main():
    # Browser configuration

    web_scraper_gui_options = GuiCollection.advanced_web_scraper_gui(gui_title='4 zida Web scraper')
    option_list = []
    if web_scraper_gui_options.get(1):
        option_list.append('--headless')
        option_list.append('--disable-gpu')
    if web_scraper_gui_options.get(3):
        option_list.append('--start-maximized')
    if web_scraper_gui_options.get(4):
        option_list.append('--incognito')
    # Initiate browser
    scraper = RunScraper()

    #  Define url for scraping. If no url is entered default url address is used.
    if web_scraper_gui_options.get(0):
        scraper.default_url = web_scraper_gui_options.get(0)

    # Run web scraper
    browser = scraper.configure_and_start_browser(option_list)
    list_of_advertisements = AdvertisementsListsPage(browser, scraper.default_url)
    extracted_urls = set(list_of_advertisements.extract_urls())
    message: str = '\nTotal extracted unique :' + str(len(extracted_urls)) + ' urls!' + '\nStarting data extraction ' \
                                                                                        'from URLS... '
    GuiCollection.success_notification(message=message)
    details_advertisement_page = AdvertisementDetails(browser)
    print('...extracting data from advertisements...')
    data_list = []
    for url in tqdm(extracted_urls):
        data_list.append(details_advertisement_page.scrape_advertisement_data(url))

    # File Export configuration
    excel_export = web_scraper_gui_options.get(5)
    html_export = web_scraper_gui_options.get(6)
    export_folder = os.getcwd() if web_scraper_gui_options.get(7) == '' else web_scraper_gui_options.get(7)
    send_email = web_scraper_gui_options.get(8)
    extension = ''

    if excel_export:
        extension = 'xlsx'
    elif html_export:
        extension = 'html'

    # Export scraping results
    process_data = DataProcessing(data_list)
    process_data.export_dataset(process_data.create_dataset(), export_format=extension, folder_name=export_folder,
                                export_title=' 4 zida')
    GuiCollection.success_notification(message='Data successfully exported!')

    scraper.teardownclass(browser)


if __name__ == '__main__':
    main()
