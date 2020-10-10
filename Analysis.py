import pandas as pd
import requests
from datetime import date, timedelta, datetime

FileNameToDownload = "Downloaded-{date_today}.csv"
FileNameToSave = "Saved-{date_today}.csv"
RequiredColumnName = {'region', 'geo_type', 'transportation_type', 'alternative_name', 'sub-region', 'country'}


class Covid19Data:
    def __init__(self, url):
        self.url = url
        date_today = date.today() - timedelta(days=2)
        self.file_name_to_save = FileNameToSave.format(date_today)
        self.file_name_to_downlaod = FileNameToDownload.format(date_today)

    @staticmethod
    def validate(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except Exception as e:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD: {}".format(e))

    def get_data_frame(self):
        try:
            data = requests.get(self.url)
            data_content = data.content

            csv_file = open(self.file_name_to_downlaod, 'wb')
            csv_file.write(data_content)
            csv_file.close()

            # Pandas guessing dtypes for each column is very memory demanding so here we use low_memory = False
            dataFrame = pd.read_csv(self.file_name_to_downlaod, low_memory=False)
            self.validate(self, dataFrame.columns[6])
            if set(dataFrame.columns[0:6]) == RequiredColumnName:
                return dataFrame
        except Exception as e:
            raise Exception("Error generating DF: {}".format(e))

    @staticmethod
    def rearrange_data_frame(self, dataFrame):
        try:
            return dataFrame.melt(id_vars=list(dataFrame.columns[0:6]), var_name="Date", value_name="Value")
        except Exception as e:
            raise Exception("Can not convert columns into rows: {}".format(e))

    def save_file(self, df):
        try:
            df.to_csv(self.file_name_to_save)
        except Exception as e:
            raise Exception("Error saving DF to file: {}".format(e))

    def run(self):
        dataFrame = self.get_data_frame()
        if dataFrame:
            newDF = self.rearrange_data_frame(self, dataFrame)
            self.save_file(newDF)
            print("Successfully Saved with file name: {}".format(self.file_name_to_save))
