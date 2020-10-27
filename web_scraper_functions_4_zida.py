from selenium import webdriver
import smtplib
import sys
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import PySimpleGUI as sg
from selenium.common.exceptions import NoSuchElementException, \
    StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def web_scraper_config_gui() -> dict:
    sg.ChangeLookAndFeel('DefaultNoMoreNagging')

    layout = [[sg.Text()],
              [sg.Text('Enter URL which contains search criteria : ')],

              [sg.InputText('', size=(73, 1))],
              [sg.Text('NOTE: Blank entry will do search with default search '
                       'criteria.')],
              [sg.Text('')],
              [sg.Frame(layout=[
                  [sg.Radio('Background run (no GUI)', "RADIO1", default=True,
                            size=(41, 1)),
                   sg.Radio('Interactive mode', "RADIO1", default=False)],
                  [sg.Checkbox('Full screen', size=(20, 1), default=True,
                               tooltip='Recommended to keep')],
                  [sg.Checkbox('Incognito mode', size=(20, 1), default=True,
                               tooltip='Run browser in incognito mode')]],
                  title='Browser startup options', title_color='black',
                  relief=sg.RELIEF_GROOVE)],
              [sg.Text('')],
              [sg.Frame(layout=[
                  [sg.Checkbox('Excel (*.xlsx)', tooltip='Export results as Excel file', default=True),
                   sg.Checkbox('HTML', size=(20, 1), default=False, tooltip='Export results as HTML file')],

                  [sg.Text('Choose folder for file export:', auto_size_text=True, text_color='black', size=(20, 1))],
                  [sg.InputText('', justification='left'), sg.FolderBrowse()],
                  [sg.Checkbox('Send results via e-mail', tooltip='', default=False)]],
                  title=' Results export options', title_color='black', relief=sg.RELIEF_GROOVE)],

              [sg.Text('')],
              [sg.Submit(tooltip='Click to submit this configuration'), sg.Cancel()]]

    window = sg.Window('4 Zida (www.4zida.rs) Web Scraping Configurator', layout, default_element_size=(60, 1),
                       grab_anywhere=False, keep_on_top=True, resizable=True)

    # Event Loop to process "events"
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            return sys.exit()
        else:
            print(values)
            window.close()
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


def configure_browser_and_run():
    """
    :return configuration data, default_browser, url, exc_export, htm_export, eml_export
    :rtype tuple
    """
    configuration = web_scraper_config_gui()
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
    export_folder = configuration.get(7)
    eml_export = configuration.get(8)

    if url == '':
        default_url_address = 'https://www.4zida.rs/prodaja-stanova/novi-beograd-beograd?jeftinije_od=140000&struktura' \
                              '=dvoiposoban&struktura=trosoban&struktura=troiposoban&struktura=cetvorosoban&struktura' \
                              '=cetvoroiposoban&vece_od=64m2'
        url = default_url_address

    # headless browser setup and initialisation
    options = Options()
    for option in option_list:
        options.add_argument(option)

    default_browser = webdriver.Chrome(executable_path=r'C:\Users\g.ristic\PycharmProjects\4_zida\chromedriver.exe',
                                       options=options)
    return default_browser, url, exc_export, htm_export, export_folder, eml_export


def get_url_from_element(web_element, browser):
    try:
        browser.implicitly_wait(30)
        return web_element.get_attribute('href')
    except StaleElementReferenceException as stale_exception:
        print(stale_exception)
        browser.refresh()
        get_url_from_element(web_element, browser)



def extract_urls_from_search_criteria(browser) -> list:
    """
    Function access to opened page returns list of advertisements and returns list of URL link
    :param browser:  instance of headless browser passed to function, to extract data from JS generated page.
    :returns extracted urls as list
    """
    url_list = []
    try:
        browser.implicitly_wait(30)
        elements = browser.find_elements_by_css_selector('a.z4-classified-title-and-price')
        for element in elements:
            adv_url = get_url_from_element(element, browser)
            url_list.append(adv_url)
        print(len(url_list), 'advertisement urls extracted.\n')
    except NoSuchElementException:
        pass
    finally:
        return url_list


def extract_data_from_advertisement_page(page_url, browser) -> dict:
    """
    :rtype: object

    """
    print('Starting data extraction from url:', page_url, '\n')
    browser.get(page_url)
    browser.implicitly_wait(30)
    advertisement_data_dict = {'00 URL': page_url}

    # Get advertisement Title
    title = browser.find_element(By.CLASS_NAME,
                                 'font-weight-bold.mt-2.title-placeholder.ng-star-inserted').text
    advertisement_data_dict['01 Naslov'] = title

    # Get advertisement Sub-location
    sub_location = browser.find_element(By.XPATH, '//body//h3//span//span[1]').text
    advertisement_data_dict['02 Lokacija'] = sub_location

    # Get advertisement Price
    price = browser.find_element(By.CLASS_NAME, 'pr-2').text.replace('.', '').replace('€', '')
    advertisement_data_dict['03 Cena'] = price

    # Get basic advertisement data
    basic_data_dict = get_basic_advertisement_data(browser)
    advertisement_data_dict.update(basic_data_dict)

    return advertisement_data_dict


def get_basic_advertisement_data(browser) -> dict:
    """
    :type
    """
    characteristic_names_elements = browser.find_elements(By.XPATH,
                                                          '//div[@class="info-item ng-star-inserted"]//span[1]')
    characteristic_value_elements = browser.find_elements(By.XPATH, '//div[@class="info-item '
                                                                    'ng-star-inserted"]//span[2]')

    characteristic_names = [element.text for element in characteristic_names_elements if not
                            element.text.startswith('/')]
    characteristic_values = [element.text for element in characteristic_value_elements if not
                             element.text.startswith('sprat')]
    basic_data_dict = dict(zip(characteristic_names, characteristic_values))
    basic_data_dict['Cena po m2'] = basic_data_dict.get('Cena po m2').replace(' €/m2', '').replace('.', '')  # Data
    # cleanup

    return basic_data_dict


def send_email(attachment_filename, message_body_as_html='', subject=None,
               sender_email_address=None,
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
    with open('C:/Users/g.ristic/PycharmProjects/4_zida/' + attachment_filename, "rb") as attachment:
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

