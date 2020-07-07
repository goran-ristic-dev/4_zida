import sys
import PySimpleGUI as sg


class GuiCollection:
    """
    This class contains generalized methods for presentation of different GUI for collecting user inputs:
     advanced web scraper gui,
     simple web scraper config gui,
     file or folder selection gui,
     text input and folder selection gui,
     success notification gui,
     failure notification gui,
     email configuration gui
    """

    @staticmethod
    def advanced_web_scraper_gui(gui_title: str = '') -> dict:
        """
        This is advanced web scraper gui configuration window. Contains web browser configuration, and output
        configuration (export file format).
        :param gui_title: str
        :return: dict of configuration values
        """
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

                      [sg.Text('Choose folder for file export:', auto_size_text=True, text_color='black',
                               size=(20, 1))],
                      [sg.InputText('', justification='left'), sg.FolderBrowse()],
                      [sg.Checkbox('Send results via e-mail', tooltip='', default=False)]],
                      title=' Results export options', title_color='black', relief=sg.RELIEF_GROOVE)],

                  [sg.Text('')],
                  [sg.Submit(tooltip='Click to submit this configuration'), sg.Cancel()]]

        window = sg.Window(gui_title + ' Web Scraping Configurator', layout, default_element_size=(60, 1),
                           grab_anywhere=False, keep_on_top=True, resizable=True)
        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                return sys.exit()
            else:
                print('Web scraper configuration:\n', values)
                window.close()
                return values

    @staticmethod
    def simpler_web_scraper_config_gui(gui_title: str = '', url_tuple=()) -> dict:
        """
         Simpler Gui configuration for predefined url addresses selectable from drop-down.
        :param gui_title: title of gui window
        :param url_tuple: list of url addresses for scraping
        :return: dict Entered configuration as dictionary.
        """
        sg.ChangeLookAndFeel('DefaultNoMoreNagging')

        layout = [[sg.Text()],
                  [sg.Text('Select URL for scraping :')],
                  [sg.Combo(list(url_tuple), auto_size_text=True)],
                  # [sg.InputText('', size=(73, 1))],
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
                      [sg.Checkbox('Excel (*.xlsx)', tooltip='Export results as Excel file', default=False),
                       sg.Checkbox('CSV', size=(20, 1), default=True, tooltip='Export results as HTML file')],

                      [sg.Text('Choose folder for file export:', auto_size_text=True, text_color='black',
                               size=(20, 1))],
                      [sg.InputText('', justification='left'), sg.FolderBrowse()]],
                      # [sg.Checkbox('Send results via e-mail', tooltip='', default=False)]],
                      title=' Results export options', title_color='black', relief=sg.RELIEF_GROOVE)],

                  [sg.Text('')],
                  [sg.Submit(tooltip='Click to submit this configuration'), sg.Cancel()]]

        window = sg.Window(gui_title, layout, default_element_size=(60, 1), grab_anywhere=False,
                           keep_on_top=True, resizable=True)

        # Event Loop to process "events"
        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                return sys.exit()
            else:
                print(values)
                window.close()
                return values

    @staticmethod
    def file_or_folder_selection_gui(tab1_title: str, tab2_title: str, gui_title: str = '',
                                     additional_option_file: str = 'file option',
                                     additional_option_folder: str = 'folder option') -> dict:
        """
        This is configuration gui for selection between file  and/or folder with different options.
        :param gui_title: str
        :param tab2_title: str
        :param tab1_title: str
        :param additional_option_folder: str
        :type additional_option_file: str
        :rtype dict
        """
        sg.ChangeLookAndFeel('Default1')

        tab1_layout = [[sg.Text('')],
                       [sg.Text('Select file:', auto_size_text=True, text_color='black'), sg.InputText(''),
                        sg.FileBrowse()],
                       [sg.Checkbox(additional_option_file)]]

        tab2_layout = [[sg.Text('')],
                       [sg.Text('Choose folder:', auto_size_text=True, text_color='black'), sg.InputText(''),
                        sg.FolderBrowse()],
                       [sg.Checkbox(additional_option_folder)]]

        layout = [[sg.TabGroup(
            [[sg.Tab(tab1_title, tab1_layout), sg.Tab(tab2_title, tab2_layout)]])],
            [sg.Text('')],
            [sg.Button('Submit'), sg.Cancel()]]

        window = sg.Window(gui_title, layout, default_element_size=(50, 4), keep_on_top=True)

        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                window.close()
            else:
                window.close()
                return values

    @staticmethod
    def text_input_and_folder_selection_gui(gui_title='', text_field_label='input text', option1='option1',
                                            option2='option2', option3='option3', option4='option4') -> dict:
        """
        This gui has two  entry fields . Text input field, and Folder selection for output.
        Some actions can be done on text input eg. opening url.
        :param gui_title: str
        :param text_field_label: str
        :param option1: str
        :param option2: str
        :param option3: str
        :param option4: str
        :return: dict
        """
        sg.ChangeLookAndFeel('Default1')

        layout = [
            [sg.Text(text_field_label, auto_size_text=True, text_color='black', size=(20, 1)), sg.InputText('')],
            [sg.Text('')],
            [sg.Text('Choose download folder:', auto_size_text=True, text_color='black', size=(20, 1)),
             sg.InputText('', justification='left'), sg.FolderBrowse()],
            [sg.Frame(layout=[
                [sg.Radio(option1, "RADIO1", default=True), sg.Radio(option2, "RADIO1"), sg.Radio(option3, "RADIO1"),
                 sg.Radio(option4, "RADIO1")]],
                title='Options', title_color='black', relief=sg.RELIEF_SUNKEN)],
            [sg.Text('')],
            [sg.Submit(), sg.Cancel()]]

        window = sg.Window(gui_title, layout, default_element_size=(50, 1),
                           grab_anywhere=False, keep_on_top=True)
        # Event Loop to process "events"
        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                return sys.exit()

            else:
                # Config from dictionary  converted to tuple
                window.close()
                return values

    @staticmethod
    def success_notification(message: str = '') -> None:
        """
        Popup message for successful action.
        :param message: str: Message will be passed to the output window.
        :return:
        """
        sg.Popup('Finished!\n' + message, title='Notification', grab_anywhere=True, keep_on_top=True, auto_close=True,
                 auto_close_duration=5)

    @staticmethod
    def failure_notification(message: str = '') -> None:
        """
        Popup message for failed action.
        :param message: str Message will be passed to the output window
        :rtype: None
        """
        sg.Popup('Failed!' + message, title='Failure!', grab_anywhere=True, keep_on_top=True, auto_close=True,
                 auto_close_duration=5)

    @staticmethod
    def email_config_gui(gui_title='', sender_email='', recipient_email='', subject='') -> dict:
        """
        Purpose of this configuration gui is to collect sender, receiver email and password, and subject of message.
        :param subject: subject of email message
        :param gui_title: title of gui window
        :param sender_email: senders email address
        :param recipient_email: recipient email address
        :return: dict: Configuration dictionary.
        """
        layout = [
            [sg.Text('NOTE: Only Gmail sender accounts are supported')],
            [sg.Text('     Sender email:  '),
             sg.InputText(default_text=sender_email, size=(30, 1), disabled=False, password_char="")],
            [sg.Text('   Receiver email:  '),
             sg.InputText(default_text=recipient_email, size=(30, 1), disabled=False, password_char="")],
            [sg.Text(' Email password:  '),
             sg.InputText(default_text="", size=(30, 1), disabled=False, password_char="*")],
            [sg.Text('            Subject:   '), sg.InputText(default_text=subject, disabled=False, password_char="")],
            [sg.Submit(tooltip='Click to submit this configuration'), sg.Cancel()]]

        window = sg.Window(gui_title, layout, default_element_size=(60, 1),
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
