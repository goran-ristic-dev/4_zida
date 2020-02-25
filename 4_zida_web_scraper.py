from datetime import datetime
from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
# import pandas as pd
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import PySimpleGUI as sg
import sys


# Functions
def check_for_last_page(browser) -> bool:
    """
    Function checks for existence of element which indicates next page.
    :returns  Bool True, if next_page_identifier exist or False if item does not exist
    """
    try:
        browser.implicitly_wait(20)
        disabled_next_page = browser.find_element_by_css_selector('li.page - item.ng - star - inserted.disabled')
        print('No more pages left')
        return True
    except NoSuchElementException as disabled_exception:
        return False


def remove_gdpr_banner(browser) -> None:  # DONE
    """
    Function removes  GDPR banner after first access to the site
    :param browser:  instance of headless browser passed to function, to extract data from JS generated page.
    :returns None
    """
    try:
        cookie_bar_button = browser.find_element_by_link_text("Prihvati").click()
        print('Success!')
    except NoSuchElementException as nse:
        print('Element not found', nse)
        pass


def configure_browser_and_run():
    """
    :return:
    """
    configuration = configurator_gui()
    url = configuration.get(0)
    # Browser configuration
    option_list = []
    if configuration.get(1):
        option_list = ['--headless', '--disable-gpu']
    if configuration.get(3):
        option_list.append('--start-maximized')
    if configuration.get(4):
        option_list.append('--incognito')
    # File Export configuration
    exc_export = configuration.get(5)
    htm_export = configuration.get(6)
    eml_export = configuration.get(7)

    default_url_address = 'https://www.4zida.rs/prodaja-stanova/novi-beograd-beograd?jeftinije_od=140000&struktura' \
                          '=dvoiposoban&struktura=trosoban&struktura=troiposoban&struktura=cetvorosoban&struktura' \
                          '=cetvoroiposoban&vece_od=65m2 '
    if url == '':
        url = default_url_address

    # headless browser setup and initialisation
    options = Options()
    for option in option_list:
        options.add_argument(option)

    default_browser = webdriver.Chrome(executable_path=r'C:\Users\g.ristic\PycharmProjects\Cityexpert\chromedriver.exe',
                                       options=options)

    return default_browser, url, exc_export, htm_export, eml_export


def extract_urls_from_search_criteria(browser) -> list:
    """
    Function access to opened page returns list of advertisements and returns list of URL link
    :param browser:  instance of headless browser passed to function, to extract data from JS generated page.
    :returns extracted urls as list
    """
    browser.implicitly_wait(15)
    url_list = []
    elements = browser.find_elements_by_css_selector('a.z4-classified-title-and-price')
    for element in elements:
        try:
            adv_url = element.get_attribute('href')
            url_list.append(adv_url)
        except StaleElementReferenceException as stale_exception:
            browser.refresh()
            browser.implicitly_wait(25)
            adv_url = element.get_attribute('href')
            url_list.append(adv_url)
    print(len(url_list), 'advertisement urls extracted.\n')
    return url_list


def extract_data_from_advertisement_page(page_url, browser) -> tuple:
    """

    """
    print('Starting data extraction from url:', page_url, '\n')
    pass
    # browser.get(page_url)
    # browser.implicitly_wait(10)
    # title_element = browser.find_element_by_css_selector('div.street-address-wrap')
    # price_element = browser.find_element_by_xpath('/html/body/app/app-wrap/property-view/div/div['
    #                                               '4]/prop-price/div/div[1]/h3')
    # page_elements = browser.find_elements_by_css_selector('prop-name-value')
    # other_page_elements = browser.find_elements_by_css_selector('div.propLabelWrap')
    # additional_elements = browser.find_element_by_css_selector('div.glyph-label-wrap').find_elements_by_tag_name('h5')
    # excluded_additional_elements = browser.find_elements_by_css_selector('div.disabled')
    #
    # characteristics = []
    # title = title_element.text.replace('/ Prodaja / Stan', '')[:-10]
    # price = price_element.text.replace('.', '').strip(' €')
    # characteristics.append('Cena (€): ' + price)
    # for element in page_elements:
    #     characteristics.append(element.text.replace('\n', ': '))
    #
    # for other in other_page_elements:
    #     a = other.text.split('\n')
    #     combine = a[0] + ':'
    #     for i in range(len(a[1:])):
    #         combine = combine + ' ' + a[i] + ','
    #     characteristics.append(combine[:-1])
    #
    # excluded_list = []
    # for excluded in excluded_additional_elements:
    #     excluded_list.append(excluded.text)
    #
    # additional_info = 'Opremljenost objekta: '
    # for additional in additional_elements:
    #     if additional.text not in excluded_list:
    #         additional_info = additional_info + additional.text + ', '
    # characteristics.append(additional_info[:-1])
    #
    # return characteristics, title  # T # TODO


