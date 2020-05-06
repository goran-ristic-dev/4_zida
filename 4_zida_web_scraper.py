from web_scraper_functions_4_zida import *
import pandas as pd


def main():
    try:
        # Prepare configuration and start Browser process
        chrome_browser, url_address, excel_export, html_export, export_folder, email_export =\
            configure_browser_and_run()

        # Open start page (search results)
        print('Opening url:', url_address)
        chrome_browser.get(url_address + '&strana=1')
        # remove_gdpr_banner(chrome_browser)
        chrome_browser.implicitly_wait(30)

        # Get last page number
        pagination = chrome_browser.find_elements(By.CSS_SELECTOR, 'ul.pagination>li.page-item.ng-star-inserted')
        page_numbers = [element.text for element in pagination if element.text.isdigit()][-1]
        print([page_numbers])
        last_page_number = int(page_numbers[-1])
        first_page_number = int(page_numbers[0]) - 1

        print('Last page number:', last_page_number)
        print('First page number:', first_page_number)

        # Extract URLs from first page
        url_list = extract_urls_from_search_criteria(chrome_browser)

        # Extract URLs from remaining pages
        for i in range(first_page_number + 1, last_page_number + 1):
            print(i)
            chrome_browser.get(url_address + '&strana=' + str(i))
            print('Processing :', url_address + '&strana=' + str(i))
            b = extract_urls_from_search_criteria(chrome_browser)
            url_list = url_list + b
        url_set = set(url_list)  # cleaning up eventual duplicates

        print('\nTotal extracted unique:', len(url_set), 'urls!')

        sg.Popup(
            'URL extraction finished!' + '\nTotal extracted unique :' + str(len(url_set)) + ' urls!' +
            '\nStarting data extraction from URLS...', title='Notification', auto_close=True, auto_close_duration=5)

        #  Commented code part should be used if progress bar is implemented

        # output = []
        # for url_address in url_set:
        #     advertisement_data_dict = extract_data_from_advertisement_page(url_address, chrome_browser)
        #     output.append(advertisement_data_dict)

        output = [extract_data_from_advertisement_page(url_address, chrome_browser) for url_address in url_set]

        # Organize data
        df = pd.DataFrame()
        for dict_item in output:
            df1 = pd.DataFrame.from_records(dict_item, index=[1])
            df = df.append(df1, sort=True, verify_integrity=False)
        df.reset_index(drop=True, inplace=True)

        # Export data
        if export_folder:
            export_folder = export_folder + '/'

        if excel_export:
            df.to_excel(export_folder + datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + ' 4zida scrapped data.xlsx',
                        engine='xlsxwriter')
        if html_export:
            df.to_html(export_folder + datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + ' 4zida scrapped data.html')

        chrome_browser.close()
        # window.close()
        sg.Popup('Scraping finished!', title='Success!', grab_anywhere=True, keep_on_top=True, auto_close=True,
                 auto_close_duration=5)
    except NoSuchElementException:
        pass

    if __name__ == '__main__':
        main()

