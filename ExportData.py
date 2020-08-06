from datetime import datetime
import pandas as pd
from pandas import DataFrame


class UnsupportedFileFormat(ValueError):
    pass


class DataProcessing:
    """
    This class contains methods used for  da
    """

    def __init__(self, data, data_type: str = ''):
        """
        :type data: List of dictionaries od dictionary if data_type is specified as dict
        """
        self.data = data
        self.data_type = data_type

    def create_dataset(self) -> "DataFrame":
        """
        :return: "DataFrame" object
        """
        df = pd.DataFrame()
        if self.data_type == 'dict':
            self.data = list(self.data)
        elif self.data_type == '':
            pass
        else:
            raise TypeError('Unsupported data type. Only list of dictionaries or dictionary are supported!')

        for dict_item in self.data:
            df1 = pd.DataFrame.from_records(dict_item, index=[1])
            df = df.append(df1, sort=True, verify_integrity=False)
        df.reset_index(drop=True, inplace=True)
        return df

    @staticmethod
    def export_dataset(data_frame, export_format: str, folder_name: str = '', export_title: str = ''):

        # Export data
        if folder_name:
            folder_name += '/'

        if export_format == 'xlsx':
            data_frame.to_excel(folder_name + datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + export_title + ' scrapped '
                                                                                                            'data.xlsx',
                                engine='xlsxwriter')

        if export_format == 'html':
            data_frame.to_html(folder_name + datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + export_title + ' scrapped '
                                                                                                           'data.html')

        if export_format == 'csv':
            data_frame.to_csv(folder_name + datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + export_title + ' scrapped '
                                                                                                          'data.csv')
        else:
            raise UnsupportedFileFormat('File format is not supported')