def send_email(attachment_filename, message_body_as_html='', subject=None, sender_email_address=None,
               receiver_email_address=None, password=None, ):
    """"
    Sends Email from google mail account
    :param message_body_as_html:
    :param attachment_filename:
    :param subject: Message subject
    :param password: Email password default can be used
    :param sender_email_address: default can be used
    :param receiver_email_address: default can be used
    """
    email_configuration = email_config_gui()
    sender_email_address = email_configuration.get(0)
    receiver_email_address = email_configuration.get(1)
    password = email_configuration.get(1)
    subject = datetime.now().strftime('%Y''_%m''_%d''_%H''_%M') + email_configuration.get(2)
    # if password is None:
    #    password = ''
    # if sender_email_address is None:
    #    sender_email_address = 'ristaa@gmail.com'
    # if receiver_email_address is None:
    #    receiver_email_address = 'goran.ristic@email.com;ristaa@gmail.com'

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email_address
    message["To"] = receiver_email_address
    # Add body to email
    message.attach(MIMEText(message_body_as_html, 'html'))

    # Open  file in binary mode
    with open('C:/Users/g.ristic/PycharmProjects/Cityexpert/' + attachment_filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Connect to the server
    server.starttls()  # Use TLS
    server.login(sender_email_address, password)  # Login to the email server
    server.sendmail(sender_email_address, receiver_email_address, text)  # Send the email
    server.quit()  # Logout of the email server
    return None


def configurator_gui() -> dict:
    sg.ChangeLookAndFeel('LightBlue7')

    layout = [
        [sg.Text('Enter url which contains search criteria : ')],

        [sg.InputText(''), sg.Text('NOTE: Blank entry will do search with default address.')],
        [sg.Frame(layout=[
            [sg.Radio('Background run (no GUI)', "RADIO1", default=True, size=(18, 1)),
             sg.Radio('Interactive mode', "RADIO1")],
            [sg.Checkbox('Full screen', size=(20, 1), default=True, tooltip='Recommended to keep')],
            [sg.Checkbox('Incognito mode', size=(20, 1), default=False, tooltip='Run browser in incognito mode')]],
            title='Browser startup options', title_color='black', relief=sg.RELIEF_GROOVE)],
        [sg.Frame(layout=[
            [sg.Checkbox('Excel (*.xlsx)', tooltip='Export results to excel file'),
             sg.Checkbox('HTML', size=(20, 1), default=False, tooltip='Export results to html file')]],
            title=' Results export options', title_color='black', relief=sg.RELIEF_GROOVE)],
        [sg.Text('Choose folder for file export:', auto_size_text=True, text_color='black', size=(20, 1)),

         sg.InputText('', justification='left'), sg.FolderBrowse()],
        [sg.Text('')],
        [sg.Checkbox('Send results via email', tooltip='', default=True)],
        [sg.Text('')],
        [sg.Submit(tooltip='Click to submit this configuration'), sg.Cancel()]]

    window = sg.Window('Cityexpert (www.cityexpert.rs) web scraping configurator', layout, default_element_size=(50, 1),
                       grab_anywhere=False)

    # Event Loop to process "events"
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            return sys.exit()
        else:
            print(values)
            return values


def email_config_gui() -> dict:
    layout = [
        [sg.Text('NOTE: Only Gmail sender accounts are supported')],
        [sg.Text('     Sender email:  '),
         sg.InputText(default_text="", size=(30, 1), disabled=False, password_char="")],
        [sg.Text('   Receiver email:  '),
         sg.InputText(default_text="", size=(30, 1), disabled=False, password_char="")],
        [sg.Text(' Email password:  '), sg.InputText(default_text="", size=(30, 1), disabled=False, password_char="*")],
        [sg.Text('            Subject:   '), sg.InputText(default_text="", disabled=False, password_char="")],

        [sg.Submit(tooltip='Click to submit this configuration'), sg.Cancel()]]

    window = sg.Window('Email configuration', layout, default_element_size=(60, 1),
                       grab_anywhere=False)

    # Event Loop to process "events"
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            print(event, values)
            return sys.exit()

        else:
            print(event, values)
            return values


def main():
    # Prepare and start process
    chrome_browser, url_address, excel_export, html_export, email_export = configure_browser_and_run()
    # Accessing to the start page
    print('Opening url:', url_address, '\n')
    chrome_browser.get(url_address)
    chrome_browser.implicitly_wait(20)
    remove_gdpr_banner(chrome_browser)

    # Extract urls from all pages:
    url_list = []
    i = 41
    while not check_for_last_page(chrome_browser):
        chrome_browser.get(url_address + '&strana=' + str(i))
        print('Processing page:', i)
        chrome_browser.implicitly_wait(20)
        b = extract_urls_from_search_criteria(chrome_browser)
        url_list = url_list + b
        i += 1
        # chrome_browser.find_element_by_link_text('»').click()
    else:
        b = extract_urls_from_search_criteria(chrome_browser)
        url_list = url_list + b
    print(url_list)
    print('\nTotal extracted :', len(url_list), 'urls!')
    chrome_browser.find_element_by_name


if __name__ == '__main__':
    main()

#li.page - item.ng - star - inserted.disabled

#aria-label="Last"
