import pandas as pd
from datetime import date, timedelta, datetime

#  Date before 2 days
today  = date.today()-timedelta(days=2)
nameOfDownloadFile = f"Downloaded-{today}.csv"
nameOfSaveFile = f"Saved-{today}.csv"

class covid19Data:

    def __init__(self, url):
        self.url = url

    def validate(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return 1
        except Exception as e:
            return 0

    def getDataFrame(self):

        try:
            getUrl = self.url

            # to access the content of the CSV file
            getContentOfFile = getUrl.content

            # writing the content into CSV file    w-writing ,  b- binary mode,  a - append
            opnCSVFile = open(nameOfDownloadFile, 'wb')
            opnCSVFile.write(getContentOfFile)

            opnCSVFile.close()

            # Pandas guessing dtypes for each column is very memory demanding so here we use low_memory = False
            dataFrame = pd.read_csv(nameOfDownloadFile, low_memory=False)

            lengthOfColumn = len(dataFrame.columns)

            if(lengthOfColumn >= 7):

                startOfDateColumn = dataFrame.columns[6]
                dataType = dataFrame.dtypes[startOfDateColumn]

                # check the data type of next column which is date and also check the format
                if dataType != "float64" or self.validate(startOfDateColumn) != 1:
                    return [dataFrame,False]

                columnNames = list(dataFrame.columns[0:6])
                requiredColumnName = ['region','geo_type', 'transportation_type', 'alternative_name', 'sub-region', 'country']

                # we can also check through columnNames == requiredColumnName but if we swap two column then it will fail
                # here we check the column name one by one
                for x in requiredColumnName:
                    if x not in columnNames:
                        return [dataFrame,False]

                return [dataFrame, True]

            else:
                return [dataFrame, False]

        except Exception as e:
            print(e.__class__)
            print("can't access dataFrame")
            return [0,False]


    def reArrangeDataFrame(self,dataFrame):

        try:
            # convert some columns into the rows
            if(len(dataFrame.columns)>=7):

                columnNames = list(dataFrame.columns[0:6])
                newDataFrame = dataFrame.melt(id_vars=columnNames, var_name="Date", value_name="Value")

                return [newDataFrame, True]
            else:

                return [0, False]

        except Exception as e:
            print(e.__class__)
            print("can not be convert columns into the rows")
            return [0,False]


    def saveFile(self, dataFrame):

        try:
            dataFrame.to_csv(nameOfSaveFile)
            return 1

        except Exception as e:
            print(e.__class__)
            print("can't Save")
            return 0


    def run(self):
        dataFrame = self.getDataFrame()

        if (dataFrame[1] == False):
            print("Failed")
            return False

        else:
            newDF = self.reArrangeDataFrame(dataFrame[0])[0]

            finalResult = self.saveFile(newDF)

            if(finalResult == 1):
                print("Successfully Saved")
                return True
            else:
                return False






